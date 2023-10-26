document.addEventListener('DOMContentLoaded', function () {
    let count = 0;
    let maxFields = 20;
    let addFieldButton = document.getElementById('add-field');
    let fieldsContainer = document.getElementById('fields');

    addFieldButton.addEventListener('click', function () {
        if (count < maxFields) {
            let fieldHtml = `
                <div class="form-field">
                    <label for="custom-${count}-input">Название поля:</label>
                    <input type="text" name="custom_field-${count}-label" required id="custom-${count}-input">
                    <label for="custom-${count}-input">Тип поля:</label>
                    <select name="custom-${count}-field_type">
                        <option value="text">Текст</option>
                        <option value="textarea">Текстовое поле</option>
                        <option value="number">Число</option>
                        <option value="email">Email</option>
                        <option value="phone">Телефон</option>
                        <option value="checkbox">Чекбокс</option>
                    </select>
                    <button class="btn remove-field-btn">Удалить поле</button>
                    <hr>
                </div>
            `;
            fieldsContainer.insertAdjacentHTML('beforeend', fieldHtml);
            count++;
            if (count === maxFields) {
                addFieldButton.disabled = true;
            }
        }
    });

    fieldsContainer.addEventListener('click', function (event) {
        if (event.target.classList.contains('remove-field-btn')) {
            event.target.parentNode.remove();
            count--;
            if (count < maxFields) {
                addFieldButton.disabled = false;
            }
        }
    });
});