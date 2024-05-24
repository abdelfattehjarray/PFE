
document.addEventListener('DOMContentLoaded', function() {
    const detailsButtons = document.querySelectorAll('.btn-danger');

    detailsButtons.forEach(button => {
        button.addEventListener('click', function() {
            const itemId = form.querySelector('input[name="supplier_id"]').value; 
            window.location.href = `/Fcommande?id=${itemId}`; // Assuming your URL pattern is like this
        });
    });
});