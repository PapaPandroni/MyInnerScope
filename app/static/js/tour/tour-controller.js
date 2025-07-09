/**
 * Onboarding Tour Controller
 * Manages the interactive user onboarding experience
 */

class OnboardingTour {
    constructor() {
        this.currentPhase = 0;
        this.phases = ['welcome', 'first-entry', 'discovery'];
        this.isActive = false;
        this.originalFormAction = null;
        
        // Bind methods to preserve context
        this.start = this.start.bind(this);
        this.skip = this.skip.bind(this);
        this.nextPhase = this.nextPhase.bind(this);
        this.complete = this.complete.bind(this);
    }

    /**
     * Check if user should see the onboarding tour
     */
    shouldShowTour() {
        const completed = localStorage.getItem('tour_completed');
        const isNewUser = window.tourConfig?.isNewUser || false;
        const userEntryCount = window.tourConfig?.userEntryCount || 0;
        
        return !completed && isNewUser && userEntryCount === 0;
    }

    /**
     * Initialize and start the tour
     */
    init() {
        if (this.shouldShowTour()) {
            // Small delay to ensure page is fully loaded
            setTimeout(() => {
                this.start();
            }, 500);
        }
        
        // Add "Take Tour Again" button to navbar if completed
        this.addTourMenuOption();
    }

    /**
     * Start the onboarding tour
     */
    start() {
        this.isActive = true;
        this.currentPhase = 0;
        
        // Store tour state in sessionStorage for page transitions
        sessionStorage.setItem('tour_active', 'true');
        sessionStorage.setItem('tour_phase', this.currentPhase);
        
        this.showPhase('welcome');
    }

    /**
     * Skip the tour and mark as completed
     */
    skip() {
        this.complete();
        this.cleanup();
    }

    /**
     * Move to next phase
     */
    nextPhase() {
        this.currentPhase++;
        
        if (this.currentPhase >= this.phases.length) {
            this.complete();
            return;
        }
        
        sessionStorage.setItem('tour_phase', this.currentPhase);
        this.showPhase(this.phases[this.currentPhase]);
    }

    /**
     * Show specific tour phase
     */
    showPhase(phaseName) {
        // Remove any existing tour elements
        this.cleanup();
        
        switch (phaseName) {
            case 'welcome':
                this.showWelcomePhase();
                break;
            case 'first-entry':
                this.showFirstEntryPhase();
                break;
            case 'discovery':
                this.showDiscoveryPhase();
                break;
        }
    }

    /**
     * Phase 1: Welcome Modal
     */
    showWelcomePhase() {
        const modalHTML = `
            <div class="modal fade tour-modal" id="tourWelcomeModal" tabindex="-1" role="dialog">
                <div class="modal-dialog modal-dialog-centered" role="document">
                    <div class="modal-content tour-welcome-content">
                        <div class="modal-body text-center">
                            <div class="tour-cosmic-header">
                                <i class="fas fa-star tour-star-icon"></i>
                                <h2 class="tour-welcome-title">Welcome to Your Inner Universe</h2>
                                <p class="tour-welcome-subtitle">In 2 minutes, you'll create your first reflection and discover how it becomes insight</p>
                            </div>
                            <div class="tour-welcome-buttons">
                                <button class="btn btn-primary tour-btn-primary" id="tour-start-btn">
                                    <i class="fas fa-rocket me-2"></i>Start Journey
                                </button>
                                <button class="btn btn-outline-secondary tour-btn-secondary" id="tour-skip-btn">
                                    Skip for Now
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        document.body.insertAdjacentHTML('beforeend', modalHTML);
        
        // Add event listeners
        document.getElementById('tour-start-btn').addEventListener('click', () => {
            this.hideModal('tourWelcomeModal');
            this.showTextareaGuidance();
        });
        
        document.getElementById('tour-skip-btn').addEventListener('click', () => {
            this.hideModal('tourWelcomeModal');
            this.skip();
        });
        
        // Show modal
        const modal = new bootstrap.Modal(document.getElementById('tourWelcomeModal'));
        modal.show();
    }

    /**
     * Show textarea guidance part of first entry phase
     */
    showTextareaGuidance() {
        const textarea = document.getElementById('diary-textarea');
        if (!textarea) return;
        
        // Pre-populate with example text
        textarea.value = "I helped a colleague with their project today";
        
        // Add highlight and tooltip
        this.addHighlight(textarea, {
            title: "This is where transformation begins",
            text: "Try editing this example or write about your own experience",
            position: "top",
            showContinue: true,
            onContinue: () => {
                this.showRatingGuidance();
            }
        });
        
        // Focus the textarea
        textarea.focus();
        textarea.setSelectionRange(textarea.value.length, textarea.value.length);
    }

    /**
     * Show rating guidance part of first entry phase
     */
    showRatingGuidance() {
        this.removeHighlights();
        
        const ratingButtons = document.querySelectorAll('.rating-btn');
        if (ratingButtons.length === 0) return;
        
        // Highlight both rating buttons
        ratingButtons.forEach(btn => {
            this.addHighlight(btn, {
                title: "The key insight",
                text: "Is this behavior you want to continue or improve? This creates patterns that help you understand yourself better.",
                position: "top",
                showContinue: false
            });
        });
        
        // Intercept form submission to continue tour
        this.interceptFormSubmission();
    }

    /**
     * Intercept diary form submission during tour
     */
    interceptFormSubmission() {
        const form = document.getElementById('diary-form');
        if (!form) return;
        
        // Store original action
        this.originalFormAction = form.action;
        
        const buttons = document.querySelectorAll('.rating-btn');
        buttons.forEach(btn => {
            btn.addEventListener('click', (e) => {
                if (this.isActive) {
                    // Let the form submit normally but then continue tour
                    setTimeout(() => {
                        this.showCelebration(() => {
                            // Navigate to progress page for discovery phase
                            window.location.href = '/progress?tour=true';
                        });
                    }, 500);
                }
            });
        });
    }

    /**
     * Phase 3: Discovery Phase (on progress page)
     */
    showDiscoveryPhase() {
        // Check if we're on progress page
        if (!window.location.pathname.includes('/progress')) {
            return;
        }
        
        // Remove tour parameter from URL
        const url = new URL(window.location);
        url.searchParams.delete('tour');
        window.history.replaceState({}, document.title, url);
        
        setTimeout(() => {
            this.showProgressInsights();
        }, 1000);
    }

    /**
     * Show progress page insights
     */
    showProgressInsights() {
        // Highlight behavior cards
        const behaviorCards = document.querySelectorAll('.improvements-card, .positive-card');
        if (behaviorCards.length > 0) {
            behaviorCards.forEach(card => {
                this.addHighlight(card, {
                    title: "Your reflection became insight!",
                    text: "Soon you'll click here to explore patterns in your growth journey",
                    position: "top",
                    showContinue: true,
                    onContinue: () => {
                        this.showChartsPreview();
                    }
                });
            });
        } else {
            this.showChartsPreview();
        }
    }

    /**
     * Show charts preview
     */
    showChartsPreview() {
        this.removeHighlights();
        
        const chartsContainer = document.querySelector('#pointsChart, .container.mt-5');
        if (chartsContainer) {
            this.addHighlight(chartsContainer, {
                title: "Visualize your growth",
                text: "Imagine seeing your personal development trends over weeks and months",
                position: "top",
                showContinue: true,
                onContinue: () => {
                    this.completeTour();
                }
            });
        } else {
            this.completeTour();
        }
    }

    /**
     * Complete the tour with celebration
     */
    completeTour() {
        this.removeHighlights();
        
        this.showCelebration(() => {
            // Navigate back to diary page
            window.location.href = '/diary';
        });
    }

    /**
     * Show celebration animation
     */
    showCelebration(callback) {
        // Create celebration overlay
        const celebrationHTML = `
            <div class="tour-celebration-overlay">
                <div class="tour-celebration-content">
                    <div class="tour-star-burst">
                        <i class="fas fa-star tour-celebration-star"></i>
                        <i class="fas fa-star tour-celebration-star"></i>
                        <i class="fas fa-star tour-celebration-star"></i>
                        <i class="fas fa-star tour-celebration-star"></i>
                        <i class="fas fa-star tour-celebration-star"></i>
                    </div>
                    <h3 class="tour-celebration-title">🌟 Journey Begins!</h3>
                    <p class="tour-celebration-text">You're ready to explore your inner universe. Write regularly and watch insights emerge!</p>
                </div>
            </div>
        `;
        
        document.body.insertAdjacentHTML('beforeend', celebrationHTML);
        
        // Remove after animation
        setTimeout(() => {
            const overlay = document.querySelector('.tour-celebration-overlay');
            if (overlay) {
                overlay.remove();
            }
            
            this.complete();
            
            if (callback) {
                callback();
            }
        }, 3000);
    }

    /**
     * Add highlight to element with tooltip
     */
    addHighlight(element, options = {}) {
        element.classList.add('tour-highlight');
        
        if (options.title || options.text) {
            const tooltip = this.createTooltip(options);
            element.appendChild(tooltip);
        }
    }

    /**
     * Create tooltip element
     */
    createTooltip(options) {
        const tooltip = document.createElement('div');
        tooltip.className = 'tour-tooltip';
        
        let html = '';
        if (options.title) {
            html += `<h6 class="tour-tooltip-title">${options.title}</h6>`;
        }
        if (options.text) {
            html += `<p class="tour-tooltip-text">${options.text}</p>`;
        }
        if (options.showContinue) {
            html += `<button class="btn btn-sm btn-primary tour-continue-btn">Continue</button>`;
        }
        
        tooltip.innerHTML = html;
        
        // Add continue button listener
        if (options.showContinue && options.onContinue) {
            tooltip.querySelector('.tour-continue-btn').addEventListener('click', options.onContinue);
        }
        
        return tooltip;
    }

    /**
     * Remove all tour highlights
     */
    removeHighlights() {
        document.querySelectorAll('.tour-highlight').forEach(element => {
            element.classList.remove('tour-highlight');
            
            // Remove tooltips
            const tooltips = element.querySelectorAll('.tour-tooltip');
            tooltips.forEach(tooltip => tooltip.remove());
        });
    }

    /**
     * Hide modal
     */
    hideModal(modalId) {
        const modal = document.getElementById(modalId);
        if (modal) {
            const bsModal = bootstrap.Modal.getInstance(modal);
            if (bsModal) {
                bsModal.hide();
            }
            
            // Remove after hide animation
            setTimeout(() => {
                modal.remove();
            }, 300);
        }
    }

    /**
     * Mark tour as completed
     */
    complete() {
        this.isActive = false;
        localStorage.setItem('tour_completed', 'true');
        sessionStorage.removeItem('tour_active');
        sessionStorage.removeItem('tour_phase');
        this.cleanup();
    }

    /**
     * Clean up tour elements and event listeners
     */
    cleanup() {
        // Remove all tour-related elements
        document.querySelectorAll('.tour-modal, .tour-tooltip, .tour-celebration-overlay').forEach(el => {
            el.remove();
        });
        
        // Remove highlights
        this.removeHighlights();
        
        // Remove backdrop if exists
        document.querySelectorAll('.modal-backdrop').forEach(backdrop => {
            backdrop.remove();
        });
    }

    /**
     * Add "Take Tour Again" option to navbar
     */
    addTourMenuOption() {
        const dropdown = document.querySelector('.dropdown-menu');
        if (dropdown && localStorage.getItem('tour_completed')) {
            const tourItem = document.createElement('li');
            tourItem.innerHTML = '<a class="dropdown-item" href="#" id="retake-tour">Take Tour Again</a>';
            
            // Insert before logout if exists, otherwise at end
            const logoutItem = dropdown.querySelector('a[href="/logout"]')?.parentElement;
            if (logoutItem) {
                dropdown.insertBefore(tourItem, logoutItem);
            } else {
                dropdown.appendChild(tourItem);
            }
            
            // Add click handler
            document.getElementById('retake-tour').addEventListener('click', (e) => {
                e.preventDefault();
                localStorage.removeItem('tour_completed');
                window.location.href = '/diary';
            });
        }
    }

    /**
     * Resume tour if active (for page transitions)
     */
    resumeIfActive() {
        const tourActive = sessionStorage.getItem('tour_active');
        const tourPhase = parseInt(sessionStorage.getItem('tour_phase') || '0');
        
        if (tourActive === 'true' && !this.isActive) {
            this.isActive = true;
            this.currentPhase = tourPhase;
            
            // Resume appropriate phase based on page
            if (window.location.pathname.includes('/progress')) {
                this.showPhase('discovery');
            } else if (window.location.pathname.includes('/diary')) {
                // If back on diary after completion, finish tour
                this.completeTour();
            }
        }
    }
}

// Initialize tour when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    window.onboardingTour = new OnboardingTour();
    
    // Initialize or resume tour
    if (sessionStorage.getItem('tour_active') === 'true') {
        window.onboardingTour.resumeIfActive();
    } else {
        window.onboardingTour.init();
    }
});

// Handle page navigation during tour
window.addEventListener('beforeunload', function() {
    if (window.onboardingTour && window.onboardingTour.isActive) {
        // Tour state is preserved in sessionStorage
    }
});