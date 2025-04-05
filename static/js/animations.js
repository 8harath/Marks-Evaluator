/**
 * Custom animations for the Essay Evaluation Platform
 */

// Function to animate numbers counting up
function animateCountUp(element) {
    const target = parseInt(element.textContent);
    const duration = 1500;
    let start = 0;
    const increment = target / 100;
    const startTime = Date.now();
    
    function updateNumber() {
        const currentTime = Date.now();
        const elapsed = currentTime - startTime;
        
        if (elapsed < duration) {
            const value = Math.min(Math.floor(start + (increment * (elapsed / (duration / 100)))), target);
            element.textContent = value;
            requestAnimationFrame(updateNumber);
        } else {
            element.textContent = target;
        }
    }
    
    updateNumber();
}

// Function to add animations to question cards
function animateQuestionCards() {
    const cards = document.querySelectorAll('.question-card');
    cards.forEach((card, index) => {
        card.style.animationDelay = `${index * 0.1}s`;
        card.classList.add('animate__animated', 'animate__fadeInUp');
    });
}

// Function to add hover effects to buttons
function addButtonHoverEffects() {
    const buttons = document.querySelectorAll('.btn');
    buttons.forEach(button => {
        button.addEventListener('mouseenter', function() {
            this.classList.add('animate__animated', 'animate__pulse');
        });
        
        button.addEventListener('mouseleave', function() {
            this.classList.remove('animate__animated', 'animate__pulse');
        });
    });
}

// Function to animate the page header
function animatePageHeader() {
    const pageTitle = document.querySelector('h1');
    if (pageTitle) {
        pageTitle.classList.add('animate__animated', 'animate__fadeInDown');
    }
    
    const pageSubtitle = document.querySelector('.lead');
    if (pageSubtitle) {
        pageSubtitle.classList.add('animate__animated', 'animate__fadeIn');
        pageSubtitle.style.animationDelay = '0.3s';
    }
}

// Initialize all animations when the DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Animate statistical counters
    const counters = document.querySelectorAll('.stats-card h3');
    counters.forEach(counter => {
        animateCountUp(counter);
    });
    
    // Add animations to question cards
    animateQuestionCards();
    
    // Add hover effects to buttons
    addButtonHoverEffects();
    
    // Animate page header
    animatePageHeader();
    
    // Add fade-in animation to alerts
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        alert.classList.add('animate__animated', 'animate__fadeIn');
    });
});
