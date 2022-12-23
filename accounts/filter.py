from django.db.models import Sum, F, Q, Case, When
from django_filters import rest_framework as filters
from common.functions import decode
from accounts import constants as accounts_constants


class ContactFilter(filters.FilterSet):
    """filter contact"""
    name = filters.CharFilter(method='name_filter')
    list_by = filters.CharFilter(method='list_by_filter')
    order_by = filters.CharFilter(method='order_by_filter')

    def name_filter(self, queryset, name, value):
        """"""
        return queryset.filter(name__icontains=value)

    def list_by_filter(self, queryset, name, value):
        """To order_by the query set"""
        if int(value) == accounts_constants.ContactListBy.INCOME.value:
            queryset = queryset.annotate(
                income=Sum(
                    'contact_transaction__amount',
                    filter=Q(contact_transaction__type=100,
                             contact_transaction__parent_transaction=None), default=0) - Sum(
                    'contact_transaction__child_transactions__amount', default=0,
                    filter=Q(contact_transaction__type=100)),
                expense=Sum(
                    'contact_transaction__amount',
                    filter=Q(contact_transaction__type=200,
                             contact_transaction__parent_transaction=None), default=0) - Sum(
                    'contact_transaction__child_transactions__amount', default=0,
                    filter=Q(contact_transaction__type=200))
            ).exclude(income=0).exclude(income__lt=F('expense'))
        elif int(value) == accounts_constants.ContactListBy.EXPENSE.value:
            queryset = queryset.annotate(
                income=Sum(
                    'contact_transaction__amount',
                    filter=Q(contact_transaction__type=100,
                             contact_transaction__parent_transaction=None), default=0) - Sum(
                    'contact_transaction__child_transactions__amount', default=0,
                    filter=Q(contact_transaction__type=100)),
                expense=Sum(
                    'contact_transaction__amount',
                    filter=Q(contact_transaction__type=200,
                             contact_transaction__parent_transaction=None), default=0) - Sum(
                    'contact_transaction__child_transactions__amount', default=0,
                    filter=Q(contact_transaction__type=200))
            ).exclude(expense=0).exclude(expense__lt=F('income'))
        return queryset

    def order_by_filter(self, queryset, name, value):
        """Order queryset"""
        queryset = queryset.annotate(
            income=Sum(
                'contact_transaction__amount',
                filter=Q(contact_transaction__type=100,
                         contact_transaction__parent_transaction=None), default=0) - Sum(
                'contact_transaction__child_transactions__amount', default=0,
                filter=Q(contact_transaction__type=100)),
            expense=Sum(
                'contact_transaction__amount',
                filter=Q(contact_transaction__type=200,
                         contact_transaction__parent_transaction=None), default=0) - Sum(
                'contact_transaction__child_transactions__amount', default=0,
                filter=Q(contact_transaction__type=200)), total=F('income') - F('expense'),
            amount=Case(When(expense__gt=F('income'), then=F('total') * -1), default=F('total')),
            type=Case(When(expense__gt=F('income'), then=1), default=2)
        )
        if int(value) == accounts_constants.ContactOrderBy.LARGEST_AMOUNT.value:
            queryset = queryset.order_by('-amount')
        elif int(value) == accounts_constants.ContactOrderBy.SMALLEST_AMOUNT.value:
            queryset = queryset.order_by('amount')
        elif int(value) == accounts_constants.ContactOrderBy.LARGEST_INCOME.value:
            queryset = queryset.order_by('-type', '-income', '-expense')
        elif int(value) == accounts_constants.ContactOrderBy.SMALLEST_INCOME.value:
            queryset = queryset.order_by('-type', 'income', 'expense')
        elif int(value) == accounts_constants.ContactOrderBy.LARGEST_EXPENSE.value:
            queryset = queryset.order_by('type', '-expense', '-income')
        elif int(value) == accounts_constants.ContactOrderBy.SMALLEST_EXPENSE.value:
            queryset = queryset.order_by('type', 'expense', 'income')
        elif int(value) == accounts_constants.ContactOrderBy.ALPHABETICAL.value:
            queryset = queryset.order_by('name')
        elif int(value) == accounts_constants.ContactOrderBy.REVERSE_ALPABETICAL.value:
            queryset = queryset.order_by('-name')
        return queryset