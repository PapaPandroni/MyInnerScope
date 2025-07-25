// Goals Page JavaScript
document.addEventListener('DOMContentLoaded', function() {
    const category_select = document.getElementById('category');
    const title_input = document.getElementById('title');
    const suggestions_container = document.getElementById('suggestions');
    const suggestions_list = document.getElementById('suggestions_list');
    
    // Goal suggestions functionality
    if (category_select && title_input) {
        category_select.addEventListener('change', function() {
            const selected_category = this.value;
            if (selected_category) {
                // Get CSRF token from meta tag
                const csrf_token = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
                
                fetch(`/api/goals/suggestions/${encodeURIComponent(selected_category)}`, {
                    headers: {
                        'X-CSRFToken': csrf_token
                    }
                })
                    .then(response => response.json())
                    .then(data => {
                        if (data.suggestions && data.suggestions.length > 0) {
                            suggestions_list.innerHTML = '';
                            data.suggestions.forEach(suggestion => {
                                const item = document.createElement('div');
                                item.className = 'suggestion_item';
                                item.textContent = suggestion;
                                item.addEventListener('click', function() {
                                    title_input.value = suggestion;
                                    suggestions_container.style.display = 'none';
                                });
                                suggestions_list.appendChild(item);
                            });
                            suggestions_container.style.display = 'block';
                        } else {
                            suggestions_container.style.display = 'none';
                        }
                    })
                    .catch(error => {
                        console.error('Error fetching suggestions:', error);
                        suggestions_container.style.display = 'none';
                    });
            } else {
                suggestions_container.style.display = 'none';
            }
        });
        
        // Hide suggestions when clicking outside
        document.addEventListener('click', function(e) {
            if (!suggestions_container.contains(e.target) && e.target !== category_select) {
                suggestions_container.style.display = 'none';
            }
        });
    }
    
    // Progress bar animation
    const progressBars = document.querySelectorAll('.progress-bar');
    progressBars.forEach(bar => {
        const width = bar.style.width;
        bar.style.width = '0%';
        setTimeout(() => {
            bar.style.width = width;
        }, 300);
    });
    
    // Form validation
    const goalForm = document.querySelector('form[action*="create_new_goal"]');
    if (goalForm) {
        goalForm.addEventListener('submit', function(e) {
            const category = document.getElementById('category').value;
            const title = document.getElementById('title').value.trim();
            
            if (!category) {
                e.preventDefault();
                showAlert('Please select a goal category.', 'warning');
                return false;
            }
            
            if (!title) {
                e.preventDefault();
                showAlert('Please enter a goal title.', 'warning');
                return false;
            }
        });
    }
    
    // Auto-save progress notes
    const progressTextarea = document.getElementById('progress_notes');
    if (progressTextarea) {
        let saveTimeout;
        progressTextarea.addEventListener('input', function() {
            clearTimeout(saveTimeout);
            saveTimeout = setTimeout(() => {
                // Auto-save functionality could be added here
                console.log('Progress notes changed:', this.value);
            }, 2000);
        });
    }
    
    // Goal completion confirmation
    const completeButtons = document.querySelectorAll('form[action*="mark_goal_complete"] button');
    completeButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            if (!confirm('Are you sure you want to mark this goal as completed?')) {
                e.preventDefault();
                return false;
            }
        });
    });
    
    // Utility function to show alerts
    function showAlert(message, type = 'info') {
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
        alertDiv.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        const container = document.querySelector('.container');
        container.insertBefore(alertDiv, container.firstChild);
        
        // Auto-dismiss after 5 seconds
        setTimeout(() => {
            if (alertDiv.parentNode) {
                alertDiv.remove();
            }
        }, 5000);
    }
    
    // Add hover effects to goal cards
    const goalCards = document.querySelectorAll('.goal-card');
    goalCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });
    
    // Animate stat numbers
    const statNumbers = document.querySelectorAll('.stat-number');
    statNumbers.forEach(stat => {
        const finalValue = parseFloat(stat.textContent);
        if (!isNaN(finalValue)) {
            animateNumber(stat, 0, finalValue, 1000);
        }
    });
    
    function animateNumber(element, start, end, duration) {
        const startTime = performance.now();
        const isPercentage = element.textContent.includes('%');
        
        function updateNumber(currentTime) {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);
            
            const current = start + (end - start) * progress;
            element.textContent = isPercentage ? 
                Math.round(current) + '%' : 
                Math.round(current);
            
            if (progress < 1) {
                requestAnimationFrame(updateNumber);
            }
        }
        
        requestAnimationFrame(updateNumber);
    }
    
    // Toggle extra goals in Recent Goals section
    window.toggle_extra_goals = function() {
        const extraGoals = document.querySelectorAll('.extra-goal');
        const btn = document.getElementById('show_more_goals_btn');
        let expanded = false;
        extraGoals.forEach(goal => {
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
}); 