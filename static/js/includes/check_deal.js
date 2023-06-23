let checkButton = document.getElementById('check-deal');
let dealInput = document.getElementById('id_deal_id');
let titleInput = document.getElementById('id_title');

checkButton.addEventListener('click', function () {
    let dealId = dealInput.value;

    // отправляем AJAX-запрос на сервер для проверки deal_id
    fetch(`/forms/check_deal/${dealId}/`)
        .then(response => response.json())
        .then(data => {
            if (data.value) {
                titleInput.value = data.message;
            } else {
                alert(data.message);
            }
        })
        .catch(err => console.error(err));
});