from django.conf import settings
from django.core.paginator import Paginator


def get_page_obj(data_set, request, context):
    """Get the page object for the given data_set and page."""
    paginator = Paginator(
        data_set,
        settings.PAGINATION_INTERVAL
    )
    context['page_obj'] = paginator.get_page(request.GET.get('page'))
