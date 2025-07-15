# Testing Framework for My Inner Scope

This directory contains comprehensive tests for the My Inner Scope application.

## 🏗️ **Test Structure**

```
tests/
├── __init__.py                      # Makes tests a Python package
├── conftest.py                      # Test configuration and fixtures
├── test_basic.py                    # Basic functionality tests
├── test_seo.py                      # SEO implementation tests
├── test_legal_compliance.py         # Legal document compliance tests
├── test_analytics_integration.py    # Analytics infrastructure tests
├── test_seo_integration_summary.py  # Core SEO/compliance summary tests
├── test_models/                     # Database model tests
│   ├── __init__.py
│   └── test_user.py                 # User model tests
├── test_routes/                     # Web route tests
│   ├── __init__.py
│   └── test_auth.py                 # Authentication route tests
├── test_utils/                      # Utility function tests
│   ├── __init__.py
│   └── test_goal_helpers.py         # Goal helper function tests
└── test_forms/                      # Form validation tests
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

# SEO and compliance tests only
python3 -m pytest tests/test_seo_integration_summary.py -v

# All SEO-related tests
python3 -m pytest tests/test_seo.py tests/test_legal_compliance.py tests/test_analytics_integration.py -v

# Legal compliance tests only
python3 -m pytest tests/test_legal_compliance.py -v
```

### Run with coverage:
```bash
python3 -m pytest tests/ --cov=app --cov-report=html
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

### 4. **SEO & Compliance Tests** (`test_seo.py`, `test_legal_compliance.py`, `test_analytics_integration.py`)
- Test SEO meta tags, structured data, robots.txt, sitemap.xml
- Test legal document compliance and privacy disclosures
- Test analytics infrastructure and GDPR compliance
- Test favicon accessibility and social media integration

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
- ✅ SEO meta tags and structured data
- ✅ robots.txt and sitemap.xml functionality
- ✅ Legal document compliance
- ✅ Analytics infrastructure and GDPR compliance
- ✅ Favicon and social media integration

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

### For SEO/Compliance:
1. Add tests to existing SEO files or create new specific test files
2. Use `client` fixture for HTTP requests to test pages
3. Use BeautifulSoup for HTML parsing and validation
4. Test both positive cases (elements present) and negative cases (security)

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