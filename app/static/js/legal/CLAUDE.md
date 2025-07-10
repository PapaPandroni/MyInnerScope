# app/static/js/legal/ Directory

This directory contains JavaScript functionality for legal compliance and privacy features in the "Aim for the Stars" application.

## Scripts

### `cookie_consent.js` - Cookie Consent Management
- **Purpose**: Handles cookie consent banner and user privacy preferences
- **GDPR Compliance**: Ensures compliance with European privacy regulations
- **Features**:
  - Cookie consent banner display and interaction
  - User preference storage and management
  - Analytics tracking consent management
  - Cookie category selection (essential, analytics, etc.)

## Functionality Overview

### Cookie Consent Banner
- **First visit detection**: Shows banner to new users
- **Consent options**: Allow users to accept/decline different cookie types
- **Preference storage**: Stores user preferences in local storage
- **Banner dismissal**: Hides banner after user interaction

### Privacy Preference Management
- **Granular control**: Users can select specific cookie categories
- **Preference updates**: Allow users to change preferences later
- **Consent withdrawal**: Option to withdraw previously given consent
- **Clear explanations**: Descriptions of what each cookie category does

### Analytics Integration
- **Conditional tracking**: Only enable analytics if user consents
- **Tracking script management**: Dynamically load/unload tracking scripts
- **Respect preferences**: Honor user choices throughout session

## Technical Implementation

### Cookie Management
- **Local storage**: Preferences stored in browser local storage
- **Cookie detection**: Checks for existing consent preferences
- **Expiration handling**: Manages consent preference expiration
- **Cross-page consistency**: Maintains preferences across site navigation

### Privacy Standards
- **Opt-in approach**: Users must actively consent to non-essential cookies
- **Clear information**: Transparent about what data is collected
- **Easy withdrawal**: Simple process to change or withdraw consent
- **No tracking without consent**: No analytics until user explicitly agrees

### User Interface
- **Non-intrusive design**: Doesn't block main content unnecessarily
- **Clear controls**: Obvious accept/decline options
- **Accessibility**: Keyboard navigation and screen reader friendly
- **Mobile responsive**: Works well on all device sizes

## Compliance Features

### GDPR Requirements
- **Lawful basis**: Clear legal basis for data processing
- **Data minimization**: Only collect necessary data
- **User rights**: Support for data access and deletion requests
- **Consent management**: Proper consent collection and storage

### Cookie Categories
- **Essential**: Required for basic site functionality
- **Analytics**: Usage statistics and performance monitoring
- **Marketing**: Advertising and remarketing (if applicable)
- **Preferences**: User customization and settings

## Integration Points

### Flask Backend
- **Privacy routes**: Integrates with privacy policy and terms pages
- **Settings management**: Server-side preference storage if needed
- **Legal pages**: Works with legal blueprint routes

### Analytics Services
- **Google Analytics**: Conditional loading based on consent
- **Custom analytics**: Internal tracking with user permission
- **Third-party services**: Manages consent for external services

## Development Notes

### Adding New Tracking
1. **Check consent**: Always verify user has consented before tracking
2. **Category assignment**: Assign new tracking to appropriate category
3. **Conditional loading**: Load tracking scripts only with consent
4. **Documentation**: Update privacy policy with new tracking details

### Testing Consent Flow
1. **Clear storage**: Test with fresh browser state
2. **Consent scenarios**: Test accept, decline, and partial consent
3. **Preference changes**: Test updating preferences after initial consent
4. **Analytics verification**: Verify tracking only occurs with consent

### Maintenance
- **Regular review**: Review and update consent mechanisms
- **Legal updates**: Keep consent flow updated with legal requirements
- **User feedback**: Monitor and respond to privacy-related user feedback