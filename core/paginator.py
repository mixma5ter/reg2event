from django.core.paginator import Paginator

POSTS_ON_PAGE = 10


def paginator(request, items):
    paginator = Paginator(items, POSTS_ON_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Определяем номера страниц для отображения в пагинаторе
    if page_obj.number <= 2:
        page_numbers = range(1, min(paginator.num_pages + 1, 6))
    elif page_obj.number >= paginator.num_pages - 1:
        page_numbers = range(max(1, paginator.num_pages - 5), paginator.num_pages + 1)
    else:
        page_numbers = range(page_obj.number - 2, page_obj.number + 3)

    return page_obj, page_numbers
