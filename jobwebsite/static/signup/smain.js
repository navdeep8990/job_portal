document.addEventListener("DOMContentLoaded", function () {
    // Set today's date as the max date for the birthday input
    const today = new Date().toISOString().split('T')[0];
    document.getElementById('birthday').setAttribute('max', today);
});
function validateForm() {
    const firstName = document.getElementById('first_name');
    const lastName = document.getElementById('last_name');
    const email = document.getElementById('email');
    const errorMessage = document.getElementById('error-message');
    const password = document.getElementById('password');


    errorMessage.style.display = 'none'; / /



    // Validate first name
    if (!firstName.value.match(/^[A-Za-z]+$/)) {
        errorMessage.textContent = 'First Name must contain only letters.';
        errorMessage.style.display = 'block';
        return false;
    }

    // Validate last name
    if (!lastName.value.match(/^[A-Za-z]+$/)) {
        errorMessage.textContent = 'Last Name must contain only letters.';
        errorMessage.style.display = 'block';
        return false;
    }

    // Validate email format
    if (!email.value.match(/^[a-zA-Z0-9._%+-]+@[a-zA-Z.-]+\.[a-zA-Z]{2,}$/)) {
        errorMessage.textContent = 'Invalid email format.';
        errorMessage.style.display = 'block';
        return false;
    }
    // Validate password
    if (password.value.length < 6) {
        errorMessage.textContent = 'Password must be at least 6 characters long.';
        errorMessage.style.display = 'block';
        return false;
    }

    return true; // Allow form submission
}