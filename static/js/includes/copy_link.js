function copyToClipboard(text) {
    var button = document.getElementById('copy-button');
    var buttonText = button.innerHTML;
    button.innerHTML = 'Ссылка скопирована';
    button.disabled = true;

    var input = document.createElement('input');
    input.setAttribute('value', text);
    document.body.appendChild(input);
    input.select();
    document.execCommand('copy');
    document.body.removeChild(input);

    setTimeout(function () {
        button.innerHTML = buttonText;
        button.disabled = false;
    }, 3000); // возвращаем текст кнопки через 3 секунды
}