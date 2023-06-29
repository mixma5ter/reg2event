document.addEventListener('DOMContentLoaded', function () {
    const message = document.querySelector('.alert');
    if (message) {
        setTimeout(function () {
            message.remove();
        }, 3000);
    }
});