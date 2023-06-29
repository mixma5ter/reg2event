document.addEventListener('DOMContentLoaded', function () {
    const deleteButton = document.getElementById('delete-button');
    if (deleteButton) {
        deleteButton.addEventListener('click', function () {
            if (!confirm("Вы уверены, что хотите удалить этот элемент?")) {
                return false;
            }
        });
    }
});