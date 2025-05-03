// Custom JavaScript for your Flask application

// Document ready function
document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM fully loaded and parsed');
    
    // Add your JavaScript functionality here
    
    // Example: Add a click event to all buttons with the 'btn' class
    const buttons = document.querySelectorAll('.btn');
    buttons.forEach(button => {
        button.addEventListener('click', function(e) {
            console.log('Button clicked:', this.textContent);
        });
    });
});
