// Получаем ссылку на форму
const form = document.querySelector('.form-container');

// Добавляем обработчик события на отправку формы
form.addEventListener('submit', function () {
    // Получаем ссылку на кнопку, на которую было нажато
    const button = document.activeElement;

    // Создаем и добавляем крутящийся индикатор ожидания
    const loader = document.createElement('div');
    loader.classList.add('loader');
    button.appendChild(loader);
});