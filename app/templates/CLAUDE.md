# app/templates/ Directory

This directory contains Jinja2 HTML templates for the "Aim for the Stars" Flask application, organized by feature for better maintainability.

## Template Architecture

### Feature-Based Organization
```
templates/
├── shared/           # Shared components and base templates
│   ├── base.html     # Master template with cosmic theme
│   └── _navbar.html  # Navigation component
├── auth/            # Authentication templates
├── diary/           # Diary management templates
├── goals/           # Goal management templates
├── main/            # Landing and info pages
├── progress/        # Progress dashboard templates
├── reader/          # Diary reading and search
├── user/            # User settings and profile
├── legal/           # Privacy, terms, cookies
└── errors/          # Custom error pages (403, 404, 500)
```

## Core Templates

### Layout Templates

#### `shared/base.html` - Master Template
- **Purpose**: Base layout template extended by all other templates
- **Features**:
  - Cosmic theme with space-inspired design
  - Bootstrap 5 CSS/JS includes with custom overrides
  - Tour system integration for user onboarding
  - Flash message display system with animations
  - CSRF token meta tag for JavaScript/AJAX
  - Chart.js and feature-specific JavaScript includes
  - Mobile-responsive navigation

#### `shared/_navbar.html` - Navigation Component
- **Purpose**: Reusable navigation bar included in base template
- **Features**:
  - Cosmic-themed responsive navigation
  - User authentication state awareness
  - Dynamic menu items based on user status
  - Mobile-friendly hamburger menu
  - Tour system integration with guided highlights

### Feature-Organized Templates

#### `main/` - Landing and Information Pages
- **index.html**: Application landing page with tour system integration
- **about.html**: Application description and feature overview
- **donate.html**: Support and donation information

#### `auth/` - Authentication Templates
- **login.html**: User authentication with login bonus tracking
- **register.html**: User registration with form validation
- **Features**: Flask-WTF integration, CSRF protection, validation display

#### `diary/` - Diary Management
- **diary.html**: Main diary interface for creating and managing entries
- **Features**: Entry forms, behavior rating system, points integration

#### `reader/` - Diary Reading and Search
- **read_diary.html**: Enhanced diary reading with filtering
- **Features**: Combined date + rating filters, search functionality, pagination

#### `progress/` - Progress Dashboard ⭐ **ENHANCED**
- **progress.html**: Interactive progress visualization
- **Features**: 
  - Clickable progress cards with detailed breakdowns
  - Chart.js integration with interactive data points
  - Points breakdown modals with transaction history
  - Real-time statistics updates

#### `goals/` - Goal Management
- **goals.html**: Goal creation, editing, and tracking interface
- **Features**: Goal forms, progress displays, goal management with points integration

#### `user/` - User Settings and Profile
- **settings.html**: User profile and account settings
- **delete_account_confirm.html**: Account deletion confirmation
- **Features**: Profile editing, account management, data export options

#### `legal/` - Legal and Compliance Templates
- **privacy.html**: Privacy policy and data handling information
- **terms.html**: Terms of service and usage agreements
- **Features**: GDPR compliance, cookie consent integration

#### `errors/` - Custom Error Pages ⭐ **NEW**
- **403.html**: Forbidden access error with user-friendly messaging
- **404.html**: Page not found error with navigation options
- **500.html**: Server error with contact information
- **Features**: Consistent branding, helpful navigation, error context

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
- **API Integration**: Templates support AJAX requests to API blueprint endpoints
- **Tour System**: Interactive onboarding tour with localStorage persistence
- **Data attributes**: Pass server data to JavaScript via data attributes
- **Event handling**: Enhanced interactions for clickable progress cards
- **Chart.js Integration**: Interactive data visualizations with clickable elements
- **Progressive enhancement**: Core functionality works without JavaScript

## Development Patterns

### Template Inheritance
```html
{% extends "shared/base.html" %}
{% block title %}Page Title{% endblock %}
{% block content %}
<!-- Page content with tour integration -->
{% endblock %}
{% block scripts %}
<!-- Feature-specific JavaScript -->
{% endblock %}
```

### Include Pattern
```html
{% include "shared/_navbar.html" %}
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

## Recent Template Improvements

### User Experience Enhancements
- **Interactive Analytics**: Clickable progress cards with detailed modals
- **Tour System**: Multi-page guided onboarding for new users
- **Enhanced Navigation**: Responsive design with cosmic theme
- **Error Pages**: Custom error templates with helpful guidance

### Technical Enhancements
- **Feature Organization**: Templates organized by application feature
- **API Integration**: AJAX-ready templates for dynamic content
- **Points Integration**: Templates show detailed transaction history
- **Mobile Optimization**: Improved responsive design patterns

## Development Workflow

### Adding New Templates
1. **Choose directory**: Place in appropriate feature directory
2. **Extend base**: Use `shared/base.html` template inheritance
3. **Add tour integration**: Include tour system data attributes if needed
4. **API integration**: Structure for AJAX updates if required
5. **Test responsive**: Verify across device sizes with cosmic theme
6. **Accessibility check**: Ensure accessibility compliance