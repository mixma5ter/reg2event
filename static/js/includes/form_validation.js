// проверяет, что в поле телефона введены только цифры и знак плюса,
// а также что количество символов в номере телефона от 10 до 14
document.addEventListener('DOMContentLoaded', function () {
    const phoneNumberInput = document.getElementById('id_Телефон');
    if (phoneNumberInput) {
        phoneNumberInput.addEventListener('input', function () {
            const regex = /^\+?[0-9]{10,14}$/;
            if (!this.value.match(regex)) {
                this.classList.add('is-invalid');
            } else {
                this.classList.remove('is-invalid');
            }
        });
    }

    // проверяет, что в поле почты введен корректный email-адрес,
    // содержащий символы до и после знака @, а также доменное имя
    const emailInput = document.getElementById('id_Почта');
    if (emailInput) {
        emailInput.addEventListener('input', function () {
            const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!this.value.match(regex)) {
                this.classList.add('is-invalid');
            } else {
                this.classList.remove('is-invalid');
            }
        });
    }
});