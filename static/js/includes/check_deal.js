let checkButton = document.getElementById('check-deal');
let dealInput = document.getElementById('id_deal_id');
let titleInput = document.getElementById('id_title');
let alertMessages = document.getElementById('alert-messages');

checkButton.addEventListener('click', function () {
    let dealId = dealInput.value;

    // Проверяем, является ли `dealId` числом
    if (!dealId) {
        return; // Прекращаем выполнение функции
    }

    // создаем элемент div для индикатора ожидания
    let loaderDiv = document.createElement('div');
    loaderDiv.classList.add('loader');

    // добавляем индикатор ожидания поверх всего контента
    document.body.appendChild(loaderDiv);

    // отправляем AJAX-запрос на сервер для проверки deal_id
    fetch(`/events/forms/check_deal/${dealId}/`)
        .then(response => response.json())
        .then(data => {
            // удаляем индикатор ожидания
            loaderDiv.remove();

            // создаем элемент div для сообщения
            let messageDiv = document.createElement('div');

            if (data.value) {
                // заполняем поле title
                titleInput.value = data.message;

                messageDiv.classList.add('alert', 'alert-success');
                messageDiv.textContent = data.message;
            } else {
                messageDiv.classList.add('alert', 'alert-danger');
                messageDiv.textContent = data.message;
            }
            // добавляем сообщение в div с id "alert-messages"
            alertMessages.appendChild(messageDiv);

            // удаляем сообщение через 3 секунды
            setTimeout(function () {
                messageDiv.remove();
            }, 3000);
        })
        .catch(err => console.error(err));

    setTimeout(function () {
        loaderDiv.remove();
    }, 5000);
});