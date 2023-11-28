document.addEventListener('DOMContentLoaded', function() {

    // Handle registration form submission
    const registerForm = document.getElementById('register-form');
    if (registerForm) {
        registerForm.addEventListener('submit', function(event) {
            event.preventDefault();
            submitForm(this, '/register');
        });
    }

    // Handle login form submission
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', function(event) {
            event.preventDefault();
            submitForm(this, '/login');
        });
    }

    // Handle admin action form submission
    const adminForm = document.getElementById('admin-form');
    if (adminForm) {
        adminForm.addEventListener('submit', function(event) {
            event.preventDefault();
            submitForm(this, '/admin');
        });
    }

    // Generic form submission handler
    function submitForm(form, url) {
        const formData = new FormData(form);

        fetch(url, {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                console.log('Action successful:', data.message);
                // Update UI or redirect as needed
            } else {
                console.error('Action failed:', data.message);
                // Show error feedback on UI
            }
        })
        .catch(error => {
            console.error('Fetch error:', error);
        });
    }

});
