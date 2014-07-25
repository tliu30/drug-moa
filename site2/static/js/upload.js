function uploadFile() {
    var xhr = new XMLHTTPRequest();

    // Make progress bar element
    var div = document.getElementById("progress");
    var progress = div.appendChild(document.createElement("p"));
    progress.appendChild(document.createTextNode("upload " + file.name));

    // Progress bar
    xhr.upload.addEventListener("progress",
        function(e) {
            var percent = parseInt(100 - (e.loaded / e.total * 100));
            progress.style.backgroundPosition = pc + "% 0";
        }, false);

    // File received/failed
    xhr.onreadystatechange = 
        function(e) {
            if (xhr.readyState == 4) {
                progress.className = (xhr.status == 200 ? "success" : "failure");
            }
        };

    // Start upload
    xhr.open("POST", $id("upload").action, true);
    xhr.setRequestHeader("X-FILENAME", file.name);
    xhr.send(file);
};
