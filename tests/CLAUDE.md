# tests/ Directory

This directory contains comprehensive tests for the "Aim for the Stars" Flask application using pytest framework.

## Test Structure

```
tests/
├── README.md               # Detailed testing documentation  
├── __init__.py            # Makes tests a Python package
├── conftest.py            # Test configuration and fixtures
├── test_basic.py          # Basic functionality tests
├── test_csrf.py           # CSRF protection tests
├── test_migrations.py     # Database migration tests
├── test_security.py       # Security feature tests
├── test_forms/            # Form validation tests
├── test_models/           # Database model tests
├── test_routes/           # Web route/endpoint tests
└── test_utils/            # Utility function tests
```

## Core Test Files

### `conftest.py` - Test Configuration
- **Purpose**: Test fixtures and configuration shared across all tests
- **Fixtures**:
  - `app`: Flask application instance with test configuration
  - `client`: Test client for HTTP requests
  - `sample_user`: Pre-created user for testing
  - `sample_diary_entry`: Pre-created diary entry
  - `sample_goal`: Pre-created goal
  - `sample_daily_stats`: Pre-created daily statistics
- **Utilities**: CSRF token extraction, database setup/teardown

### `test_basic.py` - Fundamental Tests
- **Purpose**: Basic application functionality and configuration tests
- **Coverage**: 
  - Application creation and initialization
  - Database table creation
  - Basic route accessibility
  - Configuration validation

### `test_csrf.py` - CSRF Protection Tests
- **Purpose**: Verify CSRF protection is working correctly
- **Coverage**:
  - CSRF token generation and validation
  - Form submission with/without valid tokens
  - AJAX request CSRF protection
  - Security bypass prevention

### `test_migrations.py` - Database Migration Tests
- **Purpose**: Ensure database migrations work correctly
- **Coverage**:
  - Migration execution
  - Schema consistency
  - Data integrity during migrations
  - Rollback functionality

### `test_security.py` - Security Feature Tests
- **Purpose**: Comprehensive security testing
- **Coverage**:
  - Authentication and authorization
  - Rate limiting functionality
  - Session management
  - Input validation and sanitization

## Test Categories

### Unit Tests (`test_models/`, `test_utils/`)
- **Scope**: Individual functions and classes in isolation
- **Data**: Mock data and test fixtures
- **Speed**: Fast execution for quick feedback
- **Purpose**: Verify individual component behavior

### Integration Tests (`test_routes/`)
- **Scope**: Multiple components working together
- **Data**: Test database with real relationships
- **Speed**: Moderate execution time
- **Purpose**: Verify component interactions

### Functional Tests (`test_forms/`)
- **Scope**: End-to-end user workflows
- **Data**: Complete user scenarios
- **Speed**: Slower but comprehensive
- **Purpose**: Verify user experience flows

## Testing Infrastructure

### Test Database
- **Isolation**: Each test uses temporary SQLite database
- **Cleanup**: Automatic database cleanup after each test
- **No side effects**: Tests don't affect main application database
- **Performance**: In-memory database for speed

### Fixtures and Setup
- **Reusable data**: Common test data created through fixtures
- **Dependency injection**: Fixtures provide dependencies to tests
- **Scope control**: Different fixture scopes (function, class, session)
- **Teardown**: Automatic cleanup of test resources

### Test Configuration
- **Environment**: Separate test configuration from development/production
- **Settings**: Test-specific settings for optimal testing
- **Security**: Disabled security features that interfere with testing
- **Performance**: Optimized for test execution speed

## Test Coverage Areas

### Authentication and Authorization
- User registration and login flows
- Password hashing and validation
- Session management and timeout
- Permission and access control

### Database Operations
- Model creation and validation
- Relationship handling
- Query performance and correctness
- Data integrity constraints

### Web Interface
- Route accessibility and responses
- Form validation and submission
- Error handling and user feedback
- Template rendering and context

### Business Logic
- **Points system**: PointsLog and PointsService transaction integrity
- **Dual tracking**: PointsLog (detailed) and DailyStats (cache) consistency
- Streak calculation and maintenance
- Goal progress tracking with points integration
- Statistics aggregation and API endpoints

## Running Tests

### Basic Commands
```bash
pytest                          # Run all tests
pytest -v                       # Verbose output
pytest tests/test_models/       # Run specific test directory
pytest --cov=app                # Run with coverage
```

### Test Filtering
```bash
pytest -m "not slow"            # Skip slow tests
pytest -m "unit"                # Run only unit tests
pytest -m "integration"         # Run only integration tests
pytest -k "test_user"           # Run tests matching pattern
pytest tests/test_basic.py::test_app_creation  # Run specific test
```

### Debug Mode
```bash
pytest -v -s --pdb             # Drop into debugger on failure
pytest --lf                    # Run only last failed tests
```

## Development Practices

### Test-Driven Development
1. **Write test first**: Define expected behavior through tests
2. **Implement feature**: Write minimal code to pass tests
3. **Refactor**: Improve code while maintaining test coverage
4. **Repeat**: Continue cycle for new features

### Test Quality
- **Descriptive names**: Test names clearly describe what is being tested
- **Single responsibility**: Each test verifies one specific behavior
- **Independent tests**: Tests don't depend on other tests
- **Realistic data**: Test data represents real-world scenarios

### Continuous Integration
- **Automated testing**: Tests run automatically on code changes
- **Coverage requirements**: Maintain minimum test coverage levels
- **Performance monitoring**: Track test execution time
- **Failure notifications**: Alert developers to test failures

## Maintenance and Updates

### Adding New Tests
1. **Identify testing needs**: Determine what needs testing for new features
2. **Choose test type**: Unit, integration, or functional test
3. **Create test file**: Follow naming conventions and organization
4. **Use fixtures**: Leverage existing fixtures where possible
5. **Document**: Update test documentation for significant additions

### Test Refactoring
- **DRY principle**: Remove duplicate test code
- **Fixture optimization**: Improve fixture efficiency and reusability
- **Performance improvement**: Optimize slow tests
- **Coverage gaps**: Identify and fill testing gaps

### Debugging Failed Tests
1. **Reproduce locally**: Run failing tests in development environment
2. **Check test data**: Verify test fixtures and data setup
3. **Review changes**: Look for recent code changes affecting tests
4. **Debug tools**: Use pytest debugging features and logging
5. **Fix and verify**: Correct issues and verify fix with additional testing