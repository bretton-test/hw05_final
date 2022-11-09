from django.urls import reverse

TEMPLATE_LIST = [
    ('users/password_change_form.html', 'password_change page test'),
    ('users/password_change_done.html', 'password_change_done page test'),
    ('users/login.html', 'login page test'),
    ('users/signup.html', 'signup page test'),
    ('users/password_reset_form.html', 'password_reset page test'),
    ('users/password_reset_done.html', 'password_reset_done page test'),
    (
        'users/password_reset_complete.html',
        'password_reset_complete page test',
    ),
    ('users/password_reset_confirm.html', 'password_reset_confirm page test'),
    ('users/logged_out.html', 'logout page test'),
]

URL_LIST = [
    '/auth/password_change/',
    '/auth/password_change/done/',
    '/auth/login/',
    '/auth/signup/',
    '/auth/password_reset/',
    '/auth/password_reset/done/',
    '/auth/reset/done/',
    '/auth/reset/x/x/',
    '/auth/logout/',
]

VIEW_LIST = [
    reverse('users:password_change'),
    reverse('users:password_change_done'),
    reverse('users:login'),
    reverse('users:signup'),
    reverse('users:password_reset'),
    reverse('users:password_reset_done'),
    reverse('users:password_reset_complete'),
    reverse(
        'users:password_reset_confirm', kwargs={'uidb64': 'x', 'token': 'x'}
    ),
    reverse('users:logout'),
]


def get_url_list():
    return dict(zip(URL_LIST, TEMPLATE_LIST))


def get_view_list():
    return dict(zip(VIEW_LIST, TEMPLATE_LIST))
