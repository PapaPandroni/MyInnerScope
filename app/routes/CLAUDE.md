# app/routes/ Directory

This directory contains Flask Blueprint-based route handlers for the "My Inner Scope" application.

## Blueprint Architecture

All routes are organized as Flask Blueprints for modularity and maintainability. Each blueprint handles a specific domain of functionality.

### Route Files

#### `auth.py` - Authentication Blueprint (`auth_bp`)
- **Purpose**: User registration, login, logout with points integration
- **Rate Limits**: 20 per minute, 60 per hour
- **Key Routes**:
  - `/register` - User registration form and processing
  - `/login` - User authentication with daily login bonus
  - `/logout` - Session termination
- **Security**: Password hashing, session management, CSRF protection
- **Points Integration**: Automatic daily login bonus via PointsService

#### `diary.py` - Diary Management Blueprint (`diary_bp`)
- **Purpose**: Diary entry creation, editing, and management
- **Rate Limits**: 30 per minute, 120 per hour
- **Key Routes**:
  - `/diary` - Main diary interface
  - `/entry/new` - Create new diary entry
  - `/entry/<id>/edit` - Edit existing entry
  - `/entry/<id>/delete` - Delete entry
- **Features**: Behavior rating system, points calculation

#### `progress.py` - Progress Tracking Blueprint (`progress_bp`)
- **Purpose**: User progress visualization and statistics with clickable analytics
- **Rate Limits**: 20 per minute, 60 per hour
- **Key Routes**:
  - `/progress` - Main progress dashboard with interactive cards
  - `/stats/daily` - Daily statistics view
  - `/analytics` - Advanced analytics
- **Features**: 
  - Clickable progress cards with detailed point breakdowns
  - Chart.js integration with interactive data points
  - Integration with PointsService for detailed transaction history

#### `goals.py` - Goal Management Blueprint (`goals_bp`)
- **Purpose**: Goal setting, tracking, and management
- **Rate Limits**: 30 per minute, 120 per hour
- **Key Routes**:
  - `/goals` - Goal dashboard
  - `/goals/new` - Create new goal
  - `/goals/<id>/edit` - Edit goal
  - `/goals/<id>/complete` - Mark goal as completed

#### `reader.py` - Content Reading Blueprint (`reader_bp`)
- **Purpose**: Diary entry reading and enhanced search functionality
- **Rate Limits**: 60 per minute, 300 per hour (higher for read operations)
- **Key Routes**:
  - `/read` - Read diary entries with filtering
  - `/search` - Advanced search functionality
- **Features**: 
  - Combined date + rating filters
  - Pagination, search snippets
  - Enhanced search helpers integration

#### `user.py` - User Management Blueprint (`user_bp`)
- **Purpose**: User settings, profile management, account actions
- **Rate Limits**: 20 per minute, 60 per hour
- **Key Routes**:
  - `/settings` - User settings page
  - `/profile` - User profile management
  - `/delete-account` - Account deletion

#### `legal.py` - Legal Pages Blueprint (`legal_bp`)
- **Purpose**: Privacy policy, terms of service, legal compliance
- **Key Routes**:
  - `/privacy` - Privacy policy
  - `/terms` - Terms of service
  - `/cookies` - Cookie policy
- **Features**: Cookie consent management

#### `main.py` - Main Application Blueprint (`main_bp`) ⭐ **ENHANCED**
- **Purpose**: Home page, about page, general application routes, SEO infrastructure
- **Key Routes**:
  - `/` - Home page
  - `/about` - About page
  - `/donate` - Donation page
  - `/robots.txt` - Search engine crawler guidance
  - `/sitemap.xml` - XML sitemap generation for search engines
- **SEO Features**: 
  - Dynamic sitemap generation with page priorities
  - Robots.txt with public/private area distinction
  - Search engine optimization support

#### `api.py` - API Blueprint (`api_bp`) ⭐ **NEW**
- **Purpose**: RESTful API endpoints for frontend-backend communication
- **Rate Limits**: 60 per minute, 300 per hour
- **Key Routes**:
  - `/api/points-breakdown` - Get detailed points breakdown for specific dates
  - `/api/stats/daily` - Daily statistics API endpoint
  - **Content Type**: Returns JSON responses for AJAX requests
- **Features**: Integration with PointsService, detailed transaction history

## Blueprint Registration

### `__init__.py`
- Contains `register_blueprints(app)` function
- Registers all blueprints with the Flask application
- Applies rate limiting to each blueprint with appropriate limits
- **Rate Limiting Strategy**:
  - Auth operations: Conservative limits (security-sensitive)
  - Read operations: Higher limits (less resource-intensive)
  - Write operations: Moderate limits (balance usability/security)

## Common Patterns

### Security Implementation
- **CSRF Protection**: All forms include CSRF tokens
- **Authentication Required**: Protected routes check `session['user_id']`
- **Rate Limiting**: Applied per blueprint based on operation type
- **Input Validation**: Flask-WTF forms validate all user input

### Error Handling
- Consistent error message patterns
- Proper HTTP status codes
- User-friendly error pages (handled in templates/errors/)
- Logging for debugging and monitoring

### Database Operations
- Session management with proper commit/rollback
- Optimized queries with appropriate joins
- Pagination for large result sets
- Transaction handling for data integrity

## Points System Integration

### Route-Level Points Management
- **Authentication**: Login bonus handled in `auth.py:login_page()`
- **Diary Entries**: Point awards in diary creation/editing routes
- **Goals**: Point awards for goal completion/failure
- **API Endpoints**: Points breakdown and statistics via API blueprint

### Database Compatibility Patterns
- **Enum Handling**: Use `.value` when querying PointsSourceType in filters
- **Query Safety**: Handle both enum objects and string values for database compatibility
- **Transaction Integrity**: All point awards go through PointsService

## Development Notes

- **Import Pattern**: Routes import models, forms, and services as needed
- **Response Types**: Mix of rendered templates and JSON responses (API blueprint)
- **URL Structure**: RESTful design with API endpoints for AJAX
- **Template Context**: Consistent data passed including user session info
- **Points Integration**: All point-earning activities use centralized PointsService