"""Add performance indexes for user_id and date columns

Revision ID: 1d01d06679e8
Revises: 033faf89f4e5
Create Date: 2025-07-11 16:25:49.435286

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect


# revision identifiers, used by Alembic.
revision = '1d01d06679e8'
down_revision = '033faf89f4e5'
branch_labels = None
depends_on = None


def upgrade():
    # ### Bulletproof index creation with proper error handling ###
    
    # Get database connection for raw SQL operations
    connection = op.get_bind()
    
    # Define index creation statements with IF NOT EXISTS for SQLite safety
    index_statements = [
        # User ID indexes for foreign key queries
        "CREATE INDEX IF NOT EXISTS idx_diary_entry_user_id ON diary_entry (user_id)",
        "CREATE INDEX IF NOT EXISTS idx_daily_stats_user_id ON daily_stats (user_id)", 
        "CREATE INDEX IF NOT EXISTS idx_goals_user_id ON goals (user_id)",
        
        # Date indexes for temporal queries
        "CREATE INDEX IF NOT EXISTS idx_diary_entry_entry_date ON diary_entry (entry_date)",
        "CREATE INDEX IF NOT EXISTS idx_daily_stats_date ON daily_stats (date)",
        "CREATE INDEX IF NOT EXISTS idx_goals_week_start ON goals (week_start)",
        "CREATE INDEX IF NOT EXISTS idx_goals_week_end ON goals (week_end)",
        
        # Composite indexes for common query patterns
        "CREATE INDEX IF NOT EXISTS idx_diary_entry_user_date ON diary_entry (user_id, entry_date)",
        "CREATE INDEX IF NOT EXISTS idx_daily_stats_user_date ON daily_stats (user_id, date)",
        "CREATE INDEX IF NOT EXISTS idx_goals_user_status ON goals (user_id, status)",
        
        # Rating index for filtering
        "CREATE INDEX IF NOT EXISTS idx_diary_entry_rating ON diary_entry (rating)"
    ]
    
    # Execute each index creation with error handling
    created_indexes = []
    for statement in index_statements:
        try:
            connection.execute(sa.text(statement))
            index_name = statement.split('idx_')[1].split(' ON')[0]
            created_indexes.append(f"idx_{index_name}")
            print(f"✓ Created index: idx_{index_name}")
        except Exception as e:
            index_name = statement.split('idx_')[1].split(' ON')[0] if 'idx_' in statement else 'unknown'
            print(f"⚠ Failed to create index idx_{index_name}: {e}")
            # Continue with other indexes rather than failing completely
    
    # Verify indexes were created using database-agnostic inspector
    inspector = inspect(connection)
    
    # Get indexes for each table and filter for our idx_ prefixed indexes
    all_indexes = []
    tables = ['diary_entry', 'daily_stats', 'goals']
    
    for table in tables:
        try:
            table_indexes = inspector.get_indexes(table)
            for idx in table_indexes:
                if idx['name'] and idx['name'].startswith('idx_'):
                    all_indexes.append(idx['name'])
        except Exception as e:
            print(f"⚠ Could not verify indexes for table {table}: {e}")
    
    actual_indexes = sorted(all_indexes)
    print(f"✓ Migration completed. Created indexes: {actual_indexes}")
    
    # Ensure we created at least the critical indexes
    critical_indexes = ['idx_diary_entry_user_id', 'idx_daily_stats_user_id', 'idx_goals_user_id']
    missing_critical = [idx for idx in critical_indexes if idx not in actual_indexes]
    
    if missing_critical:
        raise Exception(f"Critical indexes failed to create: {missing_critical}")
    
    print("✓ All critical indexes verified successfully")
    
    # ### end bulletproof index creation ###


def downgrade():
    # ### Bulletproof index removal with proper error handling ###
    
    # Get database connection for raw SQL operations
    connection = op.get_bind()
    
    # Define indexes to remove (in reverse order of creation)
    indexes_to_drop = [
        'idx_diary_entry_rating',
        'idx_goals_user_status', 
        'idx_daily_stats_user_date',
        'idx_diary_entry_user_date',
        'idx_goals_week_end',
        'idx_goals_week_start', 
        'idx_daily_stats_date',
        'idx_diary_entry_entry_date',
        'idx_goals_user_id',
        'idx_daily_stats_user_id',
        'idx_diary_entry_user_id'
    ]
    
    # Check which indexes actually exist before trying to drop
    result = connection.execute(sa.text(
        "SELECT name FROM sqlite_master WHERE type='index' AND name LIKE 'idx_%'"
    )).fetchall()
    existing_indexes = [row[0] for row in result]
    
    # Drop each index with error handling
    dropped_indexes = []
    for index_name in indexes_to_drop:
        if index_name in existing_indexes:
            try:
                connection.execute(sa.text(f"DROP INDEX IF EXISTS {index_name}"))
                dropped_indexes.append(index_name)
                print(f"✓ Dropped index: {index_name}")
            except Exception as e:
                print(f"⚠ Failed to drop index {index_name}: {e}")
        else:
            print(f"ℹ Index {index_name} did not exist, skipping")
    
    print(f"✓ Downgrade completed. Dropped indexes: {dropped_indexes}")
    
    # ### end bulletproof index removal ###
