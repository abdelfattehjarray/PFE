// cm.js
/*
document.addEventListener('DOMContentLoaded', function() {
    const detailsButtons = document.querySelectorAll('.details-button');

    detailsButtons.forEach(button => {
        button.addEventListener('click', function() {
            const itemId = this.dataset.itemId;
            window.location.href = `/commandedetails?id=${itemId}`; // Assuming your URL pattern is like this
        });
    });
});
*/




document.addEventListener('DOMContentLoaded', function() {
    const detailsButtons = document.querySelectorAll('.details-button');
    const deleteButtons = document.querySelectorAll('.btn-danger'); // Assuming you use a specific class for delete buttons

    detailsButtons.forEach(button => {
        button.addEventListener('click', function() {
            const itemId = this.dataset.itemId;
            window.location.href = `/commandedetails?id=${itemId}`; 
        });
    });

    deleteButtons.forEach(button => {
        button.addEventListener('click', function(event) {
            event.preventDefault(); // Prevent form submission
            const form = button.closest('form'); // Get the parent form

            // Confirm deletion with a popup
            if (confirm('Are you sure you want to delete this order?')) {
                form.submit(); // Submit the form if confirmed
            }
        });
    });
});