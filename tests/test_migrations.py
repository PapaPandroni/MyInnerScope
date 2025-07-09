import pytest
import os
import tempfile
from alembic.config import Config
from alembic import command
from sqlalchemy import create_engine, inspect
from app import create_app
from app.models import db

@pytest.fixture
def migration_app():
    """Fixture for a test app with a temp file SQLite DB and migrations setup."""
    # Create a temp file for the SQLite DB
    db_fd, db_path = tempfile.mkstemp(suffix='.db')
    os.close(db_fd)  # We only need the path
    
    # Set up the test app configuration
    os.environ['FLASK_ENV'] = 'testing'
    app = create_app('testing')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False

    yield app, db_path

    # Clean up temp DB file
    if os.path.exists(db_path):
        os.remove(db_path)

def run_alembic_command(app, db_path, command_name, *args):
    """Helper to run Alembic commands with correct config."""
    with app.app_context():
        migrations_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'migrations')
        migrations_dir = os.path.abspath(migrations_dir)
        alembic_ini_path = os.path.join(migrations_dir, 'alembic.ini')
        alembic_cfg = Config(alembic_ini_path)
        alembic_cfg.set_main_option('script_location', migrations_dir)
        alembic_cfg.set_main_option('sqlalchemy.url', f'sqlite:///{db_path}')
        if command_name == 'upgrade':
            command.upgrade(alembic_cfg, *args)
        elif command_name == 'downgrade':
            command.downgrade(alembic_cfg, *args)

def test_migrations(migration_app):
    """Test database migrations with Alembic."""
    app, db_path = migration_app
    print(f"[TEST] Using temp DB path: {db_path}")
    # Upgrade to the latest revision
    run_alembic_command(app, db_path, 'upgrade', 'head')

    # Verify tables exist
    engine = create_engine(f'sqlite:///{db_path}')
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    assert 'alembic_version' in tables
    assert 'users' in tables  # Updated to reflect new table name
    assert 'diary_entry' in tables
    assert 'daily_stats' in tables
    assert 'goals' in tables  # Updated to reflect new table name

    # Downgrade to base
    run_alembic_command(app, db_path, 'downgrade', 'base')

    # Verify tables are gone (except alembic_version)
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    assert 'alembic_version' in tables
    assert 'user' not in tables
    assert 'diary_entry' not in tables
    assert 'daily_stats' not in tables
    assert 'goal' not in tables