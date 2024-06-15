document.addEventListener('DOMContentLoaded', function() {
    const addButton = document.getElementById('add-food-item-btn');
    const formContainer = document.getElementById('food-item-forms');
    let formCount = 1;

    addButton.addEventListener('click', function() {
        const formPrefix = `food_item_${formCount}`;
        const formHtml = `
            <div class="food-item-form">
                <label for="${formPrefix}-name">Назва продукту:</label>
                <input type="text" name="${formPrefix}-name" id="${formPrefix}-name" class="form-control">
                <label for="${formPrefix}-proteins">Білки:</label>
                <input type="text" name="${formPrefix}-proteins" id="${formPrefix}-proteins" class="form-control">
                <label for="${formPrefix}-fats">Жири:</label>
                <input type="text" name="${formPrefix}-fats" id="${formPrefix}-fats" class="form-control">
                <label for="${formPrefix}-carbohydrates">Вуглеводи:</label>
                <input type="text" name="${formPrefix}-carbohydrates" id="${formPrefix}-carbohydrates" class="form-control">
            </div>
        `;
        formContainer.insertAdjacentHTML('beforeend', formHtml);
        formCount++;
    });

    const form = document.getElementById('food-measurement-form');
    form.addEventListener('submit', function(event) {
        
        const allForms = document.querySelectorAll('.food-item-form input');
        let isValid = true;
        allForms.forEach(input => {
            if (input.required && !input.value.trim()) {
                isValid = false;
            }
        });

        if (!isValid) {
            event.preventDefault();
            alert('Заполните все обязательные поля продуктов');
        }
    });
});