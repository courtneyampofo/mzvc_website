// Handle Login Form Submission
function handleLoginSubmit(e) {
    // TEMPORARILY DISABLED - Allow normal form submission
    // e.preventDefault();
    
    const form = e.target;
    const formData = new FormData(form);
    const username = formData.get('username');
    const password = formData.get('password');
    
    // Basic client-side validation
    if (!username || !password) {
        showError('Please fill in all fields');
        return;
    }
    
    if (username.length < 3) {
        showError('Username must be at least 3 characters long');
        return;
    }
    
    if (password.length < 6) {
        showError('Password must be at least 6 characters long');
        return;
    }
    
    // If validation passes, let the form submit normally
    // The server will handle the actual authentication
    form.submit();
}
