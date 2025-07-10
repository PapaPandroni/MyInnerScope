# tests/test_models/ Directory

This directory contains unit tests for SQLAlchemy database models in the "Aim for the Stars" application.

## Test Files

### `test_user.py` - User Model Tests
- **Purpose**: Comprehensive testing of the User model
- **Coverage**: User creation, authentication, data validation, relationships

## Model Testing Categories

### User Model Tests

#### User Creation and Validation
- **Valid user creation**: Users created with proper email and password
- **Email validation**: Email format requirements and uniqueness constraints
- **Password handling**: Password hashing and verification
- **Username validation**: Optional username field validation

#### Authentication Tests
- **Password hashing**: Passwords automatically hashed on assignment
- **Password verification**: `check_password()` method validation
- **Security**: Passwords never stored in plaintext
- **Double hashing prevention**: Avoid hashing already hashed passwords

#### Relationship Tests
- **Diary entries**: User one-to-many relationship with DiaryEntry
- **Daily stats**: User one-to-many relationship with DailyStats  
- **Goals**: User one-to-many relationship with Goal
- **Cascade behavior**: Proper deletion cascading

### Model Validation Tests

#### Data Integrity
- **Required fields**: Email and password fields are required
- **Unique constraints**: Email addresses must be unique
- **Field lengths**: Appropriate field length restrictions
- **Data types**: Correct data types for all fields

#### Business Logic
- **Email normalization**: Email addresses handled consistently
- **Password policies**: Password complexity requirements
- **User preferences**: User settings and preferences handling
- **Account status**: Active/inactive user states

### Database Operations

#### CRUD Operations
- **Create**: User creation with valid data
- **Read**: User retrieval by ID and email
- **Update**: User profile and settings updates
- **Delete**: User deletion and cascade effects

#### Query Testing
- **Find by email**: Efficient user lookup by email
- **Authentication queries**: Login-related database queries
- **Relationship loading**: Efficient loading of related data
- **Performance**: Query optimization and N+1 prevention

## Future Model Tests

### DiaryEntry Model Tests (To Be Added)
- **Entry creation**: Valid diary entry creation
- **Rating system**: Behavior rating validation (-1, +1)
- **Date handling**: Entry date validation and defaults
- **Content validation**: Entry content requirements
- **User association**: Proper user-entry relationships

### DailyStats Model Tests (To Be Added)
- **Statistics calculation**: Daily point totals and streaks
- **Date uniqueness**: One stats record per user per day
- **Streak logic**: Current and longest streak calculations
- **Aggregation**: Statistics derived from diary entries

### Goal Model Tests (To Be Added)
- **Goal creation**: Valid goal creation with all fields
- **Target dates**: Future date validation for goals
- **Status management**: Goal status transitions
- **Progress tracking**: Goal completion percentage
- **Points targets**: Goal points target validation

## Testing Patterns

### Model Instance Testing
```python
def test_user_creation(app):
    """Test creating a new user with valid data"""
    with app.app_context():
        user = User(email='test@example.com', password='password123')
        db.session.add(user)
        db.session.commit()
        
        assert user.id is not None
        assert user.email == 'test@example.com'
        assert user.password != 'password123'  # Should be hashed
```

### Validation Testing
```python
def test_user_email_validation(app):
    """Test user email validation rules"""
    with app.app_context():
        # Valid email should work
        user = User(email='valid@example.com', password='password')
        assert user.email == 'valid@example.com'
        
        # Invalid email should raise error
        with pytest.raises(ValidationError):
            user = User(email='invalid-email', password='password')
```

### Relationship Testing
```python
def test_user_diary_relationship(app, sample_user):
    """Test user-diary entry relationship"""
    with app.app_context():
        entry = DiaryEntry(user_id=sample_user.id, content='Test entry')
        db.session.add(entry)
        db.session.commit()
        
        assert entry in sample_user.diary_entries
        assert entry.user == sample_user
```

## Database Testing Infrastructure

### Test Database Setup
- **Isolated database**: Each test uses clean database state
- **Transaction rollback**: Tests rolled back after completion
- **Fixture data**: Consistent test data through fixtures
- **Performance**: In-memory SQLite for speed

### Test Data Management
- **Factories**: Generate test data with realistic values
- **Fixtures**: Reusable test data objects
- **Cleanup**: Automatic cleanup after each test
- **Relationships**: Proper handling of related test data

### Migration Testing
- **Schema consistency**: Database schema matches model definitions
- **Migration execution**: Database migrations run successfully
- **Data preservation**: Existing data preserved during migrations
- **Rollback capability**: Migrations can be rolled back safely

## Security Testing

### Authentication Security
- **Password storage**: Passwords properly hashed and salted
- **Timing attacks**: Consistent timing for authentication attempts
- **Session security**: Secure session handling for authenticated users
- **Account lockout**: Protection against brute force attacks

### Data Protection
- **Access control**: Users can only access their own data
- **Input validation**: All model inputs properly validated
- **SQL injection**: Parameterized queries prevent injection
- **Data sanitization**: User input properly sanitized

## Performance Testing

### Query Performance
- **Index usage**: Database queries use appropriate indexes
- **N+1 prevention**: Efficient loading of related data
- **Batch operations**: Efficient bulk operations
- **Connection pooling**: Proper database connection management

### Memory Usage
- **Object creation**: Efficient model object creation
- **Garbage collection**: Proper cleanup of model objects
- **Large datasets**: Handling of large result sets
- **Caching**: Appropriate caching of frequently accessed data

## Development Workflow

### Adding Model Tests
1. **Create model**: Define new SQLAlchemy model class
2. **Write tests**: Create comprehensive tests for all model functionality
3. **Test relationships**: Verify relationships with other models
4. **Security review**: Ensure proper validation and security measures
5. **Performance check**: Verify query performance and optimization

### Model Test Maintenance
- **Regular review**: Periodically review model validation rules
- **Migration testing**: Test model changes with database migrations
- **Performance monitoring**: Monitor query performance and optimize
- **Security updates**: Update tests when security requirements change

### Debugging Model Issues
1. **Reproduce issue**: Create test that reproduces the problem
2. **Check constraints**: Verify database constraints are correct
3. **Review relationships**: Ensure model relationships are properly defined
4. **Test validation**: Verify validation rules work as expected
5. **Fix and test**: Implement fix and verify with comprehensive tests