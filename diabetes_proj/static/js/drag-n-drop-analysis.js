var dropzone = document.getElementById('dropzone');
var fileInput = document.getElementById('fileInput');

dropzone.onclick = function() {
    fileInput.click();
};

dropzone.ondragover = function(e) {
    e.preventDefault();
};

dropzone.ondrop = function(e) {
    e.preventDefault();
    fileInput.files = e.dataTransfer.files;
    console.log('Я дошел сюда');
    document.getElementById('analysis_drag').submit();
};