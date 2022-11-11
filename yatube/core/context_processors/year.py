from django.utils import timezone


def current_year(request):
    """Добавляет переменную с текущим годом."""

    if request:
        now = timezone.now()
        return {'year': now.year}
