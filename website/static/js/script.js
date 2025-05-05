
document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM fully loaded and parsed');

    const signInButton = document.getElementById('signInBtn');
    if (signInButton) {
        const popover = new bootstrap.Popover(signInButton);
        popover.show();

    }

    const buttons = document.querySelectorAll('.btn:not(#signInBtn)');
    buttons.forEach(button => {
        button.addEventListener('click', function(e) {

            console.log('Button clicked:', this.textContent);
        });
    });
});
