// Mobile Navigation Toggle
document.addEventListener('DOMContentLoaded', function() {
    const hamburger = document.querySelector('.hamburger');
    const navMenu = document.querySelector('.nav-menu');
    
    if (hamburger && navMenu) {
        hamburger.addEventListener('click', function() {
            hamburger.classList.toggle('active');
            navMenu.classList.toggle('active');
        });
        
        // Close menu when clicking on a link
        document.querySelectorAll('.nav-link').forEach(link => {
            link.addEventListener('click', () => {
                hamburger.classList.remove('active');
                navMenu.classList.remove('active');
            });
        });
    }
    
    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                const offsetTop = target.offsetTop - 70; // Account for fixed navbar
                window.scrollTo({
                    top: offsetTop,
                    behavior: 'smooth'
                });
            }
        });
    });
    
    // Add fade-in animation to elements
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in-up');
            }
        });
    }, observerOptions);
    
    // Observe elements for animation
    document.querySelectorAll('.hero-content, .rsvp-container, .faq-container, .admin-container').forEach(el => {
        observer.observe(el);
    });
    
    // Auto-hide flash messages after 5 seconds
    const flashMessages = document.querySelectorAll('.flash-message');
    flashMessages.forEach(message => {
        setTimeout(() => {
            message.style.opacity = '0';
            setTimeout(() => {
                message.remove();
            }, 300);
        }, 5000);
    });
    
    // FAQ Toggle
    document.querySelectorAll('.faq-question').forEach(question => {
        question.addEventListener('click', () => {
            const answer = question.nextElementSibling;
            const icon = question.querySelector('i');
            
            // Close other open FAQs
            document.querySelectorAll('.faq-answer').forEach(otherAnswer => {
                if (otherAnswer !== answer) {
                    otherAnswer.classList.remove('active');
                    otherAnswer.previousElementSibling.querySelector('i').style.transform = 'rotate(0deg)';
                }
            });
            
            // Toggle current FAQ
            answer.classList.toggle('active');
            icon.style.transform = answer.classList.contains('active') ? 'rotate(180deg)' : 'rotate(0deg)';
        });
    });
    
    // Multi-step RSVP Form
    const form = document.getElementById('rsvp-form');
    const steps = document.querySelectorAll('.form-step');
    const prevBtn = document.getElementById('prev-btn');
    const nextBtn = document.getElementById('next-btn');
    const submitBtn = document.getElementById('submit-btn');
    const confirmation = document.getElementById('confirmation');
    const guestCount = document.getElementById('guest-count');
    const nameFields = document.getElementById('name-fields');
    const largeGroupNote = document.getElementById('large-group-note');
    let currentStep = 0;

    if (form && steps.length > 0) {
        // Set accommodation toggle to checked by default
        const accommodationToggle = document.getElementById('accommodation-toggle');
        if (accommodationToggle) {
            accommodationToggle.checked = true;
            console.log('Accommodation toggle set to checked:', accommodationToggle.checked);
        }
        
        // Update name fields based on guest count
        guestCount.addEventListener('change', () => {
            const count = guestCount.value;
            nameFields.innerHTML = ''; // Clear existing fields

            // Add explanatory text
            const explanation = document.createElement('p');
            explanation.style.cssText = 'font-family: "Montserrat", sans-serif; font-size: 14px; color: #6B5B47; margin-bottom: 10px; font-style: italic;';
            explanation.textContent = 'Primary contact name will be automatically included. Add additional guests below.';
            nameFields.appendChild(explanation);

            const numFields = parseInt(count) || 1;
            // Only create fields for additional guests (skip the first one as it's the primary contact)
            for (let i = 1; i < numFields; i++) {
                const input = document.createElement('input');
                input.type = 'text';
                input.name = 'guest_names[]';
                input.placeholder = `Additional guest ${i} name`;
                input.required = true;
                input.style.cssText = 'width: 100%; padding: 12px; font-family: "Montserrat", sans-serif; font-size: 16px; border: 1px solid #D3D3D3; border-radius: 8px; margin-bottom: 10px;';
                nameFields.appendChild(input);
            }
        });

        // Show current step
        function showStep(step) {
            steps.forEach((s, index) => {
                s.style.display = index === step ? 'block' : 'none';
            });
            prevBtn.style.display = step === 0 ? 'none' : 'inline-block';
            nextBtn.style.display = step === steps.length - 1 ? 'none' : 'inline-block';
            submitBtn.style.display = step === steps.length - 1 ? 'inline-block' : 'none';
        }

        // Initial step
        showStep(currentStep);

        // Next button
        nextBtn.addEventListener('click', () => {
            if (currentStep < steps.length - 1) {
                currentStep++;
                showStep(currentStep);
            }
        });

        // Previous button
        prevBtn.addEventListener('click', () => {
            if (currentStep > 0) {
                currentStep--;
                showStep(currentStep);
            }
        });

        // Button hover effects
        [nextBtn, submitBtn].forEach(btn => {
            if (btn) {
                btn.addEventListener('mouseover', () => btn.style.background = '#2B4A5A');
                btn.addEventListener('mouseout', () => btn.style.background = '#1A2E35');
            }
        });
    }

    // RSVP Form AJAX Submission
    if (form) {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Process form data for toggle switches
            const formData = new FormData(this);
            
            // Handle toggle switch values - set to 'not_attending' if not checked
            const toggleFields = ['wedding_attendance', 'welcome_lunch', 'farewell_lunch'];
            toggleFields.forEach(field => {
                if (!formData.has(field)) {
                    formData.set(field, 'not_attending');
                }
            });
            
            // Handle accommodation toggle - default to 'yes' if checked, 'no' if not
            if (!formData.has('accommodation')) {
                formData.set('accommodation', 'no');
            }
            
            // Add primary contact name to guest names array
            const primaryName = formData.get('name');
            const existingGuestNames = formData.getAll('guest_names[]');
            const allGuestNames = [primaryName, ...existingGuestNames];
            
            // Clear existing guest_names and add all names
            formData.delete('guest_names[]');
            allGuestNames.forEach(name => {
                if (name && name.trim()) {
                    formData.append('guest_names[]', name.trim());
                }
            });
            
            // Show loading state
            submitBtn.style.background = '#666';
            submitBtn.disabled = true;
            submitBtn.textContent = 'Submitting...';
            
            // Submit form via AJAX
            fetch('/submit_rsvp', {
                method: 'POST',
                body: formData
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                if (data.success) {
                    // Hide the form immediately after successful submission
                    form.style.display = 'none';
                    
                    // Show success modal or confirmation message
                    const modal = document.getElementById('success-modal');
                    if (modal) {
                        modal.style.display = 'flex';
                    } else {
                        // Fallback: show confirmation message
                        const confirmation = document.getElementById('confirmation');
                        if (confirmation) {
                            confirmation.style.display = 'block';
                        }
                    }
                    
                    // Reset button state
                    submitBtn.style.background = '#1A2E35';
                    submitBtn.disabled = false;
                    submitBtn.textContent = 'Submit RSVP';
                } else {
                    // Show error modal or alert
                    const modal = document.getElementById('error-modal');
                    if (modal) {
                        const errorMessage = document.getElementById('error-message');
                        if (errorMessage) {
                            errorMessage.textContent = data.message || 'There was an error submitting your RSVP. Please try again.';
                        }
                        modal.style.display = 'flex';
                    } else {
                        // Fallback: show alert
                        alert(data.message || 'There was an error submitting your RSVP. Please try again.');
                    }
                    // Reset button state
                    submitBtn.style.background = '#1A2E35';
                    submitBtn.disabled = false;
                    submitBtn.textContent = 'Submit RSVP';
                }
            })
            .catch(error => {
                console.error('Error:', error);
                // Show error modal or alert
                const modal = document.getElementById('error-modal');
                if (modal) {
                    const errorMessage = document.getElementById('error-message');
                    if (errorMessage) {
                        errorMessage.textContent = 'Network error. Please check your connection and try again.';
                    }
                    modal.style.display = 'flex';
                } else {
                    // Fallback: show alert
                    alert('Network error. Please check your connection and try again.');
                }
                // Reset button state
                submitBtn.style.background = '#1A2E35';
                submitBtn.disabled = false;
                submitBtn.textContent = 'Submit RSVP';
            });
        });
    }
    
    // Modal functions
    window.showModal = function(type, message = '') {
        const modal = document.getElementById(type + '-modal');
        if (modal) {
            if (type === 'error' && message) {
                const errorMessage = document.getElementById('error-message');
                if (errorMessage) {
                    errorMessage.textContent = message;
                }
            }
            modal.style.display = 'flex';
        }
    };
    
    window.closeModal = function() {
        document.querySelectorAll('.modal').forEach(modal => {
            modal.style.display = 'none';
        });
        
        // Reset form state if there was an error
        const submitBtn = document.getElementById('submit-btn');
        if (submitBtn) {
            submitBtn.style.background = '#1A2E35';
            submitBtn.disabled = false;
            submitBtn.textContent = 'Submit RSVP';
        }
    };
    
    // Close modal when clicking outside
    document.querySelectorAll('.modal').forEach(modal => {
        modal.addEventListener('click', function(e) {
            if (e.target === this) {
                closeModal();
            }
        });
    });
    
    // Form validation enhancements
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const requiredFields = form.querySelectorAll('[required]');
            let isValid = true;
            
            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    isValid = false;
                    field.style.borderColor = '#dc3545';
                    field.style.boxShadow = '0 0 0 3px rgba(220, 53, 69, 0.1)';
                } else {
                    field.style.borderColor = '#e8e4e0';
                    field.style.boxShadow = 'none';
                }
            });
            
            if (!isValid) {
                e.preventDefault();
                alert('Please fill in all required fields.');
            }
        });
    });
    
    // Email validation
    const emailInputs = document.querySelectorAll('input[type="email"]');
    emailInputs.forEach(input => {
        input.addEventListener('blur', function() {
            const email = this.value;
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            
            if (email && !emailRegex.test(email)) {
                this.style.borderColor = '#dc3545';
                this.style.boxShadow = '0 0 0 3px rgba(220, 53, 69, 0.1)';
            } else if (email) {
                this.style.borderColor = '#28a745';
                this.style.boxShadow = '0 0 0 3px rgba(40, 167, 69, 0.1)';
            }
        });
    });
    
    // Parallax effect for hero section
    const heroSection = document.querySelector('.hero-section');
    if (heroSection) {
        window.addEventListener('scroll', function() {
            const scrolled = window.pageYOffset;
            const rate = scrolled * -0.5;
            heroSection.style.transform = `translateY(${rate}px)`;
        });
    }
    
    // Countdown timer for Crystal & Yang's wedding (May 12, 2026 at 2 PM)
    const weddingDate = new Date('2026-05-12T14:00:00');
    const daysElement = document.getElementById('days');
    const hoursElement = document.getElementById('hours');
    const minutesElement = document.getElementById('minutes');
    const secondsElement = document.getElementById('seconds');
    
    if (daysElement && hoursElement && minutesElement && secondsElement) {
        function updateCountdown() {
            const now = new Date().getTime();
            const distance = weddingDate.getTime() - now;
            
            if (distance > 0) {
                const days = Math.floor(distance / (1000 * 60 * 60 * 24));
                const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
                const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
                const seconds = Math.floor((distance % (1000 * 60)) / 1000);
                
                daysElement.textContent = days;
                hoursElement.textContent = hours.toString().padStart(2, '0');
                minutesElement.textContent = minutes.toString().padStart(2, '0');
                secondsElement.textContent = seconds.toString().padStart(2, '0');
            } else {
                // Wedding day has passed - count days since
                const daysSince = Math.floor(Math.abs(distance) / (1000 * 60 * 60 * 24));
                const hoursSince = Math.floor((Math.abs(distance) % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
                const minutesSince = Math.floor((Math.abs(distance) % (1000 * 60 * 60)) / (1000 * 60));
                const secondsSince = Math.floor((Math.abs(distance) % (1000 * 60)) / 1000);
                
                daysElement.textContent = daysSince;
                hoursElement.textContent = hoursSince.toString().padStart(2, '0');
                minutesElement.textContent = minutesSince.toString().padStart(2, '0');
                secondsElement.textContent = secondsSince.toString().padStart(2, '0');
                
                // Update the countdown label
                const countdownLabel = document.querySelector('.countdown-label');
                if (countdownLabel) {
                    if (daysSince === 0) {
                        countdownLabel.textContent = '🎉 Today is our special day! 🎉';
                    } else {
                        countdownLabel.textContent = `Days since our special day 💕`;
                    }
                }
            }
        }
        
        updateCountdown();
        setInterval(updateCountdown, 1000);
    }
});

// Utility functions
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 1rem 1.5rem;
        border-radius: 8px;
        color: white;
        font-weight: 500;
        z-index: 10000;
        animation: slideInRight 0.3s ease;
        max-width: 300px;
    `;
    
    if (type === 'success') {
        notification.style.backgroundColor = '#28a745';
    } else if (type === 'error') {
        notification.style.backgroundColor = '#dc3545';
    } else {
        notification.style.backgroundColor = '#17a2b8';
    }
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.animation = 'slideOutRight 0.3s ease';
        setTimeout(() => {
            notification.remove();
        }, 300);
    }, 3000);
}

// Add CSS animations
const style = document.createElement('style');
style.textContent = `
    @keyframes slideInRight {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOutRight {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
    

`;
document.head.appendChild(style);
