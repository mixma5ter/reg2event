let checkButton = document.getElementById('check-deal');
let dealInput = document.getElementById('id_deal_id');

checkButton.addEventListener('click', function () {
    let dealId = dealInput.value;

    // отправляем AJAX-запрос на сервер для проверки deal_id
    fetch(`/forms/check_deal/${dealId}/`)
        .then(response => response.json())
        .then(data => {
            alert(data.message);
        })
        .catch(err => console.error(err));
});