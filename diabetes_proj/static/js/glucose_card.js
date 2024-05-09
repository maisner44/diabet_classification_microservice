document.addEventListener("DOMContentLoaded", function() {
    var dropdowns = document.querySelectorAll('.dropdown');

    dropdowns.forEach(function(dropdown) {

        dropdown.addEventListener('mouseenter', function() {
            this.querySelector('.dropdown-menu').classList.add('show');
        });
        dropdown.addEventListener('mouseleave', function() {
            this.querySelector('.dropdown-menu').classList.remove('show');
        });
    });


    var glucoseMeasElements = document.querySelectorAll('.glucose-block');

    glucoseMeasElements.forEach(function(glucoseMeas) {
        var glucoseValueSpan = glucoseMeas.querySelector('.glucose_value');

        if (glucoseValueSpan) {
            var glucoseValueText = glucoseValueSpan.innerText;
            var glucoseValue = parseFloat(glucoseValueText);
            console.log(glucoseValue);

            if (!isNaN(glucoseValue)) {
                if (glucoseValue <= 3 || glucoseValue > 6) {
                    glucoseMeas.classList.add('bad');
                }
            }
        }
    });
});