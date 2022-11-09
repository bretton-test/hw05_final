def current_year(request):
    """Добавляет переменную с текущим годом."""
    from datetime import date

    if request:
        now = date.today()
        return {
            'year': now.year
        }
