# Testing Framework for Aim for the Stars

This directory contains comprehensive tests for the Aim for the Stars application.

## 🏗️ **Test Structure**

```
tests/
├── __init__.py              # Makes tests a Python package
├── conftest.py              # Test configuration and fixtures
├── test_basic.py            # Basic functionality tests
├── test_models/             # Database model tests
│   ├── __init__.py
│   └── test_user.py         # User model tests
├── test_routes/             # Web route tests
│   ├── __init__.py
│   └── test_auth.py         # Authentication route tests
├── test_utils/              # Utility function tests
│   ├── __init__.py
│   └── test_goal_helpers.py # Goal helper function tests
└── test_forms/              # Form validation tests
    └── __init__.py
```

## 🚀 **Running Tests**

### Run all tests:
```bash
python3 -m pytest tests/ -v
```

### Run specific test categories:
```bash
# Model tests only
python3 -m pytest tests/test_models/ -v

# Route tests only
python3 -m pytest tests/test_routes/ -v

# Utility tests only
python3 -m pytest tests/test_utils/ -v
```

### Run with coverage:
```bash
python3 -m pytest tests/ --cov=web_app --cov-report=html
```

### Run specific test:
```bash
python3 -m pytest tests/test_basic.py::test_app_creation -v
```

## 🧪 **Test Types**

### 1. **Unit Tests** (`test_models/`, `test_utils/`)
- Test individual functions and classes in isolation
- Use mock data and fixtures
- Fast execution

### 2. **Integration Tests** (`test_routes/`)
- Test how components work together
- Test complete user workflows
- Use test database

### 3. **Functional Tests** (`test_forms/`)
- Test form validation and submission
- Test user interface behavior

## 🔧 **Fixtures**

The `conftest.py` file provides these fixtures:

- **`app`**: Flask application instance with test configuration
- **`client`**: Test client for making HTTP requests
- **`sample_user`**: Pre-created user for testing
- **`sample_diary_entry`**: Pre-created diary entry
- **`sample_goal`**: Pre-created goal
- **`sample_daily_stats`**: Pre-created daily stats

## 📊 **Test Coverage**

Current test coverage includes:
- ✅ Application creation and configuration
- ✅ Database table creation
- ✅ User model operations
- ✅ Basic route functionality
- ✅ Authentication routes (partial)

## 🎯 **Adding New Tests**

### For Models:
1. Create `tests/test_models/test_[model_name].py`
2. Import the model: `from models import [ModelName]`
3. Use the `app` fixture for database operations

### For Routes:
1. Create `tests/test_routes/test_[route_name].py`
2. Use the `client` fixture for HTTP requests
3. Test both GET and POST requests

### For Utils:
1. Create `tests/test_utils/test_[util_name].py`
2. Import utility functions directly
3. Test with mock data

## 🔒 **Safety Features**

- **Isolated databases**: Each test uses a temporary database
- **Automatic cleanup**: Database is dropped after each test
- **No side effects**: Tests don't affect your main database
- **Environment isolation**: Tests use separate configuration

## 📝 **Best Practices**

1. **Test names**: Use descriptive names like `test_user_creation_with_valid_data`
2. **Assertions**: Use specific assertions, not just `assert True`
3. **Fixtures**: Reuse fixtures for common test data
4. **Documentation**: Add docstrings to explain what each test does
5. **Isolation**: Each test should be independent of others

## 🚨 **Troubleshooting**

### Common Issues:
- **SQLAlchemy session errors**: Ensure you're within an app context
- **Import errors**: Make sure you're in the virtual environment
- **Database errors**: Check that test database is properly configured

### Debug Mode:
```bash
python -m pytest tests/ -v -s --pdb
```

This will drop you into a debugger on test failures. 