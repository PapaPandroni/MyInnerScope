/**
 * Server Clock Component
 * Shows current UTC time (server time)
 */

class ServerClock {
    constructor(elementId, serverTimeISO, timezone) {
        this.element = document.getElementById(elementId);
        this.timezone = timezone;
        
        if (!this.element) {
            console.error(`Server clock element with id '${elementId}' not found`);
            return;
        }
        
        // Parse the server time string to avoid browser timezone interference
        this.serverTime = new Date(serverTimeISO);
        this.startTime = Date.now();
        
        console.log('Server clock initialized for UTC time display');
        
        // Start the clock
        this.updateClock();
        this.interval = setInterval(() => this.updateClock(), 1000);
    }
    
    updateClock() {
        // Calculate elapsed time since initialization
        const elapsed = Date.now() - this.startTime;
        
        // Add elapsed time to server time
        const currentTime = new Date(this.serverTime.getTime() + elapsed);
        
        // Extract UTC time components to avoid browser timezone conversion
        const timeString = currentTime.toISOString().slice(11, 19);
        
        // Update the display
        this.element.textContent = `Server Time: ${timeString} ${this.timezone}`;
    }
    
    destroy() {
        if (this.interval) {
            clearInterval(this.interval);
            this.interval = null;
        }
    }
}

// Initialize server clock when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Get server time from template variables (will be injected)
    const serverTimeElement = document.getElementById('server-time-data');
    if (serverTimeElement) {
        const serverTime = serverTimeElement.dataset.serverTime;
        const timezone = serverTimeElement.dataset.timezone;
        
        console.log('Initializing server clock with:', serverTime, timezone);
        new ServerClock('server-clock', serverTime, timezone);
    } else {
        console.error('Server time data element not found');
    }
});