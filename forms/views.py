from django.shortcuts import render, redirect


def index(request):
    """Главная страница."""

    if request.user.is_authenticated:
        title = 'Регистрация обращений'
        template_name = 'forms/index.html'
        context = {
            'user': request.user,
            'title': title,
        }
        return render(request, template_name, context)

    return redirect('login')
