/**
 * Server Clock Component
 * Creates a live updating clock synchronized with server time
 */

class ServerClock {
    constructor(elementId, serverTimeISO, timezone) {
        this.element = document.getElementById(elementId);
        this.timezone = timezone;
        
        if (!this.element) {
            console.error(`Server clock element with id '${elementId}' not found`);
            return;
        }
        
        // Calculate offset between server time and local time
        this.serverTime = new Date(serverTimeISO);
        this.localTime = new Date();
        this.offset = this.serverTime.getTime() - this.localTime.getTime();
        
        // Start the clock
        this.updateClock();
        this.interval = setInterval(() => this.updateClock(), 1000);
    }
    
    updateClock() {
        // Get current local time and apply server offset
        const now = new Date();
        const serverNow = new Date(now.getTime() + this.offset);
        
        // Format time as HH:MM:SS
        const timeString = serverNow.toTimeString().split(' ')[0];
        
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
        
        new ServerClock('server-clock', serverTime, timezone);
    }
});