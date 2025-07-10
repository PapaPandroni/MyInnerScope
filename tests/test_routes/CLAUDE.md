# tests/test_routes/ Directory

This directory contains integration tests for Flask routes and endpoints in the "Aim for the Stars" application.

## Test Files

### `test_auth.py` - Authentication Route Tests
- **Purpose**: Test user authentication, registration, and session management
- **Coverage**: Login, logout, registration, session handling

### `test_diary.py` - Diary Route Tests
- **Purpose**: Test diary entry creation, editing, and management
- **Coverage**: Entry CRUD operations, rating system, entry validation

### `test_progress.py` - Progress Route Tests
- **Purpose**: Test progress tracking and statistics visualization
- **Coverage**: Progress dashboard, statistics display, chart data

### `test_user.py` - User Management Route Tests
- **Purpose**: Test user settings, profile management, account operations
- **Coverage**: Settings updates, profile changes, account deletion

## Route Testing Categories

### Authentication Routes (`test_auth.py`)

#### Registration Testing
- **Valid registration**: Successful user account creation
- **Email validation**: Unique email requirement enforcement
- **Password requirements**: Password strength and confirmation
- **Form validation**: Registration form validation and error handling
- **Redirect behavior**: Proper redirect after successful registration

#### Login Testing
- **Valid credentials**: Successful login with correct email/password
- **Invalid credentials**: Rejection of incorrect credentials
- **Account states**: Handling of active/inactive accounts
- **Session creation**: Proper session establishment after login
- **CSRF protection**: Login form CSRF token validation

#### Logout Testing
- **Session termination**: Proper session cleanup on logout
- **Redirect behavior**: Appropriate redirect after logout
- **Security**: Prevention of session fixation attacks
- **Multiple sessions**: Handling of multiple browser sessions

### Diary Routes (`test_diary.py`)

#### Entry Creation
- **Valid entries**: Successful diary entry creation
- **Rating system**: Proper handling of behavior ratings (+1, -1)
- **Content validation**: Entry content length and format validation
- **Date handling**: Entry date assignment and validation
- **User association**: Entries properly associated with authenticated user

#### Entry Management
- **Edit entries**: Updating existing diary entries
- **Delete entries**: Removing diary entries with proper confirmation
- **View entries**: Displaying entries with proper formatting
- **Access control**: Users can only access their own entries
- **Pagination**: Proper pagination for large numbers of entries

#### Points System
- **Point calculation**: Correct points assigned based on ratings
- **Daily aggregation**: Proper daily statistics calculation
- **Streak calculation**: Current and longest streak maintenance
- **Statistics updates**: Real-time statistics updates after entry changes

### Progress Routes (`test_progress.py`)

#### Dashboard Display
- **Statistics rendering**: Proper display of user statistics
- **Chart data**: Correct data formatting for Chart.js
- **Date filtering**: Progress data filtering by date ranges
- **Performance**: Efficient loading of progress data
- **Responsive design**: Progress display works on all device sizes

#### Analytics Features
- **Trend analysis**: Progress trends over time
- **Goal progress**: Integration with goal tracking
- **Comparative statistics**: Current vs. historical performance
- **Export functionality**: Data export in various formats
- **Real-time updates**: Live updates as new entries are added

### User Routes (`test_user.py`)

#### Profile Management
- **Settings updates**: User profile and preference changes
- **Email changes**: Email address update with validation
- **Password changes**: Secure password update process
- **Display preferences**: User interface customization options

#### Account Operations
- **Account deletion**: Secure account deletion with confirmation
- **Data export**: User data export before deletion
- **Privacy settings**: User privacy and data sharing preferences
- **Account recovery**: Password reset and account recovery

## Testing Patterns

### Route Access Testing
```python
def test_protected_route_requires_login(client):
    """Test that protected routes require authentication"""
    response = client.get('/protected-route')
    assert response.status_code == 302  # Redirect to login
    assert '/login' in response.location

def test_authenticated_route_access(client, logged_in_user):
    """Test that authenticated users can access protected routes"""
    response = client.get('/protected-route')
    assert response.status_code == 200
```

### Form Submission Testing
```python
def test_form_submission_with_csrf(client, csrf_token):
    """Test form submission with valid CSRF token"""
    response = client.post('/form-route', data={
        'field': 'value',
        'csrf_token': csrf_token
    })
    assert response.status_code == 302  # Successful redirect
```

### JSON API Testing
```python
def test_api_endpoint_returns_json(client, logged_in_user):
    """Test API endpoint returns proper JSON response"""
    response = client.get('/api/data')
    assert response.status_code == 200
    assert response.content_type == 'application/json'
    data = response.get_json()
    assert 'expected_field' in data
```

## HTTP Status Code Testing

### Success Responses
- **200 OK**: Successful GET requests and page displays
- **201 Created**: Successful resource creation
- **204 No Content**: Successful DELETE operations
- **302 Found**: Proper redirects after form submissions

### Client Error Responses
- **400 Bad Request**: Invalid form data or malformed requests
- **401 Unauthorized**: Authentication required responses
- **403 Forbidden**: Access denied for insufficient permissions
- **404 Not Found**: Non-existent resources and pages
- **422 Unprocessable Entity**: Form validation failures

### Server Error Responses
- **500 Internal Server Error**: Proper error handling for server issues

## Security Testing

### Authentication and Authorization
- **Session management**: Proper session creation and destruction
- **Access control**: Route protection and permission enforcement
- **CSRF protection**: All forms include and validate CSRF tokens
- **Rate limiting**: Route rate limiting functionality

### Input Validation
- **XSS prevention**: User input properly escaped in templates
- **SQL injection**: Parameterized queries prevent injection attacks
- **File upload security**: Secure handling of file uploads
- **Input sanitization**: All user input properly sanitized

### Session Security
- **Session hijacking**: Protection against session hijacking
- **Session fixation**: Prevention of session fixation attacks
- **Timeout handling**: Proper session timeout and renewal
- **Cross-origin protection**: CORS and CSRF protection

## Performance Testing

### Response Times
- **Page load times**: Routes respond within acceptable time limits
- **Database queries**: Efficient database query execution
- **Template rendering**: Fast template rendering and caching
- **Static asset loading**: Optimized static asset delivery

### Scalability Testing
- **Concurrent users**: Routes handle multiple simultaneous users
- **Large datasets**: Performance with large amounts of user data
- **Memory usage**: Efficient memory usage during request processing
- **Resource cleanup**: Proper cleanup of resources after requests

## Error Handling Testing

### Application Errors
- **Database errors**: Graceful handling of database connection issues
- **Validation errors**: Proper display of form validation errors
- **Server errors**: Appropriate error pages for server issues
- **Network errors**: Handling of network connectivity problems

### User Experience
- **Error messages**: Clear, helpful error messages for users
- **Error recovery**: Ways for users to recover from errors
- **Logging**: Proper error logging for debugging
- **Monitoring**: Error tracking and monitoring integration

## Development Workflow

### Adding Route Tests
1. **Create route**: Implement new Flask route in appropriate blueprint
2. **Write tests**: Create comprehensive tests for all route functionality
3. **Test authentication**: Verify proper authentication and authorization
4. **Security review**: Ensure CSRF protection and input validation
5. **Performance check**: Verify route performance and optimization

### Route Test Maintenance
- **Regular review**: Periodically review route functionality and tests
- **Security updates**: Update tests when security requirements change
- **Performance monitoring**: Monitor route performance and optimize
- **User feedback**: Incorporate user experience feedback into tests

### Debugging Route Issues
1. **Reproduce issue**: Create test that reproduces the problem
2. **Check routing**: Verify URL routing and blueprint registration
3. **Review templates**: Ensure templates render correctly
4. **Test authentication**: Verify authentication and session handling
5. **Fix and test**: Implement fix and verify with comprehensive tests