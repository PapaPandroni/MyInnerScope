# migrations/ Directory

This directory contains Flask-Migrate (Alembic) database migration files for the "Aim for the Stars" application.

## Migration Structure

```
migrations/
├── README                  # Migration documentation
├── alembic.ini            # Alembic configuration file
├── env.py                 # Migration environment configuration
├── script.py.mako         # Template for new migration scripts
└── versions/              # Individual migration version files
```

## Core Migration Files

### `alembic.ini` - Configuration
- **Purpose**: Alembic configuration settings
- **Contents**: Database connection settings, logging configuration
- **Integration**: Configured to work with Flask application factory

### `env.py` - Environment Setup
- **Purpose**: Migration environment initialization and configuration
- **Features**:
  - Flask application context setup
  - Database connection management
  - Migration context configuration
  - Target metadata configuration

### `script.py.mako` - Migration Template
- **Purpose**: Template for generating new migration files
- **Contents**: Standard migration file structure and imports
- **Usage**: Used by `flask db migrate` command to create new migrations

### `README` - Documentation
- **Purpose**: Basic documentation for using Flask-Migrate
- **Contents**: Common migration commands and workflow instructions

## Migration Versions (`versions/`)

### Current Migrations

#### `1a2b3c4d5e6f_create_initial_tables.py`
- **Purpose**: Initial database schema creation
- **Tables Created**: Users, diary_entries, daily_stats, goals
- **Features**: Base table structure with primary keys and basic relationships

#### `bc311ce7dcf8_increase_password_column_length.py`
- **Purpose**: Increase password column length for better security
- **Changes**: Expanded password field to accommodate longer hashes
- **Reason**: Support for stronger password hashing algorithms

#### `033faf89f4e5_rename_tables_to_snake_case_plural.py`
- **Purpose**: Standardize table naming convention
- **Changes**: Renamed tables to use snake_case plural naming
- **Benefits**: Consistent naming across database schema

## Migration Management

### Creating New Migrations
```bash
flask db migrate -m "descriptive message"  # Generate new migration
flask db upgrade                           # Apply migrations
flask db downgrade                         # Rollback migrations
```

### Migration Workflow
1. **Model changes**: Modify SQLAlchemy models in `app/models/`
2. **Generate migration**: Use `flask db migrate` to create migration file
3. **Review migration**: Manually review generated migration for accuracy
4. **Test migration**: Test migration in development environment
5. **Apply migration**: Use `flask db upgrade` to apply changes

### Migration Best Practices
- **Descriptive messages**: Use clear, descriptive migration messages
- **Review before applying**: Always review auto-generated migrations
- **Backup before major changes**: Backup database before destructive migrations
- **Test rollbacks**: Ensure migrations can be rolled back if needed

## Migration Types

### Schema Migrations
- **Table creation**: Creating new database tables
- **Column additions**: Adding new columns to existing tables
- **Column modifications**: Changing column types or constraints
- **Index creation**: Adding database indexes for performance

### Data Migrations
- **Data transformation**: Converting existing data to new formats
- **Data population**: Populating new fields with calculated values
- **Data cleanup**: Removing obsolete or inconsistent data
- **Reference updates**: Updating foreign key relationships

### Constraint Migrations
- **Foreign keys**: Adding or modifying foreign key constraints
- **Unique constraints**: Adding uniqueness requirements
- **Check constraints**: Adding data validation constraints
- **Index constraints**: Modifying index definitions

## Environment Considerations

### Development Environment
- **SQLite database**: Uses local SQLite for development
- **Fast migrations**: Quick migration execution for development
- **Frequent changes**: Support for frequent schema iterations
- **Reset capability**: Easy database reset when needed

### Production Environment
- **PostgreSQL database**: Uses PostgreSQL for production
- **Careful migrations**: More cautious migration approach
- **Backup requirements**: Mandatory backups before migrations
- **Rollback planning**: Always have rollback strategy

### Testing Environment
- **In-memory database**: Uses in-memory SQLite for testing
- **Clean state**: Fresh database for each test run
- **Migration validation**: Automated testing of migration scripts
- **Schema consistency**: Verify schema matches model definitions

## Migration Safety

### Pre-Migration Checks
- **Database backup**: Always backup production data
- **Migration review**: Manually review auto-generated migrations
- **Development testing**: Test migrations in development environment
- **Rollback plan**: Prepare rollback strategy before applying

### Common Migration Issues
- **Data loss prevention**: Avoid migrations that could cause data loss
- **Performance impact**: Consider performance impact of large migrations
- **Dependency management**: Handle migration dependencies correctly
- **Naming conflicts**: Avoid naming conflicts in migration files

### Rollback Strategy
- **Downgrade capability**: Ensure migrations can be rolled back
- **Data preservation**: Rollbacks should preserve important data
- **Quick recovery**: Fast rollback for critical production issues
- **Testing rollbacks**: Test rollback procedures in development

## Monitoring and Maintenance

### Migration Tracking
- **Version control**: All migrations committed to version control
- **Migration history**: Track applied migrations in database
- **Documentation**: Document significant migrations and their purposes
- **Change log**: Maintain changelog of schema changes

### Performance Monitoring
- **Migration timing**: Monitor time required for migrations
- **Database impact**: Monitor database performance during migrations
- **Resource usage**: Track resource usage during large migrations
- **Index performance**: Monitor index performance after changes

### Maintenance Tasks
- **Schema cleanup**: Periodically review and clean up schema
- **Migration consolidation**: Consolidate migrations when appropriate
- **Performance optimization**: Optimize database schema for performance
- **Documentation updates**: Keep migration documentation current

## Development Workflow

### Adding Database Changes
1. **Model modification**: Update SQLAlchemy models
2. **Generate migration**: Create migration with `flask db migrate`
3. **Review changes**: Manually review generated migration script
4. **Test locally**: Apply migration in development environment
5. **Test application**: Verify application works with schema changes
6. **Commit migration**: Add migration file to version control

### Deployment Process
1. **Backup database**: Create production database backup
2. **Deploy code**: Deploy application code with new migrations
3. **Apply migrations**: Run `flask db upgrade` in production
4. **Verify deployment**: Ensure application works correctly
5. **Monitor performance**: Watch for any performance issues

### Troubleshooting Migrations
1. **Check error logs**: Review migration error messages
2. **Verify syntax**: Check migration script syntax
3. **Check dependencies**: Ensure migration dependencies are correct
4. **Test rollback**: Verify rollback works if needed
5. **Seek help**: Consult team or documentation for complex issues