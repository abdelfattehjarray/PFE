document.addEventListener("DOMContentLoaded", function() {
  const fileInput = document.querySelector(".file-input");
  const uploadForm = document.getElementById("uploadForm");
  const submitButton = document.querySelector("#extractButton");
  const progressArea = document.querySelector(".progress-area");
  const uploadedArea = document.querySelector(".uploaded-area");

  submitButton.addEventListener("click", function(event) {
    event.preventDefault(); 
    uploadForm.submit(); 
  });


  

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

  // fileInput event listeners
  fileInput.addEventListener("change", function(event) {
    let file = this.files[0]; // Get the selected file
    if (file) {
      let fileName = file.name; // Get file name
      if (fileName.length >= 12) { // If file name length is greater than 12, truncate it
        let splitName = fileName.split('.');
        fileName = splitName[0].substring(0, 13) + "... ." + splitName[1];
      }
      uploadFile(file, fileName); // Call uploadFile function with the file and file name as arguments
    }
  });

  // Upload file function
function uploadFile(file, name) {
  let fileLoaded = 0;
  let fileSize = file.size;
  let progressHTML = `<li class="row">
                        <i class="fas fa-file-alt"></i>
                        <div class="content">
                          <div class="details">
                            <span class="name">${name} • Uploading</span>
                            <span class="percent">0%</span>
                          </div>
                          <div class="progress-bar">
                            <div class="progress" style="width: 0%"></div>
                          </div>
                        </div>
                      </li>`;
  uploadedArea.classList.add("onprogress");
  progressArea.innerHTML = progressHTML;

  // Simulate file upload progress
  let interval = setInterval(() => {
    fileLoaded += 1024 * 1024; // Simulate uploading 1 MB at a time
    let fileLoadedPercent = Math.floor((fileLoaded / fileSize) * 100);
    if (fileLoadedPercent > 100) {
      fileLoadedPercent = 100;
    }
    progressHTML = `<li class="row">
                      <i class="fas fa-file-alt"></i>
                      <div class="content">
                        <div class="details">
                          <span class="name">${name} • Uploading</span>
                          <span class="percent">${fileLoadedPercent}%</span>
                        </div>
                        <div class="progress-bar">
                          <div class="progress" style="width: ${fileLoadedPercent}%"></div>
                        </div>
                      </div>
                    </li>`;
    progressArea.innerHTML = progressHTML;
    if (fileLoaded >= fileSize) {
      clearInterval(interval);
      setTimeout(() => {
        let uploadedHTML = `<li class="row">
                              <div class="content upload">
                                <i class="fas fa-file-alt"></i>
                                <div class="details">
                                  <span class="name">${name} • Uploaded</span>
                                  <span class="size">${(fileSize / (1024 * 1024)).toFixed(2)} MB</span>
                                </div>
                              </div>
                              <i class="fas fa-check"></i>
                            </li>`;
        uploadedArea.classList.remove("onprogress");
        uploadedArea.insertAdjacentHTML("afterbegin", uploadedHTML);
        progressArea.innerHTML = "";
      }, 1000); // Simulate a delay before showing upload completion
    }
  }, 1000); // Simulate a delay before updating progress
}

});

