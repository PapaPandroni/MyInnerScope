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
     * @param {string} entry_id - The ID of the entry to toggle
     */
    toggle_entry(entry_id) {
        const preview = document.getElementById('preview_' + entry_id);
        const full = document.getElementById('full_' + entry_id);
        
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
window.toggle_entry = function(entry_id) {
    window.entryManager.toggle_entry(entry_id);
};

// Toggle extra entries for Top 3 Days
window.toggle_extra_entries = function(day_index) {
    const extra_entries = document.querySelectorAll('.extra_entry_' + day_index);
    const btn = document.getElementById('show_more_btn_' + day_index);
    let expanded = false;
    extra_entries.forEach(entry => {
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

// Toggle extra goals in Recent Goals section
window.toggle_extra_goals = function() {
    const extra_goals = document.querySelectorAll('.extra-goal');
    const btn = document.getElementById('show_more_goals_btn');
    let expanded = false;
    extra_goals.forEach(goal => {
        if (goal.classList.contains('d-none')) {
            goal.classList.remove('d-none');
            expanded = true;
        } else {
            goal.classList.add('d-none');
        }
    });
    if (btn) {
        btn.textContent = expanded ? 'Show less' : 'Show more';
    }
} 