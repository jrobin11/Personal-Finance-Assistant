document.addEventListener('DOMContentLoaded', function() {

    // Handle registration form submission
    const registerForm = document.getElementById('registerForm');
    if (registerForm) {
        registerForm.addEventListener('submit', function(event) {
            event.preventDefault();
            submitForm(this, '/register');
        });
    }

    // Handle login form submission
    const loginForm = document.getElementById('loginForm');
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

    function submitForm(form, url) {
        const formData = new FormData(form);
    
        fetch(url, {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (response.ok) {
                if (url === '/login' && response.redirected) {
                    window.location.href = response.url;  // Redirect to the new URL
                } else {
                    return response.json();
                }
            } else {
                throw new Error('Network response was not ok.');
            }
        })
        .then(data => {
            if (data && !data.success) {
                // Handle failure
                alert(data.message);
            }
        })
        .catch(error => {
            console.error('Fetch error:', error);
        });
    }
    

});
