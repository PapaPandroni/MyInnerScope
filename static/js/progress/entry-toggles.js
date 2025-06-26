/**
 * Entry toggle functionality for progress page
 * Handles expanding/collapsing diary entries in the top days section
 */

function toggleEntry(entryId) {
    const preview = document.getElementById('preview-' + entryId);
    const full = document.getElementById('full-' + entryId);
    
    if (preview.classList.contains('d-none')) {
        preview.classList.remove('d-none');
        full.classList.add('d-none');
    } else {
        preview.classList.add('d-none');
        full.classList.remove('d-none');
    }
}

// Make function globally available
window.toggleEntry = toggleEntry; 