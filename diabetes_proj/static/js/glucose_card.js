document.addEventListener("DOMContentLoaded", function() {
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