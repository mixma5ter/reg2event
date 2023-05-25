$(document).ready(function () {
    var count = 0;
    var maxFields = 2;
    $("#add-field").on("click", function () {
        if (count < maxFields) {
            var fieldHtml = `
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
            $("#fields").append(fieldHtml);
            count++;
            if (count === maxFields) {
                $("#add-field").prop("disabled", true);
            }
        }
    });
    $("#fields").on("click", ".remove-field-btn", function () {
        $(this).parent().remove();
        count--;
        if (count < maxFields) {
            $("#add-field").prop("disabled", false);
        }
    });
});