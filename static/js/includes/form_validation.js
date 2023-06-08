// проверка поля ФИО на наличие только букв и пробелов
$(document).ready(function () {
    $('#id_ФИО').on('input', function () {
        var regex = /[^a-zA-Zа-яА-Я\s-ё]/g;
        if ($(this).val().match(regex)) {
            $(this).addClass('is-invalid');
        } else {
            $(this).removeClass('is-invalid');
        }
    });
});

// проверяет, что в поле телефона введены только цифры и знак плюса,
// а также что количество символов в номере телефона от 10 до 14
$(document).ready(function () {
    $('#id_Телефон').on('input', function () {
        var regex = /^\+?[0-9]{10,14}$/;
        if (!$(this).val().match(regex)) {
            $(this).addClass('is-invalid');
        } else {
            $(this).removeClass('is-invalid');
        }
    });
});

// проверяет, что в поле почты введен корректный email-адрес,
// содержащий символы до и после знака @, а также доменное имя
$(document).ready(function () {
    $('#id_Почта').on('input', function () {
        var regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!$(this).val().match(regex)) {
            $(this).addClass('is-invalid');
        } else {
            $(this).removeClass('is-invalid');
        }
    });
});