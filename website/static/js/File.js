document.addEventListener("DOMContentLoaded", function() {

  // Add event listener to the whole form
  uploadForm.addEventListener('click', function() {
    // Simulate a click on the file input
    fileInput.click();
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
  document.getElementById('idp').value = 'idp'; // Adjust as needed
  document.getElementById('namep').value = data.pname;
  document.getElementById('characteristic').value = data.pchar;

  // Commande data
  document.getElementById('id').value = 'id'; // Adjust as needed
  document.getElementById('product').value = data.pname;
  document.getElementById('quantity').value = data.quantity;
  document.getElementById('unite').value = data.unity;
  document.getElementById('prixindiv').value = data.prixi;
  document.getElementById('prixtotal').value = data.prixt;
  document.getElementById('somme').value = data.somme;

  // Client data
  document.getElementById('idc').value = 'idc'; // Adjust as needed
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
