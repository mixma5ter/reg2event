$(document).ready(function () {
    $('#delete-button').click(function () {
        if (!confirm("Вы уверены, что хотите удалить этот элемент?")) {
            return false;
        }
    });
});