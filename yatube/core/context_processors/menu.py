def header_menu(request):
    """Добавляет словарь меню в header"""

    auth_menu = {
        'Об авторе': 'about:author',
        'Технологии': 'about:tech',
        'Новая запись': 'posts:post_create',
        'Изменить пароль': 'users:password_change',
        'Выйти': 'users:logout'

    }
    menu = {
        'Об авторе': 'about:author',
        'Технологии': 'about:tech',
        'Войти': 'users:login',
        'Регистрация': 'users:signup'
    }

    if request:
        if request.user.is_authenticated:
            return {'menu': auth_menu}

        return {'menu': menu}
