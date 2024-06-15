var dropzone = document.getElementById('dropzone');
var fileInput = document.getElementById('fileInput');
var error_block = document.getElementById('upload_error');

dropzone.onclick = function() {
    fileInput.click();
};

dropzone.ondragover = function(e) {
    e.preventDefault();
};

fileInput.onchange = function(e) {
    e.preventDefault();

    var file = fileInput.files[0];
    if (drop_validation(file)){
        return;
    }

    document.getElementById('analysis_drag').submit();
};

dropzone.ondrop = function(e) {
    e.preventDefault();
    fileInput.files = e.dataTransfer.files;

    var file = fileInput.files[0];
    if (drop_validation(file)){
        return;
    }

    document.getElementById('analysis_drag').submit();
};

function drop_validation(file){
    if (file.type != 'application/pdf'){
        error_block.style.display = 'block';
        error_block.innerText = 'Файл повинен бути в розширені .pdf';
        return;
    }
}