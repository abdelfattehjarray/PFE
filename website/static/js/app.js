const sign_in_btn = document.querySelector("#sign-in-btn");
const sign_up_btn = document.querySelector("#sign-up-btn");
const container = document.querySelector(".container");
const signupForm = document.querySelector("#sign-up-form");
const signupMessages = document.getElementById('signup-messages'); // Get the div for messages

sign_up_btn.addEventListener("click", () => {
  container.classList.add("sign-up-mode");
});

sign_in_btn.addEventListener("click", () => {
  container.classList.remove("sign-up-mode");
});

signupForm.addEventListener("submit", (event) => {
  event.preventDefault(); // Prevent default form submission

  const formData = new FormData(signupForm);

  fetch(UserURL, { // Use the correct URL for your view
    method: 'POST',
    body: formData
  })
  .then(response => {
      if (response.ok) {
        return response.json();
      } else {
        throw new Error('Error during signup');
      }
    })
    .then(data => {
      if (data.success) { 
        // Success - display success message
        signupMessages.innerHTML = `<p class="success">account created, wait for verification...</p>`;
        signupForm.reset();
      } else if (data.errors) {
        // Error - display error message(s)
        let errorMessage = '<ul class="errors">';
        data.errors.forEach(error => errorMessage += `<li>${error}</li>`);
        errorMessage += '</ul>';
        signupMessages.innerHTML = errorMessage;
      } else {
        // Handle unexpected response
        signupMessages.innerHTML = '<p class="error">Unexpected error occurred.</p>';
      }
    })
    .catch(error => {
      // Handle general errors
      console.error("Error during signup:", error);
      signupMessages.innerHTML = '<p class="error">An error occurred. Please try again.</p>';
    });
 
});