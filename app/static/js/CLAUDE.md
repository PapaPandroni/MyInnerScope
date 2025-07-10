# app/static/js/ Directory

This directory contains JavaScript files for the "Aim for the Stars" application, organized by feature for maintainability.

## Directory Structure

```
js/
├── goals/              # Goal management functionality
├── legal/              # Legal compliance (cookies, privacy)
└── progress/           # Progress tracking and visualization
```

## JavaScript Architecture

### Feature-Based Organization
JavaScript is organized into feature directories to maintain clear separation of concerns and improve code maintainability.

### Technology Stack
- **Vanilla JavaScript**: Primary development approach for performance
- **Chart.js**: Data visualization library for progress charts
- **Bootstrap JavaScript**: Component interactivity
- **Modern ES6+**: Uses modern JavaScript features

## Feature Directories

### `goals/` - Goal Management Scripts
- **Purpose**: Interactive functionality for goal creation, editing, and tracking
- **Components**: Goal forms, progress updates, goal management interface

### `legal/` - Legal Compliance Scripts
- **Purpose**: Privacy and legal compliance functionality
- **Components**: Cookie consent management, privacy preferences

### `progress/` - Progress Dashboard Scripts
- **Purpose**: Interactive progress tracking and data visualization
- **Components**: Charts, diary entry interactions, statistics displays

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
- **CSRF tokens**: JavaScript respects CSRF protection
- **URL generation**: Uses Flask-generated URLs in HTML data attributes
- **Session awareness**: Respects user authentication state

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