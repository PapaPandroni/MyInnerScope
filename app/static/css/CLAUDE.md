# app/static/css/ Directory

This directory contains CSS stylesheets for the "Aim for the Stars" application, built on Bootstrap 5 with custom styling.

## Stylesheet Files

### `custom_css.css` - Global Styles
- **Purpose**: Application-wide custom styles and Bootstrap overrides
- **Scope**: Global styles, theme variables, utility classes
- **Usage**: Loaded on every page for consistent styling
- **Content**: 
  - Color scheme and theme variables
  - Typography overrides
  - Global component styling
  - Responsive design utilities

### `goals.css` - Goal Management Styles
- **Purpose**: Styles specific to goal creation, display, and management
- **Scope**: Goal-specific components and layouts
- **Features**:
  - Goal card styling
  - Progress indicators
  - Form layouts for goal creation/editing
  - Goal status displays

### `progress.css` - Progress Dashboard Styles
- **Purpose**: Styles for progress tracking and analytics visualization
- **Scope**: Progress dashboard, charts, and statistics displays
- **Features**:
  - Chart container styling
  - Statistics card layouts
  - Progress visualization components
  - Diary entry displays in progress context

## CSS Architecture

### Framework Foundation
- **Bootstrap 5**: Primary CSS framework providing base styles
- **Custom overrides**: Feature-specific customizations
- **Responsive design**: Mobile-first responsive layouts

### Design System
- **Color palette**: Consistent color scheme across features
- **Typography**: Hierarchical text styling
- **Spacing**: Consistent margins and padding
- **Components**: Reusable styled components

## Development Patterns

### CSS Organization
- **Feature-based files**: Each major feature has its own CSS file
- **Global base**: Common styles in custom_css.css
- **Bootstrap integration**: Custom styles build on Bootstrap foundation
- **Component-scoped**: Styles specific to particular components

### Naming Conventions
- **BEM methodology**: Block-Element-Modifier naming where appropriate
- **Semantic names**: Classes named for purpose, not appearance
- **Feature prefixes**: Goal-specific classes prefixed with `goal-`

### Responsive Design
- **Mobile-first**: Base styles for mobile, enhanced for larger screens
- **Bootstrap grid**: Leverages Bootstrap's responsive grid system
- **Breakpoint consistency**: Uses Bootstrap's breakpoint system

## File Loading Order

1. **Bootstrap 5 CSS** (from CDN or local)
2. **custom_css.css** (global overrides)
3. **Feature-specific CSS** (goals.css, progress.css) as needed per page

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