const fileInput = document.getElementById("image");
    const fileName = document.getElementById("file-name");

    fileInput.addEventListener("change", function () {
        fileName.textContent = this.files[0]?.name || "No file chosen";
    });