"""Add PointsLog table for detailed point tracking (CLEAN VERSION)

Revision ID: bb3c496b0bdc
Revises: 1d01d06679e8
Create Date: 2025-07-11 22:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bb3c496b0bdc'
down_revision = '1d01d06679e8'
branch_labels = None
depends_on = None


def upgrade():
    # ### Clean PointsLog table creation ###
    
    # Get database connection for verification
    connection = op.get_bind()
    
    # Check if PointsLog table already exists
    result = connection.execute(sa.text(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='points_log'"
    )).fetchone()
    
    if result:
        print("ℹ PointsLog table already exists, skipping creation")
    else:
        # Create PointsLog table with enum type for SQLite compatibility
        op.create_table('points_log',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('user_id', sa.Integer(), nullable=False),
            sa.Column('date', sa.Date(), nullable=False),
            sa.Column('points', sa.Integer(), nullable=False),
            sa.Column('source_type', sa.String(20), nullable=False),  # Using String instead of Enum for SQLite
            sa.Column('source_id', sa.Integer(), nullable=True),
            sa.Column('description', sa.Text(), nullable=False),
            sa.Column('created_at', sa.DateTime(), nullable=True),
            sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
            sa.PrimaryKeyConstraint('id')
        )
        print("✓ Created PointsLog table")
    
    # Verify the table was created/exists and is accessible
    try:
        result = connection.execute(sa.text("SELECT COUNT(*) FROM points_log")).fetchone()
        print(f"✓ PointsLog table verified - contains {result[0]} entries")
    except Exception as e:
        raise Exception(f"PointsLog table verification failed: {e}")
    
    print("✓ PointsLog migration completed successfully")
    
    # ### end clean PointsLog creation ###


def downgrade():
    # ### Clean PointsLog table removal ###
    
    # Get database connection for verification
    connection = op.get_bind()
    
    # Check if table exists before trying to drop
    result = connection.execute(sa.text(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='points_log'"
    )).fetchone()
    
    if result:
        # Get count for logging
        count_result = connection.execute(sa.text("SELECT COUNT(*) FROM points_log")).fetchone()
        entry_count = count_result[0] if count_result else 0
        
        print(f"⚠ Dropping PointsLog table with {entry_count} entries")
        op.drop_table('points_log')
        print("✓ PointsLog table dropped")
    else:
        print("ℹ PointsLog table does not exist, nothing to drop")
    
    # ### end clean PointsLog removal ###