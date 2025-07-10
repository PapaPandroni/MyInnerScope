# app/static/assets/ Directory

This directory contains image and media assets for the "Aim for the Stars" application.

## Current Assets

### Images
- **starry_sky.jpg**: Main background/header image supporting the space theme
  - **Usage**: Hero sections, page headers, theme reinforcement
  - **Theme**: Reinforces the "Aim for the Stars" branding
  - **Size**: Optimized for web display

## Asset Guidelines

### Image Standards
- **Format**: Prefer JPEG for photos, PNG for graphics with transparency
- **Optimization**: Compress images for web delivery
- **Naming**: Use descriptive, lowercase, hyphenated names
- **Size**: Multiple sizes for responsive design when needed

### File Organization
- **Categories**: Group by asset type (images, icons, documents)
- **Naming Convention**: `category_name_purpose.extension`
- **Examples**: `hero_starry_sky.jpg`, `icon_goal_star.png`

## Usage in Templates

Assets are referenced in templates using Flask's `url_for()`:
```html
<img src="{{ url_for('static', filename='assets/starry_sky.jpg') }}" alt="Starry Sky">
```

## Performance Considerations

- **File size**: Keep images under 500KB for fast loading
- **Responsive images**: Provide multiple sizes if needed
- **Alt text**: Always provide descriptive alt text for accessibility
- **Loading**: Use lazy loading for below-the-fold images

## Adding New Assets

1. **Optimization**: Compress images before adding
2. **Naming**: Use descriptive, consistent naming
3. **Documentation**: Update this file when adding new assets
4. **Testing**: Verify assets load correctly in development

## Future Assets

Consider adding:
- **Favicon**: Site icon for browser tabs
- **App icons**: Various sizes for web app manifest
- **Social media**: Open Graph images for sharing
- **Illustrations**: Custom graphics for features
- **Loading animations**: Spinners or progress indicators