# migrations/versions/ Directory

This directory contains individual database migration version files for the "Aim for the Stars" application.

## Migration Files

### `1a2b3c4d5e6f_create_initial_tables.py` - Initial Schema
- **Purpose**: Creates the initial database schema for the application
- **Created Tables**:
  - `users`: User accounts with authentication
  - `diary_entries`: User diary entries with behavior ratings
  - `daily_stats`: Daily aggregated statistics and streaks
  - `goals`: User-defined goals with progress tracking
- **Relationships**: Establishes foreign key relationships between tables
- **Indexes**: Creates essential indexes for query performance

### `bc311ce7dcf8_increase_password_column_length.py` - Security Enhancement
- **Purpose**: Increases password column length for enhanced security
- **Changes**: Expanded password field from shorter length to 255 characters
- **Reason**: Support for stronger password hashing algorithms
- **Security**: Enables use of more secure hash formats like pbkdf2
- **Backward Compatibility**: Maintains compatibility with existing password hashes

### `033faf89f4e5_rename_tables_to_snake_case_plural.py` - Naming Convention
- **Purpose**: Standardizes table naming to snake_case plural convention
- **Changes**: 
  - Renamed tables to follow consistent naming patterns
  - Updated foreign key references to match new table names
  - Maintained data integrity during renaming process
- **Benefits**: Improved code consistency and database convention adherence
- **Impact**: No data loss, purely structural change

## Migration File Structure

### Standard Migration Components
Each migration file contains:
- **Revision identifiers**: Unique ID and parent revision
- **Migration metadata**: Timestamp, description, dependencies
- **Upgrade function**: Forward migration operations
- **Downgrade function**: Rollback migration operations
- **Import statements**: Required Alembic and SQLAlchemy imports

### Migration Operations
Common operations in migration files:
- **`op.create_table()`**: Create new database tables
- **`op.add_column()`**: Add columns to existing tables
- **`op.alter_column()`**: Modify existing column properties
- **`op.create_index()`**: Create database indexes
- **`op.drop_table()`**: Remove tables (in downgrade functions)

## Migration History and Dependencies

### Linear Migration Chain
```
None → 1a2b3c4d5e6f → bc311ce7dcf8 → 033faf89f4e5 → HEAD
```

### Dependency Management
- **Parent-child relationships**: Each migration specifies its parent
- **Sequential application**: Migrations applied in dependency order
- **Rollback chain**: Downgrades follow reverse dependency order
- **Conflict resolution**: Alembic prevents conflicting migrations

## Migration Content Details

### Initial Schema (`1a2b3c4d5e6f`)
```python
# Creates fundamental application tables
op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(120), nullable=False),
    sa.Column('password', sa.String(128), nullable=False),
    sa.Column('user_name', sa.String(200), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
)
```

### Security Enhancement (`bc311ce7dcf8`)
```python
# Increases password column length
op.alter_column('users', 'password',
               existing_type=sa.VARCHAR(length=128),
               type_=sa.String(length=255),
               existing_nullable=False)
```

### Naming Convention (`033faf89f4e5`)
```python
# Renames tables to standard convention
op.rename_table('user', 'users')
op.rename_table('diary_entry', 'diary_entries')
# ... additional table renames
```

## Migration Best Practices

### Writing Safe Migrations
- **Reversible operations**: All migrations should be reversible
- **Data preservation**: Never write migrations that could lose data
- **Performance consideration**: Large table modifications should be batched
- **Index management**: Consider index creation/deletion performance impact

### Testing Migrations
- **Development testing**: Test all migrations in development environment
- **Rollback testing**: Verify downgrade functions work correctly
- **Data integrity**: Ensure data remains consistent after migration
- **Performance testing**: Test migration performance with realistic data volumes

### Documentation Standards
- **Descriptive names**: Migration messages should clearly describe changes
- **Code comments**: Complex migrations should include explanatory comments
- **Change documentation**: Significant changes documented in commit messages
- **Impact assessment**: Document potential impact on application functionality

## Migration Management

### Version Control
- **Committed files**: All migration files committed to version control
- **No modification**: Never modify committed migration files
- **Branching strategy**: Handle migration conflicts in feature branches
- **Merge procedures**: Careful merge procedures for migration conflicts

### Production Deployment
- **Backup requirement**: Always backup before applying production migrations
- **Downtime planning**: Plan for potential downtime during migrations
- **Rollback preparation**: Have rollback plan ready before applying
- **Monitoring**: Monitor application during and after migration

### Development Workflow
- **Feature branches**: Create migrations in feature branches
- **Review process**: Peer review of migration files before merge
- **Testing requirement**: All migrations must pass testing before merge
- **Conflict resolution**: Handle migration file conflicts carefully

## Troubleshooting

### Common Issues
- **Migration conflicts**: Multiple migrations with same parent revision
- **Schema drift**: Development schema differs from migration-generated schema
- **Data migration failures**: Data transformation errors during migration
- **Performance issues**: Slow migrations on large tables

### Resolution Strategies
- **Conflict resolution**: Use `flask db merge` to resolve conflicts
- **Schema repair**: Use `flask db stamp` to repair schema version tracking
- **Manual intervention**: Sometimes manual database changes are needed
- **Expert consultation**: Complex issues may require database expert help

### Recovery Procedures
- **Rollback execution**: Use `flask db downgrade` to rollback problematic migrations
- **Database restoration**: Restore from backup if migrations cause critical issues
- **Schema rebuild**: Rebuild schema from scratch in extreme cases
- **Data recovery**: Recover data from backups when necessary

## Future Migration Considerations

### Upcoming Changes
- **Feature additions**: New features may require additional tables
- **Performance optimization**: Indexes and constraints for better performance
- **Data archival**: Procedures for archiving old data
- **Security enhancements**: Additional security-related schema changes

### Migration Strategy
- **Planning**: Plan complex migrations carefully
- **Testing**: Extensive testing of large or complex migrations
- **Communication**: Communicate migration plans to team
- **Documentation**: Document significant migrations for future reference