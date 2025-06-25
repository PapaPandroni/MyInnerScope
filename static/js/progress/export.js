/**
 * PDF Export functionality for the progress page
 * Handles the export button click and loading overlay
 */

class ExportManager {
    constructor() {
        this.exportButton = null;
        this.overlay = null;
        this.init();
    }

    init() {
        this.exportButton = document.getElementById('exportButton');
        this.overlay = document.getElementById('generatingOverlay');
        
        if (this.exportButton) {
            this.exportButton.addEventListener('click', this.handleExport.bind(this));
        }
    }

    /**
     * Handle the export button click
     */
    async handleExport() {
        this.showOverlay();
        
        try {
            const response = await fetch('/export-journey', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
            });
            
            if (!response.ok) {
                throw new Error('Export failed');
            }
            
            const blob = await response.blob();
            this.downloadFile(blob, 'my-self-reflective-journey.pdf');
        } catch (error) {
            console.error('Export failed:', error);
            this.showError('Failed to generate export. Please try again.');
        } finally {
            this.hideOverlay();
        }
    }

    /**
     * Show the loading overlay
     */
    showOverlay() {
        if (this.overlay) {
            this.overlay.classList.remove('d-none');
        }
    }

    /**
     * Hide the loading overlay
     */
    hideOverlay() {
        if (this.overlay) {
            this.overlay.classList.add('d-none');
        }
    }

    /**
     * Download a file from blob
     * @param {Blob} blob - The file blob to download
     * @param {string} filename - The filename for the download
     */
    downloadFile(blob, filename) {
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        a.remove();
    }

    /**
     * Show error message to user
     * @param {string} message - Error message to display
     */
    showError(message) {
        alert(message);
    }
}

// Create global instance
window.exportManager = new ExportManager(); 