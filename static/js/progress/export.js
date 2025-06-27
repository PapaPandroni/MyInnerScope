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
     * Wait for wordcloud to be fully rendered
     * @returns {Promise<string|null>} Base64 image data or null if not available
     */
    async waitForWordcloud() {
        return new Promise((resolve) => {
            const maxAttempts = 50; // 5 seconds max wait
            let attempts = 0;
            
            const checkWordcloud = () => {
                attempts++;
                console.log(`Checking export wordcloud canvas (attempt ${attempts}/${maxAttempts})...`);
                const wordcloudCanvas = document.getElementById('wordcloud-canvas');
                if (wordcloudCanvas) {
                    // Check if canvas has content (not just empty)
                    const ctx = wordcloudCanvas.getContext('2d');
                    const imageData = ctx.getImageData(0, 0, wordcloudCanvas.width, wordcloudCanvas.height);
                    const hasContent = imageData.data.some(pixel => pixel !== 0);
                    console.log('Export canvas has content:', hasContent);
                    if (hasContent) {
                        const imageDataUrl = wordcloudCanvas.toDataURL('image/png');
                        console.log('Export canvas image data length:', imageDataUrl.length);
                        resolve(imageDataUrl);
                        return;
                    }
                }
                if (attempts >= maxAttempts) {
                    console.log('Export wordcloud canvas not found or empty after maximum attempts');
                    resolve(null);
                    return;
                }
                setTimeout(checkWordcloud, 100);
            };
            checkWordcloud();
        });
    }

    /**
     * Handle the export button click
     */
    async handleExport() {
        this.showOverlay();
        
        try {
            console.log('Starting PDF export...');
            
            // Wait for wordcloud to be ready
            const wordcloudImage = await this.waitForWordcloud();
            console.log('Wordcloud image captured:', wordcloudImage ? 'Yes' : 'No');
            
            const response = await fetch('/export-journey', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ wordcloud_image: wordcloudImage })
            });
            
            if (!response.ok) {
                throw new Error(`Export failed: ${response.status} ${response.statusText}`);
            }
            
            const blob = await response.blob();
            this.downloadFile(blob, 'my-self-reflective-journey.pdf');
            console.log('PDF export completed successfully');
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