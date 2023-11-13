document.addEventListener('DOMContentLoaded', function () {
    let count = 0;
    let maxFields = 500;
    let fieldsContainer = document.getElementById('fields');

    fieldsContainer.addEventListener('click', function (event) {
        if (event.target.classList.contains('remove-field-btn')) {
            event.target.parentNode.remove();
            count--;
            if (count < maxFields) {
                addFieldButton.disabled = false;
            }
        } else if (event.target.classList.contains('add-list-item-btn')) {
            let fieldIndex = event.target.parentNode.dataset.fieldIndex;
            let listItemHtml = `
                <div class="list-item">
                    <input type="text" name="custom-${fieldIndex}-list_item" required>
                    <button class="btn remove-list-item-btn">×</button>
                </div>
            `;
            let listContainer = event.target.parentNode.querySelector('.list-container');
            listContainer.insertAdjacentHTML('beforeend', listItemHtml);
        } else if (event.target.classList.contains('remove-list-item-btn')) {
            event.target.parentNode.remove();
        }
    });

    document.getElementById('add-field').addEventListener('click', function () {
        if (count < maxFields) {
            let fieldHtml = `
                <div class="form-field" data-field-index="${count}">
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
                        <option value="select">Список</option>
                        <option value="separator">Разделитель</option>
                    </select>
                    <div class="list-container"></div>
                    <button class="btn mb-4 add-list-item-btn" style="display: none;">Добавить элемент</button>
                    <button class="btn mb-4 remove-field-btn">Удалить поле</button>
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

    fieldsContainer.addEventListener('change', function (event) {
        if (event.target.tagName === 'SELECT') {
            let fieldType = event.target.value;
            let listContainer = event.target.parentNode.querySelector('.list-container');
            let addListItemButton = event.target.parentNode.querySelector('.add-list-item-btn');
            if (fieldType === 'select') {
                listContainer.innerHTML = '';
                let listItemHtml = `
                    <div class="list-item">
                        <input type="text" name="custom-${count - 1}-list_item" required>
                        <button class="btn remove-list-item-btn">×</button>
                    </div>
                `;
                listContainer.insertAdjacentHTML('beforeend', listItemHtml);
                addListItemButton.style.display = 'inline-block';
            } else {
                listContainer.innerHTML = '';
                addListItemButton.style.display = 'none';
            }
        }
    });
});