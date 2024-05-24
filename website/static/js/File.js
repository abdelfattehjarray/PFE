document.addEventListener("DOMContentLoaded", function() {

  // Add event listener to the whole form
  uploadForm.addEventListener('click', function(event) {
    // Simulate a click on the file input
    
        fileInput.click(); 
        console.log(event.target)
    
  });

  fileInput.removeEventListener("change", () => uploadForm.submit());

  

  document.querySelector("#viewdata").addEventListener("click", function(){
    document.querySelector(".popup").classList.add("active");
    document.querySelector(".wrapper").style.display = "none"; 
    // Hide the wrapper
  });

  document.querySelector(".popup .close-btn").addEventListener("click", function(){
    document.querySelector(".popup").classList.remove("active");
    document.querySelector(".wrapper").style.display = "block"; // Show the wrapper
  });


});





const uploadForm = document.getElementById('uploadForm');
const fileInput = document.querySelector('.file-input');
const extractButton = document.getElementById('extractButton');
const saveForm = document.getElementById('saveform');
const popup = document.querySelector('.popup');
const loading = document.getElementById('loading');
const viewdataButton = document.getElementById('viewdata'); // Get the viewdata button

// Function to show the popup
function showPopup() {
    popup.style.display = 'block';
}

// Function to hide the popup
function hidePopup() {
    popup.style.display = 'none';
    document.querySelector(".wrapper").style.display = "block";
}

fileInput.addEventListener('change', () => {
    const fileName = fileInput.files[0].name;
    document.querySelector('.uploaded-area').innerHTML = fileName;
});

extractButton.addEventListener('click', (event) => {
    event.preventDefault();

    const fileError = document.getElementById('fileError');

    // Check if a file is selected
    if (fileInput.files.length === 0) {
        fileError.textContent = "No file selected.";
        fileError.style.display = 'block';
        return; // Don't proceed with extraction
    } else {
        // Hide the error message if it was previously displayed
        fileError.style.display = 'none'; 
    }





    const formData = new FormData(uploadForm);

    loading.style.display = 'block'; 
    extractButton.disabled = true; 
    viewdataButton.disabled = true; 

    fetch('', {
        method: 'POST',
        body: formData,
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        populateSaveForm(data);
        loading.style.display = 'none'; 
        extractButton.disabled = false; 
        viewdataButton.disabled = false; 

        
    })
    .catch(error => {
        console.error('There has been a problem with your fetch operation:', error);
        loading.style.display = 'none';
        extractButton.disabled = false; 
        viewdataButton.disabled = false; 

    });
});

function populateSaveForm(data) {
  // Fournisseur data
  document.getElementById('identificateur').value = data.identificateur;
  document.getElementById('name').value = data.name;
  document.getElementById('adresse').value = data.address;
  document.getElementById('sujet').value = data.sujet;
  document.getElementById('consultation').value = data.consultation;

  // Produit data
  document.getElementById('namep').value = data.pname;
  document.getElementById('characteristic').value = data.pchar;

  // Commande data
  document.getElementById('product').value = data.pname;
  document.getElementById('quantity').value = data.quantity;
  document.getElementById('unite').value = data.unity;
  document.getElementById('prixindiv').value = data.prixi;
  document.getElementById('prixtotal').value = data.prixt;
  document.getElementById('somme').value = data.somme;

  // Client data
  document.getElementById('namec').value = data.cname;
  document.getElementById('adressec').value = data.caddress;
  document.getElementById('mail').value = data.cmail;
  document.getElementById('phone').value = data.cphone;
  document.getElementById('fax').value = data.cfax;
  document.getElementById('taxid').value = data.ctax;

  // BonCommande data
  document.getElementById('date').value = data.date; 
  document.getElementById('number').value = data.numero;
}

function displaySuccessMessage() {
    // Hide the popup
    hidePopup();

       // Create the success message element
       const successMessage = document.createElement('div');
       successMessage.classList.add('alert', 'alert-success');
       successMessage.innerHTML = `
           <span class="close-btn" onclick="closeSuccessMessage()">&times;</span>
           Data saved successfully.
       `;
       document.body.appendChild(successMessage);
       setTimeout(function() {
        successMessage.style.display = 'none';  }, 1500);
   }
// Function to close the success message
function closeSuccessMessage() {
    const successMessage = document.querySelector('.alert-success');
    if (successMessage) {
        successMessage.remove();
    }
}
// Add event listener to the save button
document.getElementById('savebutton').addEventListener('click', (event) => {
    event.preventDefault(); // Prevent default form submission
    const saveFormData = new FormData(saveForm); // Create FormData from saveForm
  
    fetch(saveDataURL, { 
        method: 'POST',
        body: saveFormData,
        headers: {
            'X-CSRFToken': getCookie('csrftoken') // Get the token from a cookie
        }
    })

    .then(response => {
        // Handle the response from your server
        displaySuccessMessage();
        hidePopup();

    })
    .catch(error => {
        console.error('Error:', error);
    });
       // Helper function to get the CSRF token from cookies
 
  }); 
  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}