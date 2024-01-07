function checkFileSize(event) {
    const file = event.target.files[0];
    const maxFileSize = 200 * 1024; // 100 KB
    const messageBox = document.getElementById("jsMessageBox");
    console.log('working');
    if (file && file.size > maxFileSize) {
        event.target.value = '';
        messageBox.textContent = "File exceeds max file size (100KB)";
    } else {
        messageBox.textContent = "";
    }
}