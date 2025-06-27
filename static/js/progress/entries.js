/**
 * Entry toggle functionality for the progress page
 * Handles expanding/collapsing diary entries in the top days section
 */

class EntryManager {
    constructor() {
        this.init();
    }

    init() {
        // Entry toggle functionality is already available globally
        // This class can be extended for future entry-related functionality
    }

    /**
     * Toggle between preview and full view of an entry
     * @param {string} entryId - The ID of the entry to toggle
     */
    toggleEntry(entryId) {
        const preview = document.getElementById('preview-' + entryId);
        const full = document.getElementById('full-' + entryId);
        
        if (preview.classList.contains('d-none')) {
            // Currently showing full, switch to preview
            preview.classList.remove('d-none');
            full.classList.add('d-none');
        } else {
            // Currently showing preview, switch to full
            preview.classList.add('d-none');
            full.classList.remove('d-none');
        }
    }
}

// Create global instance
window.entryManager = new EntryManager();

// Keep the global function for backward compatibility with inline onclick handlers
window.toggleEntry = function(entryId) {
    window.entryManager.toggleEntry(entryId);
};

// Toggle extra entries for Top 3 Days
window.toggleExtraEntries = function(dayIndex) {
    const extraEntries = document.querySelectorAll('.extra-entry-' + dayIndex);
    const btn = document.getElementById('show-more-btn-' + dayIndex);
    let expanded = false;
    extraEntries.forEach(entry => {
        if (entry.classList.contains('d-none')) {
            entry.classList.remove('d-none');
            expanded = true;
        } else {
            entry.classList.add('d-none');
        }
    });
    if (btn) {
        btn.textContent = expanded ? 'Show less' : 'Show more';
    }
} 