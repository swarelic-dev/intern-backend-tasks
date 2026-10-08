from rest_framework.pagination import PageNumberPagination


class ContactPagination(PageNumberPagination):
    """
    Standard pagination class configured for 5 items per page.
    """
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 50
