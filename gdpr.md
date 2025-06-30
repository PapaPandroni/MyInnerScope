# GDPR & Legal Compliance Implementation Plan

## Overview
This document outlines the plan to implement GDPR and legal compliance features for the "Aim for the Stars" web application, with a focus on user self-service and transparency. The plan integrates these features into a new user profile/settings page, providing users with control over their data and compliance with EU regulations.

---

## 1. User Profile/Settings Page

### A. Route and Template
- **Route:** `/profile` (link in navbar as "Profile")
- **Template:** `settings.html` (page title: e.g., "Captain's Cabin" or "The Bridge")
- **Access:** Only for logged-in users

### B. Features to Include (Initial)
- Download my data (JSON and CSV)
- Delete my account (with confirmation)
- View Privacy Policy and Terms of Service (links)

### C. Navigation
- Add a "Profile" link to the navbar (visible when logged in)
- Add links to legal pages in the footer and on the profile page

---

## 2. Legal Compliance Features

### A. Privacy Policy and Terms of Service
- Create dedicated pages (`/privacy`, `/terms`) with clear, user-friendly language
- Link to these pages from the profile page and site footer

### B. Cookie Consent Banner
- Show a banner to new users explaining cookie usage, with an "Accept" button
- Store consent in a cookie and hide the banner once accepted
- Implemented site-wide (not just on profile page)

### C. Data Portability
- Add a "Download my data" button to the profile page
- Route returns all user-related data as both JSON and CSV files
- Ensure only authenticated users can access their own data

### D. Right to Erasure (Account Deletion)
- Add a "Delete my account" button to the profile page
- Route asks for confirmation (and password re-entry for safety)
- Deletes user and all related data (cascade delete), logs out, and shows a confirmation page

---

## 3. File/Code Changes
- `routes/user.py` (new blueprint for user profile/settings)
- `templates/settings.html` (new profile/settings page)
- `templates/base.html` (add profile link to navbar)
- `routes/legal.py` (privacy policy, terms of service)
- `templates/privacy.html`, `templates/terms.html`
- `static/js/cookie_consent.js` (cookie banner logic)
- `forms.py` (add/change forms as needed)
- `models/` (ensure cascade delete for user data)
- `gdpr.md` (this plan)

---

## 4. Risk Assessment
- **Profile/settings page:** No risk; just a new page.
- **Delete account:** High risk if not tested (permanent data loss). Requires confirmation and careful implementation.
- **Data download:** No risk; just reads and serializes data.
- **Legal pages/cookie consent:** No risk.

---

## 5. Next Steps
- Implement the user profile/settings page and integrate legal compliance features as outlined above.
- Start with legal features (data download, account deletion, privacy/terms links, cookie consent).
- Expand profile page features in the future as needed. 