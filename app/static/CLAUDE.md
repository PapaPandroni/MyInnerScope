# app/static/ Directory

This directory contains static assets for the "My Inner Scope" web application frontend.

## Directory Structure

```
static/
├── assets/             # Image and media files
├── css/               # Feature-organized stylesheets
│   ├── progress/      # Progress dashboard specific CSS
│   └── shared/        # Shared components and base styles
└── js/                # Feature-organized JavaScript modules
    ├── goals/         # Goal management scripts
    ├── legal/         # Legal compliance (cookies, consent)
    ├── progress/      # Progress dashboard and analytics
    └── shared/        # Shared utilities and tour system
```

## Asset Organization

### `assets/` - Media Files ⭐ **ENHANCED**
- **Images**: Application imagery and visual assets
- **starry_sky.jpg**: Main background/header image for the space theme
- **SEO Assets**: Favicon system and social media assets
  - **favicon.ico**: Main favicon (16x16 and 32x32 pixels)
  - **favicon-16x16.png**: Small favicon for browser tabs
  - **favicon-32x32.png**: Standard favicon for bookmarks
  - **apple-touch-icon.png**: Apple device home screen icon (180x180)
  - **social-preview.jpg**: Social media preview image (1200x630)
  - **site.webmanifest**: Web app manifest for PWA support
- **Purpose**: Static media files served directly by Flask

### `css/` - Feature-Organized Stylesheets

#### `css/shared/` - Shared Components
- **base.css**: Global styles, theme variables, and Bootstrap overrides
- **goals.css**: Goal management styling and layouts  
- **tour.css**: User onboarding tour styling and animations

#### `css/progress/` - Progress Dashboard
- **progress.css**: Progress dashboard, chart styling, and interactive elements

**Framework**: Built on Bootstrap 5 with cosmic theme customization

### `js/` - Feature-Organized JavaScript Modules

#### `js/goals/` - Goal Management
- **goals.js**: Goal creation, editing, management, and progress tracking
- **Features**: Dynamic form handling, goal status updates

#### `js/legal/` - Legal Compliance  
- Files moved to shared/ (see shared section below)

#### `js/progress/` - Progress Dashboard & Analytics
- **charts.js**: Chart.js integration with clickable data points
- **entries.js**: Diary entry display and interaction patterns
- **entry-toggles.js**: Toggle functionality for diary entry views
- **main.js**: Core progress dashboard with interactive analytics
- **Features**: 
  - Clickable progress cards with detailed breakdowns
  - Interactive Chart.js visualizations
  - Points breakdown modals with transaction history

#### `js/shared/` - Shared Utilities ⭐ **NEW**
- **cookie_consent.js**: GDPR cookie consent and preferences management
- **tour-controller.js**: Interactive user onboarding tour system
- **Features**:
  - Multi-page tour with localStorage persistence
  - Progressive disclosure of application features
  - First-visit detection and guidance

## Frontend Technology Stack

### CSS Framework
- **Bootstrap 5**: Primary UI framework
- **Custom CSS**: Theme customization and component styling
- **Responsive Design**: Mobile-first approach

### JavaScript Libraries
- **Chart.js**: Interactive data visualization with clickable elements
- **Bootstrap JS**: Component interactivity and modal management
- **Vanilla JS**: Custom application logic and tour system
- **localStorage API**: User preferences and tour state persistence

## Development Patterns

### CSS Architecture
- **Component-based styling**: Each feature has dedicated CSS
- **Bootstrap customization**: Overrides in custom_css.css
- **CSS variables**: Used for theming and consistency

### JavaScript Architecture
- **Feature modules**: Directory-based organization by application feature
- **Event-driven**: Modern event handling with delegation patterns
- **Progressive enhancement**: Core functionality works without JavaScript
- **API Integration**: AJAX requests to API blueprint endpoints
- **State Management**: localStorage for user preferences and tour progress

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

## Recent Frontend Improvements

### User Experience Enhancements
- **Interactive Analytics**: Clickable progress cards with detailed point breakdowns
- **Onboarding System**: Multi-page guided tour for new users
- **Enhanced Visualizations**: Chart.js integration with clickable data points

### Code Organization
- **Feature-based Structure**: CSS and JS organized by application feature
- **Shared Components**: Common utilities in shared/ directories
- **API Integration**: Frontend communicates with backend via API endpoints

## Development Workflow

1. **CSS Changes**: Edit feature-specific CSS files in appropriate subdirectory
2. **JavaScript**: Add new scripts to feature-based directories (goals/, progress/, shared/)
3. **Images**: Add to assets/ with descriptive names
4. **API Integration**: Use API blueprint endpoints for dynamic content
5. **Testing**: Verify asset loading and feature functionality in development server