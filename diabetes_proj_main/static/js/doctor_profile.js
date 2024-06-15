function copyHiddenText() {
    
    var textarea = document.createElement('textarea');
    textarea.value = document.querySelector('.hidden-text').textContent.trim();
    textarea.setAttribute('readonly', ''); 
    textarea.style.position = 'absolute';
    textarea.style.left = '-9999px';

    document.body.appendChild(textarea);

    textarea.select();
    document.execCommand('copy');

    document.body.removeChild(textarea);
}