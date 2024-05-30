/*
document.addEventListener('DOMContentLoaded', function() {
    const detailsButtons = document.querySelectorAll('.details-button');

    detailsButtons.forEach(button => {
        button.addEventListener('click', function() {
            const itemId = this.dataset.itemId;
            window.location.href = `/Fcommande?id=${itemId}`; // Assuming your URL pattern is like this
        });
    });
});*/




document.addEventListener('DOMContentLoaded', function() {
    const detailsButtons = document.querySelectorAll('.details-button');
    const deleteButtons = document.querySelectorAll('.btn-danger'); 
    detailsButtons.forEach(button => {
        button.addEventListener('click', function() {
            const itemId = this.dataset.itemId;
            window.location.href = `/Fcommande?id=${itemId}`; 
        });
    });

    deleteButtons.forEach(button => {
        button.addEventListener('click', function(event) {
            event.preventDefault(); 
            const form = button.closest('form'); 

            
            if (confirm('Are you sure you want to delete this item?')) {
                form.submit(); 
            }
        });
    });
});