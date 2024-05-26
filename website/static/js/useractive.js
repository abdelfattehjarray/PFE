$(document).ready(function() {
    // Handle "Active" button clicks
    $('.active-btn').click(function(event) {
      event.preventDefault(); // Prevent default form submission
      const form = $(this).closest('form');
      const userId = form.find('input[name="id"]').val();
  
      $.ajax({
        url: '/activate_user/', // Replace with your actual URL
        method: 'POST',
        data: {
          id: userId,
          csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val()
        },
        success: function(response) {
          // Handle success (e.g., refresh the page or update the UI)
          console.log(response);
          location.reload(); // Refresh to see changes
        },
        error: function(error) {
          console.error(error);
        }
      });
    });
  
    // Handle "Delete" button clicks (if necessary)
    $('.btn-danger').click(function(event) {
      event.preventDefault();
      // ... Your delete logic (similar to activate_user)
    });
  });