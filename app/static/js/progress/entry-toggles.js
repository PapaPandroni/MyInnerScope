/**
 * Entry toggle functionality for progress page
 * Handles expanding/collapsing diary entries in the top days section
 */

function toggle_entry(entry_id) {
    const preview = document.getElementById('preview_' + entry_id);
    const full = document.getElementById('full_' + entry_id);
    
    if (preview.classList.contains('d-none')) {
        preview.classList.remove('d-none');
        full.classList.add('d-none');
    } else {
        preview.classList.add('d-none');
        full.classList.remove('d-none');
    }
}

// Make function globally available
window.toggle_entry = toggle_entry; 