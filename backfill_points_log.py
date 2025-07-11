#!/usr/bin/env python3
"""
Backfill script to populate PointsLog from existing DailyStats data.

This script creates PointsLog entries from existing DailyStats to provide
detailed point breakdowns for historical data.
"""

import sys
import os
from datetime import datetime, timedelta

# Add the app directory to the path so we can import our modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from app import create_app
from app.models import db, DailyStats, DiaryEntry, Goal, PointsLog
from app.models.points_log import PointsSourceType
from app.models.goal import GoalStatus


def backfill_points_log():
    """Backfill PointsLog entries from existing data."""
    
    print("Starting PointsLog backfill...")
    
    # Get all daily stats with points
    all_stats = DailyStats.query.filter(DailyStats.points > 0).order_by(DailyStats.date).all()
    
    print(f"Found {len(all_stats)} daily stats entries with points")
    
    backfilled_count = 0
    
    for stats in all_stats:
        user_id = stats.user_id
        date = stats.date
        total_points = stats.points
        
        print(f"Processing {user_id} on {date} with {total_points} points...")
        
        # Check if we already have log entries for this user/date
        existing_entries = PointsLog.query.filter_by(user_id=user_id, date=date).all()
        if existing_entries:
            existing_total = sum(entry.points for entry in existing_entries)
            print(f"  Already has {len(existing_entries)} log entries totaling {existing_total} points - skipping")
            continue
        
        # Track points accounted for
        points_accounted = 0
        
        # 1. Add diary entry points for this date
        diary_entries = DiaryEntry.query.filter_by(user_id=user_id, entry_date=date).all()
        for entry in diary_entries:
            if entry.rating == 1:
                points = 5
                description = "Encouraged Behavior Diary"
            else:  # rating == -1
                points = 2
                description = "Growth Opportunity Diary"
            
            log_entry = PointsLog.create_entry(
                user_id=user_id,
                points=points,
                source_type=PointsSourceType.DIARY_ENTRY,
                description=description,
                date=date,
                source_id=entry.id
            )
            points_accounted += points
            print(f"  Added diary entry: {points} points")
        
        # 2. Add goal completion/failure points for this date
        # Note: Since we don't have completed_at timestamps, we'll estimate based on goals
        # that were likely completed/failed around this date
        goals = Goal.query.filter_by(user_id=user_id).all()
        for goal in goals:
            # Check if goal time period overlaps with this date and has final status
            if (goal.status in [GoalStatus.COMPLETED, GoalStatus.FAILED] and
                goal.week_start <= date <= goal.week_end):
                
                if goal.status == GoalStatus.COMPLETED:
                    points = 10
                    description = f"Goal Completed: '{goal.title}'"
                    source_type = PointsSourceType.GOAL_COMPLETED
                else:  # FAILED
                    points = 1
                    description = f"Goal Failed: '{goal.title}'"
                    source_type = PointsSourceType.GOAL_FAILED
                
                # Only add if we haven't already accounted for all points
                if points_accounted + points <= total_points:
                    log_entry = PointsLog.create_entry(
                        user_id=user_id,
                        points=points,
                        source_type=source_type,
                        description=description,
                        date=date,
                        source_id=goal.id
                    )
                    points_accounted += points
                    print(f"  Added goal {goal.status.value}: {points} points")
        
        # 3. Add daily login bonus for remaining points
        remaining_points = total_points - points_accounted
        if remaining_points > 0:
            # Assume remaining points come from daily login bonus(es)
            for _ in range(remaining_points):
                log_entry = PointsLog.create_entry(
                    user_id=user_id,
                    points=1,
                    source_type=PointsSourceType.DAILY_LOGIN,
                    description="Daily Login Bonus",
                    date=date
                )
            print(f"  Added {remaining_points} login bonus points")
            points_accounted += remaining_points
        
        if points_accounted == total_points:
            print(f"  ✓ Successfully backfilled {points_accounted} points")
        else:
            print(f"  ⚠ Point mismatch: accounted {points_accounted}, expected {total_points}")
        
        backfilled_count += 1
    
    # Commit all changes
    db.session.commit()
    
    print(f"\nBackfill complete! Processed {backfilled_count} daily stats entries.")
    
    # Verify the backfill
    total_log_entries = PointsLog.query.count()
    print(f"Total PointsLog entries in database: {total_log_entries}")


def verify_consistency():
    """Verify that PointsLog totals match DailyStats totals."""
    
    print("\nVerifying data consistency...")
    
    # Get all users with both DailyStats and PointsLog entries
    users_with_stats = db.session.query(DailyStats.user_id).distinct().all()
    users_with_logs = db.session.query(PointsLog.user_id).distinct().all()
    
    inconsistencies = 0
    
    for (user_id,) in users_with_stats:
        # Get all dates with DailyStats for this user
        daily_stats = DailyStats.query.filter_by(user_id=user_id).all()
        
        for stats in daily_stats:
            if stats.points == 0:
                continue
                
            # Calculate total from PointsLog for this date
            log_total = PointsLog.get_daily_total(user_id, stats.date)
            
            if log_total != stats.points:
                print(f"  INCONSISTENCY: User {user_id} on {stats.date}: "
                      f"DailyStats={stats.points}, PointsLog={log_total}")
                inconsistencies += 1
    
    if inconsistencies == 0:
        print("✓ All data is consistent between DailyStats and PointsLog")
    else:
        print(f"⚠ Found {inconsistencies} inconsistencies")


if __name__ == "__main__":
    app = create_app()
    
    with app.app_context():
        print("PointsLog Backfill Script")
        print("========================")
        
        # Check if we already have data
        existing_count = PointsLog.query.count()
        if existing_count > 0:
            response = input(f"PointsLog already has {existing_count} entries. Continue? (y/N): ")
            if response.lower() != 'y':
                print("Aborted.")
                sys.exit(0)
        
        try:
            backfill_points_log()
            verify_consistency()
            print("\n✓ Backfill completed successfully!")
            
        except Exception as e:
            print(f"\n✗ Error during backfill: {e}")
            db.session.rollback()
            sys.exit(1)