document.addEventListener('DOMContentLoaded', function(){

    var navUpLink = document.getElementById('linkUP');
    var patientBtn = document.getElementById('patient__btn');
    var patientFormSection = document.getElementById('patient__form');
    var optionChoiceSection = document.getElementById('options');
    
    patientBtn.addEventListener('click', function () {
        optionChoiceSection.style.display = 'none';
        patientFormSection.style.display = 'block';
        patientFormSection.scrollIntoView({ behavior: 'smooth' });
    });

    navUpLink.addEventListener('click', function(){
        optionChoiceSection.scrollIntoView({behavior: 'smooth'});
        patientFormSection.style.display = 'none';
        optionChoiceSection.style.display = 'block';
    });

});