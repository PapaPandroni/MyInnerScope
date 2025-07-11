#!/usr/bin/env python3
"""
Enhanced Data Integrity Analysis and Recovery System
"""

import sys
import os
from datetime import datetime, date

# Add the app directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from app import create_app
from app.models import db, User, DailyStats, DiaryEntry, Goal, PointsLog
from app.models.goal import GoalStatus
from app.models.points_log import PointsSourceType


def analyze_data_integrity():
    """Comprehensive analysis of data integrity across all users."""
    
    print("=== COMPREHENSIVE DATA INTEGRITY ANALYSIS ===\n")
    
    # Get all users
    users = User.query.all()
    print(f"Total users: {len(users)}")
    
    # Analyze each user's data consistency
    inconsistencies = []
    missing_entries_details = []
    
    for user in users:
        print(f"\nAnalyzing user {user.id} ({user.email})...")
        
        # Get all daily stats for this user
        daily_stats = DailyStats.query.filter_by(user_id=user.id).filter(DailyStats.points > 0).all()
        
        for stats in daily_stats:
            # Get PointsLog total for this date
            log_entries = PointsLog.query.filter_by(user_id=user.id, date=stats.date).all()
            log_total = sum(entry.points for entry in log_entries)
            
            if log_total != stats.points:
                print(f"  ⚠ Inconsistency on {stats.date}: DailyStats={stats.points}, PointsLog={log_total}")
                
                # Analyze what's missing
                diary_entries = DiaryEntry.query.filter_by(user_id=user.id, entry_date=stats.date).all()
                goals = Goal.query.filter_by(user_id=user.id).filter(
                    Goal.week_start <= stats.date,
                    Goal.week_end >= stats.date,
                    Goal.status.in_([GoalStatus.COMPLETED, GoalStatus.FAILED])
                ).all()
                
                expected_diary_points = sum(5 if entry.rating == 1 else 2 for entry in diary_entries)
                expected_goal_points = sum(10 if goal.status == GoalStatus.COMPLETED else 1 for goal in goals)
                expected_total = expected_diary_points + expected_goal_points
                
                # Estimate login bonuses
                remaining_points = stats.points - expected_total
                estimated_login_bonuses = max(0, remaining_points)
                
                inconsistencies.append({
                    'user_id': user.id,
                    'date': stats.date,
                    'daily_stats': stats.points,
                    'points_log': log_total,
                    'difference': stats.points - log_total,
                    'diary_entries': len(diary_entries),
                    'expected_diary_points': expected_diary_points,
                    'goals': len(goals),
                    'expected_goal_points': expected_goal_points,
                    'estimated_login_bonuses': estimated_login_bonuses
                })
    
    # Summary
    daily_stats_with_points = DailyStats.query.filter(DailyStats.points > 0).count()
    total_log_entries = PointsLog.query.count()
    
    print(f"\n=== SUMMARY ===")
    print(f"Total daily stats with points: {daily_stats_with_points}")
    print(f"Total PointsLog entries: {total_log_entries}")
    print(f"Data inconsistencies found: {len(inconsistencies)}")
    
    if inconsistencies:
        print(f"\nINCONSISTENCIES DETAILS:")
        for inc in inconsistencies:
            print(f"  User {inc['user_id']} on {inc['date']}:")
            print(f"    DailyStats: {inc['daily_stats']} points")
            print(f"    PointsLog: {inc['points_log']} points") 
            print(f"    Missing: {inc['difference']} points")
            print(f"    Analysis: {inc['diary_entries']} diary entries ({inc['expected_diary_points']} pts), "
                  f"{inc['goals']} goals ({inc['expected_goal_points']} pts), "
                  f"~{inc['estimated_login_bonuses']} login bonuses")
            print()
    else:
        print("✓ Perfect data consistency!")
    
    return inconsistencies


def create_missing_entries(inconsistencies):
    """Create missing PointsLog entries to fix inconsistencies."""
    
    if not inconsistencies:
        print("No inconsistencies to fix!")
        return
    
    print(f"\n=== CREATING MISSING ENTRIES ===")
    print(f"Fixing {len(inconsistencies)} inconsistencies...")
    
    total_created = 0
    
    for inc in inconsistencies:
        user_id = inc['user_id']
        target_date = inc['date']
        missing_points = inc['difference']
        
        print(f"\nFixing User {user_id} on {target_date} (missing {missing_points} points)...")
        
        # Get existing PointsLog entries to avoid duplicates
        existing_entries = PointsLog.query.filter_by(user_id=user_id, date=target_date).all()
        existing_diary_ids = {e.source_id for e in existing_entries if e.source_type == PointsSourceType.DIARY_ENTRY}
        existing_goal_ids = {e.source_id for e in existing_entries if e.source_type in [PointsSourceType.GOAL_COMPLETED, PointsSourceType.GOAL_FAILED]}
        
        points_created = 0
        
        # 1. Add missing diary entries
        diary_entries = DiaryEntry.query.filter_by(user_id=user_id, entry_date=target_date).all()
        for entry in diary_entries:
            if entry.id not in existing_diary_ids:
                points = 5 if entry.rating == 1 else 2
                description = "Encouraged Behavior Diary" if entry.rating == 1 else "Growth Opportunity Diary"
                
                log_entry = PointsLog.create_entry(
                    user_id=user_id,
                    points=points,
                    source_type=PointsSourceType.DIARY_ENTRY,
                    description=description,
                    date=target_date,
                    source_id=entry.id
                )
                points_created += points
                total_created += 1
                print(f"  ✓ Added diary entry: {points} points")
        
        # 2. Add missing goal entries
        goals = Goal.query.filter_by(user_id=user_id).filter(
            Goal.week_start <= target_date,
            Goal.week_end >= target_date,
            Goal.status.in_([GoalStatus.COMPLETED, GoalStatus.FAILED])
        ).all()
        
        for goal in goals:
            if goal.id not in existing_goal_ids:
                if goal.status == GoalStatus.COMPLETED:
                    points = 10
                    source_type = PointsSourceType.GOAL_COMPLETED
                    description = f"Goal Completed: '{goal.title}'"
                else:
                    points = 1
                    source_type = PointsSourceType.GOAL_FAILED
                    description = f"Goal Failed: '{goal.title}'"
                
                log_entry = PointsLog.create_entry(
                    user_id=user_id,
                    points=points,
                    source_type=source_type,
                    description=description,
                    date=target_date,
                    source_id=goal.id
                )
                points_created += points
                total_created += 1
                print(f"  ✓ Added goal entry: {points} points")
        
        # 3. Add remaining points as login bonuses
        remaining_points = missing_points - points_created
        if remaining_points > 0:
            for i in range(remaining_points):
                log_entry = PointsLog.create_entry(
                    user_id=user_id,
                    points=1,
                    source_type=PointsSourceType.DAILY_LOGIN,
                    description="Daily Login Bonus",
                    date=target_date
                )
                total_created += 1
            print(f"  ✓ Added {remaining_points} login bonus points")
            points_created += remaining_points
        
        print(f"  ✅ Created {points_created} points for user {user_id}")
    
    # Commit all changes
    db.session.commit()
    print(f"\n✅ Recovery complete! Created {total_created} PointsLog entries.")


if __name__ == "__main__":
    app = create_app()
    
    with app.app_context():
        print("Enhanced Data Integrity Check and Recovery")
        print("=========================================")
        
        try:
            # Step 1: Analyze current state
            inconsistencies = analyze_data_integrity()
            
            # Step 2: Offer to fix inconsistencies
            if inconsistencies:
                response = input(f"\nFound {len(inconsistencies)} inconsistencies. Fix them? (y/N): ")
                if response.lower() == 'y':
                    create_missing_entries(inconsistencies)
                    
                    # Step 3: Verify fix
                    print("\n=== VERIFICATION ===")
                    final_inconsistencies = analyze_data_integrity()
                    
                    if not final_inconsistencies:
                        print("🎉 ALL DATA INCONSISTENCIES RESOLVED!")
                    else:
                        print(f"⚠ {len(final_inconsistencies)} inconsistencies remain")
                else:
                    print("Skipped fixing inconsistencies.")
            
            print("\n✅ Data integrity check completed!")
            
        except Exception as e:
            print(f"\n❌ Error during analysis: {e}")
            db.session.rollback()
            sys.exit(1)