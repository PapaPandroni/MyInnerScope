/**
 * Improved Onboarding Tour Controller
 * Multi-page card-based onboarding experience
 */

class OnboardingTour {
    constructor() {
        this.isActive = false;
        this.currentPage = 0;
        this.currentTour = null;
        this.isNewUserTour = false; // Track if this is a new user tour vs auto-popup tour
        this.tours = this.initializeTours();
        
        // Bind methods to preserve context
        this.start = this.start.bind(this);
        this.skip = this.skip.bind(this);
        this.nextPage = this.nextPage.bind(this);
        this.prevPage = this.prevPage.bind(this);
        this.complete = this.complete.bind(this);
        this.startJourney = this.startJourney.bind(this);
        this.done = this.done.bind(this);
    }

    /**
     * Initialize tour content for each page
     */
    initializeTours() {
        return {
            diary: {
                pages: [
                    {
                        title: "Welcome to Your Inner Universe",
                        content: "In just a few minutes, you'll create your first reflection and discover how it becomes insight.",
                        icon: "fas fa-star"
                    },
                    {
                        title: "Daily Reflection Space",
                        content: "The core function of this page is to write daily diary entries about situations and your actions throughout the day. You can write as many entries as you like.",
                        icon: "fas fa-book"
                    },
                    {
                        title: "Self-Awareness Through Reflection",
                        content: "Reflect on your actions and behaviors. Are your actions today something you want to continue encouraging, or something you want to improve and change? Identifying your own behaviors is the first step to self-improvement.",
                        icon: "fas fa-mirror"
                    },
                    {
                        title: "Begin Your Journey",
                        content: "Start by writing your first diary entry and identify and categorize your behavior. Every great journey of self-discovery begins with a single step.",
                        icon: "fas fa-rocket",
                        isLast: true
                    }
                ]
            },
            progress: {
                pages: [
                    {
                        title: "Your Progress Dashboard",
                        content: "Welcome to your Progress Dashboard! This is where your daily reflections transform into meaningful insights about your personal growth journey.",
                        icon: "fas fa-chart-line"
                    },
                    {
                        title: "Track Your Growth",
                        content: "Track your progress over time through interactive charts and statistics. See patterns in your behavior and celebrate your consistency with streak tracking.",
                        icon: "fas fa-trophy"
                    },
                    {
                        title: "Behavior Insights",
                        content: "Your behavior cards show the balance between actions you want to encourage and those you want to improve. Watch your growth unfold as you continue your reflection practice.",
                        icon: "fas fa-balance-scale",
                        isDone: true
                    }
                ]
            },
            read_diary: {
                pages: [
                    {
                        title: "Your Reflection Archive",
                        content: "Welcome to your Reflection Archive! Here you can revisit and search through all your diary entries to discover patterns and insights.",
                        icon: "fas fa-archive"
                    },
                    {
                        title: "Search and Discover",
                        content: "Use the search feature to find specific moments, emotions, or situations. Filter by date or behavior type to focus on particular aspects of your growth.",
                        icon: "fas fa-search"
                    },
                    {
                        title: "Recognize Your Progress",
                        content: "Reading your past entries helps you recognize progress you might not have noticed. Your journey of self-awareness becomes clearer over time.",
                        icon: "fas fa-lightbulb",
                        isDone: true
                    }
                ]
            },
            goals: {
                pages: [
                    {
                        title: "Your Goal Setting Hub",
                        content: "Welcome to your Goal Setting Hub! Set meaningful weekly objectives that align with your personal growth journey.",
                        icon: "fas fa-target"
                    },
                    {
                        title: "Create Meaningful Goals",
                        content: "Create specific, actionable goals that connect to the behaviors you're working on. Focus on what you want to improve or encourage in yourself.",
                        icon: "fas fa-bullseye"
                    },
                    {
                        title: "Track Your Progress",
                        content: "Track your progress toward each goal and see how your daily diary entries contribute to achieving your objectives.",
                        icon: "fas fa-chart-bar"
                    },
                    {
                        title: "Set Your First Goal",
                        content: "Start by setting your first goal that supports your self-improvement journey. Small, consistent steps lead to remarkable transformation.",
                        icon: "fas fa-flag",
                        isDone: true
                    }
                ]
            }
        };
    }

    /**
     * Check if user should see the onboarding tour (for new users)
     */
    shouldShowTour() {
        const completed = localStorage.getItem('tour_completed');
        const is_new_user = window.tour_config?.is_new_user || false;
        const user_entry_count = window.tour_config?.user_entry_count || 0;
        
        return !completed && is_new_user && user_entry_count === 0;
    }

    /**
     * Check if user should see auto-popup tour for current page
     */
    shouldAutoStartTour() {
        const pageName = this.getCurrentPageName();
        const hasVisited = localStorage.getItem(`tour_visited_${pageName}`);
        
        // Only check if this specific page has been visited
        // Allow auto-popup tours even if global tour was completed on other pages
        return !hasVisited;
    }

    /**
     * Mark current page as visited
     */
    markPageVisited() {
        const pageName = this.getCurrentPageName();
        localStorage.setItem(`tour_visited_${pageName}`, 'true');
    }

    /**
     * Get current page name based on URL
     */
    getCurrentPageName() {
        const path = window.location.pathname;
        if (path.includes('/progress')) return 'progress';
        if (path.includes('/read')) return 'read_diary';
        if (path.includes('/goals')) return 'goals';
        return 'diary';
    }

    /**
     * Initialize and start the tour
     */
    init() {
        // Check for new user tour (original behavior)
        if (this.shouldShowTour()) {
            this.isNewUserTour = true;
            // Small delay to ensure page is fully loaded
            setTimeout(() => {
                this.start();
            }, 500);
        }
        // Check for auto-popup tour on first page visit
        else if (this.shouldAutoStartTour()) {
            this.isNewUserTour = false;
            // Small delay to ensure page is fully loaded
            setTimeout(() => {
                this.start();
            }, 1000); // Slightly longer delay for auto-popup
        }
        
        // Add "Take Tour Again" button to navbar
        this.addTourMenuOption();
    }

    /**
     * Start the onboarding tour for current page
     */
    start(pageName = null) {
        const currentPageName = pageName || this.getCurrentPageName();
        
        // Only start tour if we have content for this page
        if (!this.tours[currentPageName]) {
            return;
        }
        
        this.isActive = true;
        this.currentPage = 0;
        this.currentTour = this.tours[currentPageName];
        
        // Store tour state
        sessionStorage.setItem('tour_active', 'true');
        sessionStorage.setItem('tour_page', currentPageName);
        sessionStorage.setItem('tour_current_page', '0');
        
        // When manually starting tour (e.g., "Take Tour Again"), treat as auto-popup
        if (pageName !== null) {
            this.isNewUserTour = false;
        }
        
        this.showTourModal();
    }

    /**
     * Show the tour modal with current page content
     */
    showTourModal() {
        if (!this.currentTour || !this.currentTour.pages[this.currentPage]) {
            return;
        }
        
        const page = this.currentTour.pages[this.currentPage];
        const totalPages = this.currentTour.pages.length;
        
        // Create modal HTML
        const modalHTML = `
            <div class="modal fade tour-modal" id="tourModal" tabindex="-1" role="dialog" aria-labelledby="tourModalLabel" aria-hidden="true">
                <div class="modal-dialog modal-dialog-centered" role="document">
                    <div class="modal-content tour-modal-content">
                        <div class="modal-body text-center">
                            <div class="tour-cosmic-header">
                                <i class="${page.icon} tour-icon"></i>
                                <h2 class="tour-title">${page.title}</h2>
                                <p class="tour-content">${page.content}</p>
                            </div>
                            
                            <div class="tour-page-indicator">
                                <span class="tour-page-numbers">${this.currentPage + 1} / ${totalPages}</span>
                            </div>
                            
                            <div class="tour-navigation">
                                ${this.currentPage > 0 ? 
                                    '<button class="btn btn-outline-secondary tour-btn-prev" id="tour_prev_btn">Previous</button>' : 
                                    ''
                                }
                                
                                <button class="btn btn-outline-light tour-btn-skip" id="tour_skip_btn">Skip</button>
                                
                                ${page.isDone ? 
                                    '<button class="btn btn-primary tour-btn-primary" id="tour_done_btn"><i class="fas fa-check me-2"></i>Done</button>' :
                                    page.isLast ? 
                                        '<button class="btn btn-primary tour-btn-primary" id="tour_journey_btn"><i class="fas fa-rocket me-2"></i>Start Journey</button>' :
                                        '<button class="btn btn-primary tour-btn-primary" id="tour_next_btn">Next</button>'
                                }
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        // Remove existing modal if present
        const existingModal = document.getElementById('tourModal');
        if (existingModal) {
            existingModal.remove();
        }
        
        // Add modal to DOM
        document.body.insertAdjacentHTML('beforeend', modalHTML);
        
        // Add event listeners
        this.addModalEventListeners();
        
        // Show modal
        const modal = new bootstrap.Modal(document.getElementById('tourModal'));
        modal.show();
    }

    /**
     * Add event listeners to modal buttons
     */
    addModalEventListeners() {
        const prevBtn = document.getElementById('tour_prev_btn');
        const nextBtn = document.getElementById('tour_next_btn');
        const skipBtn = document.getElementById('tour_skip_btn');
        const journeyBtn = document.getElementById('tour_journey_btn');
        const doneBtn = document.getElementById('tour_done_btn');
        
        if (prevBtn) {
            prevBtn.addEventListener('click', this.prevPage);
        }
        
        if (nextBtn) {
            nextBtn.addEventListener('click', this.nextPage);
        }
        
        if (skipBtn) {
            skipBtn.addEventListener('click', this.skip);
        }
        
        if (journeyBtn) {
            journeyBtn.addEventListener('click', this.startJourney);
        }
        
        if (doneBtn) {
            doneBtn.addEventListener('click', this.done);
        }
    }

    /**
     * Go to next page
     */
    nextPage() {
        if (this.currentPage < this.currentTour.pages.length - 1) {
            this.currentPage++;
            sessionStorage.setItem('tour_current_page', this.currentPage.toString());
            this.hideModal(() => {
                this.showTourModal();
            });
        }
    }

    /**
     * Go to previous page
     */
    prevPage() {
        if (this.currentPage > 0) {
            this.currentPage--;
            sessionStorage.setItem('tour_current_page', this.currentPage.toString());
            this.hideModal(() => {
                this.showTourModal();
            });
        }
    }

    /**
     * Skip the tour and mark as completed
     */
    skip() {
        this.hideModal(() => {
            if (this.isNewUserTour) {
                this.completeGlobalTour();
            } else {
                this.completePageTour();
            }
        });
    }

    /**
     * Done button action (for final pages with isDone: true)
     */
    done() {
        this.hideModal(() => {
            if (this.isNewUserTour) {
                this.completeGlobalTour();
            } else {
                this.completePageTour();
            }
        });
    }

    /**
     * Start Journey button action (for diary and goals pages)
     */
    startJourney() {
        this.hideModal(() => {
            if (this.isNewUserTour) {
                this.completeGlobalTour();
            } else {
                this.completePageTour();
            }
            
            // Add specific actions for different pages
            const currentPageName = this.getCurrentPageName();
            if (currentPageName === 'diary') {
                // Focus on diary textarea
                const textarea = document.getElementById('diary_textarea');
                if (textarea) {
                    textarea.focus();
                }
            } else if (currentPageName === 'goals') {
                // Focus on goal title input
                const goalInput = document.querySelector('input[name="goal_title"], #goal-title');
                if (goalInput) {
                    goalInput.focus();
                }
            }
        });
    }

    /**
     * Hide modal with callback
     */
    hideModal(callback) {
        const modal = document.getElementById('tourModal');
        if (modal) {
            const bsModal = bootstrap.Modal.getInstance(modal);
            if (bsModal) {
                bsModal.hide();
            }
            
            // Remove after hide animation
            setTimeout(() => {
                modal.remove();
                if (callback) callback();
            }, 300);
        } else if (callback) {
            callback();
        }
    }

    /**
     * Mark tour as completed (for global new-user tours)
     */
    complete() {
        this.isActive = false;
        localStorage.setItem('tour_completed', 'true');
        sessionStorage.removeItem('tour_active');
        sessionStorage.removeItem('tour_page');
        sessionStorage.removeItem('tour_current_page');
        this.cleanup();
    }

    /**
     * Complete only the current page tour (for auto-popup tours)
     */
    completePageTour() {
        this.isActive = false;
        // Only mark this page as visited, don't set global completion
        this.markPageVisited();
        sessionStorage.removeItem('tour_active');
        sessionStorage.removeItem('tour_page');
        sessionStorage.removeItem('tour_current_page');
        this.cleanup();
        
        // Add "Take Tour Again" menu option now that a tour has been completed
        this.addTourMenuOption();
    }

    /**
     * Complete the global tour (for new user onboarding)
     */
    completeGlobalTour() {
        this.markPageVisited();
        this.complete();
        
        // Add "Take Tour Again" menu option now that a tour has been completed
        this.addTourMenuOption();
    }

    /**
     * Clean up tour elements
     */
    cleanup() {
        // Remove all tour-related elements
        document.querySelectorAll('.tour-modal').forEach(el => {
            el.remove();
        });
        
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
        if (dropdown) {
            // Check if menu item already exists to avoid duplicates
            const existingTourItem = dropdown.querySelector('#retake-tour');
            if (existingTourItem) {
                return; // Already exists, no need to add again
            }
            
            // Check if any tours have been seen (either completed globally or current page visited)
            const hasSeenAnyTour = localStorage.getItem('tour_completed') || 
                                 localStorage.getItem(`tour_visited_${this.getCurrentPageName()}`);
            
            if (hasSeenAnyTour) {
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
                    this.isNewUserTour = false; // Manual retake is treated as auto-popup
                    this.start();
                });
            }
        }
    }

    /**
     * Resume tour if active (for page transitions)
     */
    resumeIfActive() {
        const tourActive = sessionStorage.getItem('tour_active');
        const tourPage = sessionStorage.getItem('tour_page');
        const currentPageNum = parseInt(sessionStorage.getItem('tour_current_page') || '0');
        
        if (tourActive === 'true' && tourPage) {
            // Check if we're on the correct page
            const currentPageName = this.getCurrentPageName();
            if (currentPageName === tourPage) {
                this.isActive = true;
                this.currentPage = currentPageNum;
                this.currentTour = this.tours[tourPage];
                
                // Determine tour type based on how it was started
                this.isNewUserTour = this.shouldShowTour();
                
                // Resume tour
                setTimeout(() => {
                    this.showTourModal();
                }, 500);
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