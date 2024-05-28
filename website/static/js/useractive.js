/*$(document).ready(function() {
    // Handle "Active" button clicks
    $('.active-btn').click(function(event) {
      event.preventDefault(); // Prevent default form submission
      const form = $(this).closest('form');
      const userId = form.find('input[name="id"]').val();
      const permission = form.find('select[name="permission"]').val();

  
      $.ajax({
        url: '/activate_user/', // Replace with your actual URL
        method: 'POST',
        data: {
          id: userId,
          permission: permission,
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
*/

$(document).ready(function() {
  $('.active-btn, .btn-danger').click(function(event) {
        event.preventDefault(); 
        const form = $(this).closest('form');
        const userId = form.find('input[name="id"]').val();
        const permission = form.find('select[name="permission"]').val();

        if ($(this).hasClass('active-btn')) {
            // Handle "Active" button click
            $.ajax({
                url: '/activate_user/', 
                method: 'POST',
                data: {
                    id: userId,
                    permission: permission,
                    csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val()
                },
                success: function(response) {
                    console.log(response);
                    location.reload();
                },
                error: function(error) {
                    console.error(error);
                }
            });
        } else if ($(this).hasClass('btn-danger')) {
            // Handle "Delete" button click
            // You might want to add a confirmation dialog here
            form.submit(); 
        }
  });
});