# app/static/css/ Directory

This directory contains feature-organized CSS stylesheets for the "Aim for the Stars" application, built on Bootstrap 5 with cosmic theme customization.

## Feature-Based Organization

### `shared/` - Shared Components
#### `shared/base.css` - Global Cosmic Theme
- **Purpose**: Application-wide cosmic theme and Bootstrap overrides
- **Features**:
  - Cosmic color palette with space-inspired gradients
  - Typography with celestial theme
  - Global component styling
  - Responsive design utilities
  - Theme variables for consistency

#### `shared/goals.css` - Goal Management Styles
- **Purpose**: Goal-specific components and layouts
- **Features**:
  - Goal card styling with cosmic theme
  - Progress indicators with star motifs
  - Form layouts for goal creation/editing
  - Goal status displays

#### `shared/tour.css` - User Onboarding Tour ⭐ **NEW**
- **Purpose**: Interactive tour system styling
- **Features**:
  - Tour overlay and modal styling
  - Step indicator animations
  - Highlighted element styling
  - Responsive tour layout

### `progress/` - Progress Dashboard
#### `progress/progress.css` - Enhanced Progress Visualization
- **Purpose**: Interactive progress tracking and analytics
- **Features**:
  - **Clickable cards**: Interactive progress cards with hover effects
  - **Chart styling**: Chart.js container and responsive layouts
  - **Modal integration**: Points breakdown modal styling
  - **Statistics displays**: Enhanced statistics card layouts
  - **Cosmic theme**: Space-inspired progress visualizations

## CSS Architecture

### Framework Foundation
- **Bootstrap 5**: Primary CSS framework with cosmic theme overrides
- **Feature organization**: Directory-based CSS organization by feature
- **Responsive design**: Mobile-first with enhanced interactive elements

### Cosmic Design System
- **Color palette**: Space-inspired cosmic colors with gradients
- **Typography**: Celestial-themed text styling and hierarchy
- **Interactive elements**: Hover effects and transitions
- **Theme consistency**: Unified cosmic branding across all features
- **Accessibility**: High contrast ratios and readable color combinations

## Development Patterns

### CSS Organization
- **Directory-based**: Feature-specific CSS organized in subdirectories
- **Shared components**: Common styles in `shared/` directory
- **Feature isolation**: Feature-specific styles in dedicated directories
- **Bootstrap integration**: Custom cosmic theme builds on Bootstrap foundation

### Naming Conventions
- **BEM methodology**: Block-Element-Modifier naming for complex components
- **Semantic names**: Classes named for purpose (e.g., `.progress-card-clickable`)
- **Feature prefixes**: Clear feature identification in class names
- **Cosmic theme**: Consistent cosmic-themed class names

### Responsive Design
- **Mobile-first**: Base styles for mobile, enhanced for larger screens
- **Bootstrap grid**: Leverages Bootstrap's responsive grid system
- **Breakpoint consistency**: Uses Bootstrap's breakpoint system

## File Loading Order

1. **Bootstrap 5 CSS** (from CDN)
2. **shared/base.css** (global cosmic theme)
3. **shared/goals.css** (goal management styles)
4. **shared/tour.css** (onboarding tour styles)
5. **progress/progress.css** (progress dashboard specific)

## Customization Guidelines

### Adding New Styles
1. **Check Bootstrap**: Use Bootstrap classes when available
2. **Global vs. Feature**: Determine if styles belong in custom_css.css or feature file
3. **Responsive**: Ensure styles work across all screen sizes
4. **Consistency**: Follow existing patterns and naming conventions

### Color Scheme
- **Primary**: Theme colors aligned with "Aim for the Stars" branding
- **Semantic**: Success, warning, danger colors for user feedback
- **Neutral**: Grays for text and backgrounds

## Performance Considerations

- **Minification**: CSS should be minified in production
- **Critical CSS**: Consider inlining critical above-the-fold styles
- **Unused styles**: Remove unused Bootstrap components if needed
- **Caching**: Leverage browser caching for CSS files