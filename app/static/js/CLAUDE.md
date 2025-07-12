# app/static/js/ Directory

This directory contains JavaScript files for the "Aim for the Stars" application, organized by feature for maintainability.

## Directory Structure

```
js/
├── goals/              # Goal management functionality
├── legal/              # Legal compliance (moved to shared/)
├── progress/           # Progress tracking and interactive analytics
└── shared/             # Shared utilities and tour system ⭐ NEW
```

## JavaScript Architecture

### Feature-Based Organization
JavaScript is organized into feature directories to maintain clear separation of concerns and improve code maintainability.

### Technology Stack
- **Vanilla JavaScript**: Primary development approach for performance and simplicity
- **Chart.js**: Interactive data visualization with clickable elements
- **Bootstrap JavaScript**: Modal management and component interactivity
- **localStorage API**: User preferences and tour state persistence
- **Modern ES6+**: Arrow functions, async/await, modern DOM APIs

## Feature Directories

### `goals/` - Goal Management Scripts
- **Purpose**: Interactive functionality for goal creation, editing, and tracking
- **Components**: Goal forms, progress updates, goal management interface

### `progress/` - Interactive Progress Dashboard ⭐ **ENHANCED**
- **Purpose**: Advanced progress tracking with interactive analytics
- **Components**: 
  - **charts.js**: Chart.js integration with clickable data points
  - **entries.js**: Diary entry display and interaction patterns
  - **entry-toggles.js**: Toggle functionality for diary entry views  
  - **main.js**: Core dashboard functionality with API integration
- **Features**: Clickable progress cards, points breakdown modals, real-time updates

### `shared/` - Shared Utilities ⭐ **NEW**
- **Purpose**: Common functionality and user experience features
- **Components**:
  - **cookie_consent.js**: GDPR cookie consent and preferences (moved from legal/)
  - **tour-controller.js**: Interactive user onboarding tour system
- **Features**: 
  - Multi-page guided tours with localStorage persistence
  - Progressive disclosure of application features
  - First-visit detection and user guidance

## Development Patterns

### Code Organization
- **Feature modules**: Each feature directory contains related scripts
- **Single responsibility**: Each file has a clear, focused purpose
- **Event-driven**: Uses modern event handling and DOM APIs
- **Progressive enhancement**: Functionality enhances the base HTML experience

### JavaScript Standards
- **Modern syntax**: ES6+ features (arrow functions, const/let, modules)
- **DOM manipulation**: QuerySelector API and modern DOM methods
- **Error handling**: Proper error handling and user feedback
- **Performance**: Efficient DOM queries and event handling

### Loading Strategy
- **Non-blocking**: Scripts loaded at end of body
- **Conditional loading**: Feature scripts loaded only on relevant pages
- **Dependency management**: Clear dependency ordering

## Integration Patterns

### Flask Integration
- **API endpoints**: AJAX requests to API blueprint for dynamic content
- **CSRF tokens**: JavaScript includes CSRF tokens in all requests
- **URL generation**: Uses Flask-generated URLs in HTML data attributes
- **Session awareness**: Respects user authentication state
- **Points integration**: Real-time points breakdown via API calls

### Template Integration
- **Data passing**: Server data passed via HTML data attributes or JSON
- **Progressive enhancement**: JavaScript enhances server-rendered HTML
- **Graceful degradation**: Core functionality works without JavaScript

## File Naming Conventions

- **Hyphenated names**: `entry-toggles.js`, `cookie_consent.js`
- **Descriptive names**: Clear indication of file purpose
- **Feature grouping**: Files organized by application feature

## Performance Considerations

- **Minification**: Production JavaScript should be minified
- **Caching**: Leverage browser caching for script files
- **Bundle size**: Keep individual scripts focused and lightweight
- **Loading**: Async/defer loading where appropriate

## Development Workflow

1. **Feature scripts**: Add new functionality to appropriate feature directory
2. **Testing**: Test JavaScript functionality across browsers
3. **Documentation**: Update feature documentation when adding scripts
4. **Integration**: Ensure scripts work with Flask backend and CSRF protection

## Future Enhancements

Consider adding:
- **Module bundling**: Webpack or similar for production builds
- **TypeScript**: Type safety for larger JavaScript codebases
- **Testing**: JavaScript unit tests for complex functionality
- **Service workers**: For offline functionality and caching