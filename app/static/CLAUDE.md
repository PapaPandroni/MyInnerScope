# app/static/ Directory

This directory contains static assets for the "Aim for the Stars" web application frontend.

## Directory Structure

```
static/
├── assets/             # Image and media files
├── css/               # Stylesheets
└── js/                # JavaScript files organized by feature
```

## Asset Organization

### `assets/` - Media Files
- **Images**: Application imagery and visual assets
- **starry_sky.jpg**: Main background/header image for the space theme
- **Purpose**: Static media files served directly by Flask

### `css/` - Stylesheets
- **custom_css.css**: Global custom styles and theme overrides
- **goals.css**: Goal-specific styling and layouts
- **progress.css**: Progress dashboard and chart styling
- **Framework**: Built on Bootstrap 5 foundation with custom overrides

### `js/` - JavaScript Files

#### Feature-Based Organization
JavaScript is organized by application feature for maintainability:

#### `goals/` - Goal Management Scripts
- **goals.js**: Goal creation, editing, and management functionality
- **Features**: Dynamic form handling, goal progress updates

#### `legal/` - Legal Compliance Scripts  
- **cookie_consent.js**: Cookie consent banner and preferences management
- **GDPR Compliance**: Handles user consent for tracking and analytics

#### `progress/` - Progress Dashboard Scripts
- **charts.js**: Chart.js integration for progress visualizations
- **entries.js**: Diary entry display and interaction
- **entry-toggles.js**: Toggle functionality for diary entry views
- **main.js**: Core progress dashboard functionality
- **Data Visualization**: Interactive charts showing user progress over time

## Frontend Technology Stack

### CSS Framework
- **Bootstrap 5**: Primary UI framework
- **Custom CSS**: Theme customization and component styling
- **Responsive Design**: Mobile-first approach

### JavaScript Libraries
- **Chart.js**: Data visualization for progress tracking
- **Bootstrap JS**: Component interactivity
- **Vanilla JS**: Custom application logic

## Development Patterns

### CSS Architecture
- **Component-based styling**: Each feature has dedicated CSS
- **Bootstrap customization**: Overrides in custom_css.css
- **CSS variables**: Used for theming and consistency

### JavaScript Architecture
- **Feature modules**: Each feature directory contains related scripts
- **Event-driven**: Uses modern event handling patterns
- **Progressive enhancement**: Works without JavaScript enabled

### Asset Management
- **Static serving**: Flask serves files directly from static/
- **Caching**: Configured for optimal browser caching
- **Organization**: Logical grouping by feature/purpose

## File Naming Conventions

- **Hyphenated names**: `entry-toggles.js`, `custom_css.css`
- **Feature prefixes**: Files grouped by application feature
- **Descriptive names**: Clear indication of file purpose

## Performance Considerations

- **Minification**: Production assets should be minified
- **Compression**: Served with gzip compression
- **Caching**: Appropriate cache headers for static files
- **Loading**: JavaScript loaded at end of body for performance

## Development Workflow

1. **CSS Changes**: Edit feature-specific CSS files
2. **JavaScript**: Add new scripts to appropriate feature directory
3. **Images**: Add to assets/ with descriptive names
4. **Testing**: Verify asset loading in development server