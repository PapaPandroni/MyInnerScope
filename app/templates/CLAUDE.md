# app/templates/ Directory

This directory contains Jinja2 HTML templates for the "Aim for the Stars" Flask application.

## Template Architecture

### Template Structure
- **base.html**: Master template with common layout and includes
- **_navbar.html**: Reusable navigation component
- **Feature templates**: Individual pages for each application feature
- **errors/**: Error page templates (403, 404, 500)

## Core Templates

### Layout Templates

#### `base.html` - Master Template
- **Purpose**: Base layout template extended by all other templates
- **Features**:
  - HTML document structure
  - Bootstrap 5 CSS/JS includes
  - Common meta tags and SEO elements
  - Flash message display system
  - CSRF token meta tag for JavaScript
  - Common JavaScript includes

#### `_navbar.html` - Navigation Component
- **Purpose**: Reusable navigation bar included in base template
- **Features**:
  - Responsive navigation menu
  - User authentication state awareness
  - Dynamic menu items based on user status
  - Mobile-friendly hamburger menu

### Main Application Templates

#### `index.html` - Home Page
- **Purpose**: Application landing page and dashboard
- **Features**: Welcome content, recent activity, quick actions

#### `about.html` - About Page
- **Purpose**: Information about the application and its purpose
- **Features**: Application description, feature overview

#### `login.html` & `register.html` - Authentication
- **Purpose**: User authentication and registration forms
- **Features**: Flask-WTF form integration, validation display, CSRF protection

#### `diary.html` - Diary Management
- **Purpose**: Main diary interface for creating and managing entries
- **Features**: Entry forms, rating system, entry display

#### `read_diary.html` - Diary Reading
- **Purpose**: Read and search through diary entries
- **Features**: Entry display, search functionality, pagination

#### `progress.html` - Progress Dashboard
- **Purpose**: User progress visualization and statistics
- **Features**: Chart.js integration, statistics display, progress tracking

#### `goals.html` - Goal Management
- **Purpose**: Goal creation, editing, and tracking interface
- **Features**: Goal forms, progress displays, goal management

#### `settings.html` - User Settings
- **Purpose**: User profile and account settings
- **Features**: Profile editing, account management, preferences

### Legal and Information Templates

#### `privacy.html` - Privacy Policy
- **Purpose**: Privacy policy and data handling information
- **Features**: Legal compliance content, cookie information

#### `terms.html` - Terms of Service
- **Purpose**: Terms of service and usage agreements
- **Features**: Legal terms and conditions

#### `donate.html` - Donation Page
- **Purpose**: Support and donation information
- **Features**: Donation options and support information

#### `delete_account_confirm.html` - Account Deletion
- **Purpose**: Account deletion confirmation and process
- **Features**: Confirmation form, data deletion information

## Template Features

### Jinja2 Integration
- **Template inheritance**: All templates extend base.html
- **Block system**: Organized content blocks (title, content, scripts)
- **Include system**: Reusable components via include
- **Context variables**: Access to Flask context and user data

### Bootstrap 5 Integration
- **Responsive design**: Mobile-first responsive layouts
- **Component library**: Bootstrap components for consistent UI
- **Grid system**: Responsive grid layouts
- **Utility classes**: Bootstrap utility classes for styling

### Form Integration
- **Flask-WTF**: Integrated form handling with CSRF protection
- **Validation display**: Automatic error message display
- **Form rendering**: Consistent form styling and structure
- **Field types**: Support for various input types and widgets

### JavaScript Integration
- **Data attributes**: Pass server data to JavaScript via data attributes
- **Event handling**: JavaScript enhancements for forms and interactions
- **AJAX support**: Templates structured to support AJAX updates
- **Progressive enhancement**: Core functionality works without JavaScript

## Development Patterns

### Template Inheritance
```html
{% extends "base.html" %}
{% block title %}Page Title{% endblock %}
{% block content %}
<!-- Page content -->
{% endblock %}
```

### Include Pattern
```html
{% include "_navbar.html" %}
```

### Context Usage
- **current_user**: User object available in all templates
- **url_for()**: Flask URL generation
- **config**: Access to application configuration
- **flash messages**: Automatic display of flash messages

### Error Handling
- **Custom error pages**: 403, 404, 500 error templates
- **User-friendly messages**: Clear error explanations
- **Navigation preservation**: Error pages maintain site navigation

## Security Considerations

### CSRF Protection
- **Meta tag**: CSRF token available to JavaScript
- **Form integration**: All forms include CSRF tokens
- **AJAX requests**: JavaScript includes CSRF tokens in requests

### Content Security
- **Input escaping**: Automatic HTML escaping via Jinja2
- **Safe content**: Explicit marking of safe HTML content
- **XSS prevention**: Protection against cross-site scripting

### Authentication
- **User context**: Templates respect user authentication state
- **Conditional content**: Content varies based on authentication
- **Secure areas**: Protected content requires authentication

## Accessibility

### Semantic HTML
- **Proper structure**: Logical heading hierarchy and structure
- **ARIA labels**: Accessibility labels where needed
- **Form labels**: Proper form labeling and associations

### Responsive Design
- **Mobile-first**: Templates work well on all device sizes
- **Touch-friendly**: Interactive elements sized for touch
- **Readable text**: Appropriate font sizes and contrast

## Development Workflow

### Adding New Templates
1. **Create template**: Follow naming conventions
2. **Extend base**: Use template inheritance
3. **Add blocks**: Define necessary content blocks
4. **Test responsive**: Verify across device sizes
5. **Accessibility check**: Ensure accessibility compliance