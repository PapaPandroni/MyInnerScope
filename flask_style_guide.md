# Flask Application Style Guide

## Table of Contents
1. [Project Structure](#project-structure)
2. [Python Code Style](#python-code-style)
3. [HTML Style](#html-style)
4. [CSS Style](#css-style)
5. [JavaScript Style](#javascript-style)
6. [Bootstrap Usage](#bootstrap-usage)
7. [File Organization](#file-organization)
8. [Naming Conventions](#naming-conventions)
9. [Documentation Standards](#documentation-standards)
10. [Testing Guidelines](#testing-guidelines)

## Project Structure

### Recommended Directory Layout
```
your_flask_app/
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── product.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth/
│   │   │   ├── __init__.py
│   │   │   ├── routes.py
│   │   │   └── helpers.py
│   │   ├── dashboard/
│   │   │   ├── __init__.py
│   │   │   ├── routes.py
│   │   │   └── helpers.py
│   │   └── api/
│   │       ├── __init__.py
│   │       ├── routes.py
│   │       └── helpers.py
│   ├── templates/
│   │   ├── base.html
│   │   ├── auth/
│   │   │   ├── login.html
│   │   │   └── register.html
│   │   └── dashboard/
│   │       └── index.html
│   ├── static/
│   │   ├── css/
│   │   │   ├── main.css
│   │   │   ├── auth.css
│   │   │   └── dashboard.css
│   │   ├── js/
│   │   │   ├── main.js
│   │   │   ├── auth.js
│   │   │   └── dashboard.js
│   │   └── img/
│   └── utils/
│       ├── __init__.py
│       ├── decorators.py
│       ├── validators.py
│       └── email_service.py
├── tests/
├── migrations/
├── requirements.txt
├── .env
├── .gitignore
└── run.py
```

## Python Code Style

### General Guidelines
- Follow PEP 8 standards
- Use snake_case for all variables, functions, and module names
- Use UPPER_SNAKE_CASE for constants
- Maximum line length: 88 characters (Black formatter standard)
- Use type hints where possible

### Function Definitions
```python
# Good
def calculate_user_score(user_id: int, include_bonus: bool = False) -> float:
    """Calculate the total score for a user.
    
    Args:
        user_id: The ID of the user
        include_bonus: Whether to include bonus points
        
    Returns:
        The calculated score as a float
    """
    pass

# Bad
def calculateUserScore(userId, includeBonus=False):
    pass
```

### Class Definitions
```python
# Good
class UserProfileManager:
    """Manages user profile operations."""
    
    def __init__(self, database_connection: Database):
        self.db = database_connection
        self._cache = {}
    
    def get_user_profile(self, user_id: int) -> dict:
        """Retrieve user profile by ID."""
        pass

# Bad
class userProfileManager:
    pass
```

### Route-Specific Helper Organization
Each route module should have its own helper file:

```python
# app/routes/auth/helpers.py
def validate_login_credentials(email: str, password: str) -> bool:
    """Validate user login credentials."""
    pass

def generate_password_reset_token(user_id: int) -> str:
    """Generate a secure password reset token."""
    pass

# app/routes/auth/routes.py
from flask import Blueprint, request, render_template
from .helpers import validate_login_credentials, generate_password_reset_token

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        if validate_login_credentials(email, password):
            # Handle successful login
            pass
    
    return render_template('auth/login.html')
```

### Error Handling
```python
# Good
def get_user_by_id(user_id: int) -> dict:
    try:
        user = User.query.get(user_id)
        if not user:
            raise ValueError(f"User with ID {user_id} not found")
        return user.to_dict()
    except SQLAlchemyError as e:
        logger.error(f"Database error retrieving user {user_id}: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error retrieving user {user_id}: {e}")
        raise
```

## HTML Style

### Template Structure
- Use semantic HTML5 elements
- Maintain consistent indentation (2 spaces)
- Use snake_case for custom attributes and IDs
- Include proper meta tags and accessibility attributes

```html
<!-- Good -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}My Flask App{% endblock %}</title>
    <link href="{{ url_for('static', filename='css/main.css') }}" rel="stylesheet">
</head>
<body>
    <header class="main-header">
        <nav class="navbar navbar-expand-lg" id="main_navigation">
            <!-- Navigation content -->
        </nav>
    </header>
    
    <main class="main-content">
        {% block content %}{% endblock %}
    </main>
    
    <footer class="main-footer">
        <!-- Footer content -->
    </footer>
    
    <script src="{{ url_for('static', filename='js/main.js') }}"></script>
    {% block scripts %}{% endblock %}
</body>
</html>
```

### Form Guidelines
```html
<form method="POST" class="user-form" id="login_form">
    {{ csrf_token() }}
    
    <div class="form-group">
        <label for="email_input" class="form-label">Email Address</label>
        <input 
            type="email" 
            id="email_input" 
            name="email" 
            class="form-control"
            required
            aria-describedby="email_help"
        >
        <small id="email_help" class="form-text text-muted">
            We'll never share your email with anyone else.
        </small>
    </div>
    
    <button type="submit" class="btn btn-primary">Sign In</button>
</form>
```

## CSS Style

### Organization and Structure
- Use BEM methodology for class naming when not using Bootstrap
- Organize CSS by component/page
- Use CSS custom properties for theming
- Mobile-first responsive design

```css
/* Good - Component-based organization */
/* === USER PROFILE COMPONENT === */
.user-profile {
    --profile-bg-color: #ffffff;
    --profile-border-color: #e0e0e0;
    
    background-color: var(--profile-bg-color);
    border: 1px solid var(--profile-border-color);
    border-radius: 8px;
    padding: 1.5rem;
}

.user-profile__avatar {
    width: 80px;
    height: 80px;
    border-radius: 50%;
    object-fit: cover;
}

.user-profile__name {
    font-size: 1.25rem;
    font-weight: 600;
    margin-bottom: 0.5rem;
}

.user-profile__email {
    color: #6c757d;
    font-size: 0.875rem;
}

/* === RESPONSIVE DESIGN === */
@media (max-width: 768px) {
    .user-profile {
        padding: 1rem;
    }
    
    .user-profile__avatar {
        width: 60px;
        height: 60px;
    }
}
```

### Custom Properties
```css
:root {
    /* Color Palette */
    --primary-color: #007bff;
    --secondary-color: #6c757d;
    --success-color: #28a745;
    --danger-color: #dc3545;
    --warning-color: #ffc107;
    
    /* Typography */
    --font-family-base: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    --font-size-base: 1rem;
    --line-height-base: 1.5;
    
    /* Spacing */
    --spacing-xs: 0.25rem;
    --spacing-sm: 0.5rem;
    --spacing-md: 1rem;
    --spacing-lg: 1.5rem;
    --spacing-xl: 3rem;
}
```

## JavaScript Style

### General Guidelines
- Use snake_case for variables and functions
- Use UPPER_SNAKE_CASE for constants
- Use ES6+ features (arrow functions, const/let, template literals)
- Organize code into modules by functionality

```javascript
// Good
const USER_API_ENDPOINT = '/api/users';

const user_manager = {
    current_user: null,
    
    init() {
        this.bind_events();
        this.load_current_user();
    },
    
    bind_events() {
        document.addEventListener('DOMContentLoaded', () => {
            const login_form = document.getElementById('login_form');
            if (login_form) {
                login_form.addEventListener('submit', this.handle_login_submit.bind(this));
            }
        });
    },
    
    async handle_login_submit(event) {
        event.preventDefault();
        
        const form_data = new FormData(event.target);
        const login_data = {
            email: form_data.get('email'),
            password: form_data.get('password')
        };
        
        try {
            const response = await this.submit_login(login_data);
            if (response.success) {
                window.location.href = '/dashboard';
            } else {
                this.show_error_message(response.message);
            }
        } catch (error) {
            console.error('Login error:', error);
            this.show_error_message('An unexpected error occurred');
        }
    },
    
    async submit_login(credentials) {
        const response = await fetch('/auth/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': this.get_csrf_token()
            },
            body: JSON.stringify(credentials)
        });
        
        return await response.json();
    },
    
    get_csrf_token() {
        return document.querySelector('meta[name="csrf-token"]')?.getAttribute('content');
    },
    
    show_error_message(message) {
        const alert_container = document.getElementById('alert_container');
        if (alert_container) {
            alert_container.innerHTML = `
                <div class="alert alert-danger alert-dismissible fade show" role="alert">
                    ${message}
                    <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                </div>
            `;
        }
    }
};

// Initialize when DOM is ready
user_manager.init();
```

## Bootstrap Usage

### Custom Bootstrap Integration
- Use Bootstrap's utility classes where appropriate
- Override Bootstrap variables with custom CSS properties
- Maintain consistency with Bootstrap's naming conventions for custom components

```css
/* Custom Bootstrap theme */
:root {
    --bs-primary: #007bff;
    --bs-secondary: #6c757d;
    --bs-font-family-base: var(--font-family-base);
}

/* Custom component that integrates with Bootstrap */
.custom-card {
    @extend .card;
    --card-bg: var(--bs-light);
    background-color: var(--card-bg);
}

.custom-card__header {
    @extend .card-header;
    font-weight: 600;
}

.custom-card__body {
    @extend .card-body;
}
```

## File Organization

### Route Module Structure
Each route should be self-contained with its own helpers:

```python
# app/routes/dashboard/__init__.py
from .routes import dashboard_bp

# app/routes/dashboard/routes.py
from flask import Blueprint, render_template, request
from .helpers import get_dashboard_data, calculate_user_stats

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')

@dashboard_bp.route('/')
def index():
    user_id = session.get('user_id')
    dashboard_data = get_dashboard_data(user_id)
    user_stats = calculate_user_stats(user_id)
    
    return render_template('dashboard/index.html', 
                         data=dashboard_data, 
                         stats=user_stats)

# app/routes/dashboard/helpers.py
def get_dashboard_data(user_id: int) -> dict:
    """Get all dashboard data for a user."""
    pass

def calculate_user_stats(user_id: int) -> dict:
    """Calculate statistics for dashboard display."""
    pass
```

### Static File Organization
- Group CSS and JS files by feature/route
- Use consistent naming patterns
- Include a main file for global styles/scripts

```
static/
├── css/
│   ├── main.css          # Global styles
│   ├── auth.css          # Authentication pages
│   ├── dashboard.css     # Dashboard specific
│   └── components.css    # Reusable components
├── js/
│   ├── main.js           # Global JavaScript
│   ├── auth.js           # Authentication functionality
│   ├── dashboard.js      # Dashboard functionality
│   └── utils.js          # Utility functions
└── img/
    ├── icons/
    ├── backgrounds/
    └── user-uploads/
```

## Naming Conventions

### Files and Directories
- Use snake_case for all file and directory names
- Use descriptive names that indicate purpose
- Group related files in directories

### Variables and Functions
- Python: snake_case
- JavaScript: snake_case
- CSS: kebab-case for classes, snake_case for IDs
- HTML: snake_case for IDs and custom attributes

### Database
- Table names: snake_case, plural (e.g., `user_profiles`)
- Column names: snake_case (e.g., `created_at`, `user_id`)
- Foreign keys: `{table_name}_id` (e.g., `user_id`)

## Documentation Standards

### Python Docstrings
Use Google-style docstrings:

```python
def process_user_data(user_id: int, include_history: bool = False) -> dict:
    """Process and return user data with optional history.
    
    Args:
        user_id: The unique identifier for the user
        include_history: Whether to include user's action history
        
    Returns:
        A dictionary containing processed user data
        
    Raises:
        ValueError: If user_id is invalid
        DatabaseError: If database operation fails
    """
    pass
```

### Code Comments
- Use comments sparingly, prefer self-documenting code
- Explain why, not what
- Update comments when code changes

```python
# Good
# Calculate tax using the current year's rates (rates change annually)
tax_amount = calculate_tax(income, current_year_rates)

# Bad
# Calculate tax
tax_amount = calculate_tax(income, rates)
```

## Testing Guidelines

### Test Organization
```
tests/
├── unit/
│   ├── test_auth_helpers.py
│   ├── test_dashboard_helpers.py
│   └── test_models.py
├── integration/
│   ├── test_auth_routes.py
│   └── test_dashboard_routes.py
└── fixtures/
    ├── sample_data.py
    └── test_users.py
```

### Test Naming
```python
class TestAuthHelpers:
    def test_validate_login_credentials_with_valid_data_returns_true(self):
        """Test that valid credentials return True."""
        pass
    
    def test_validate_login_credentials_with_invalid_email_returns_false(self):
        """Test that invalid email returns False."""
        pass
    
    def test_generate_password_reset_token_returns_valid_token(self):
        """Test that password reset token generation works correctly."""
        pass
```

---

## Quick Reference Checklist

### Before Committing Code
- [ ] All functions have type hints and docstrings
- [ ] Variable names use snake_case
- [ ] Files are organized in appropriate directories
- [ ] CSS follows BEM methodology or Bootstrap conventions
- [ ] JavaScript uses snake_case naming
- [ ] HTML includes proper semantic elements and accessibility attributes
- [ ] Tests are written for new functionality
- [ ] Comments explain complex logic
- [ ] No hardcoded values (use configuration)
- [ ] Error handling is implemented

### File Naming Quick Guide
- Python files: `user_profile.py`
- HTML templates: `user_profile.html` 
- CSS files: `user-profile.css`
- JavaScript files: `user_profile.js`
- Directories: `user_profiles/`