// cm.js

document.addEventListener('DOMContentLoaded', function() {
    const detailsButtons = document.querySelectorAll('.details-button');

    detailsButtons.forEach(button => {
        button.addEventListener('click', function() {
            const itemId = this.dataset.itemId;
            window.location.href = `/commandedetails?id=${itemId}`; // Assuming your URL pattern is like this
        });
    });
});