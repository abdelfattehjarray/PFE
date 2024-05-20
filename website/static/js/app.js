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
    if (data.success_message) {
      signupMessages.innerHTML = `<p class="success">${data.success_message}</p>`; // Display success message
      signupForm.reset(); // Reset the form
    } else if (data.error_message) {
      signupMessages.innerHTML = `<p class="error">${data.error_message}</p>`; // Display error message
    }
  })
  .catch(error => {
    console.error('Signup error:', error);
    signupMessages.innerHTML = `<p class="error">Une erreur s'est produite. Veuillez réessayer.</p>`;
  });
});