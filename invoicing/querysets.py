import datetime

from django.db import connection
from django.db.models import Q
from django.db.models.query import QuerySet
from django.utils.timezone import now


class InvoiceQuerySet(QuerySet):
    def overdue(self):
        return self.filter(date_due__lt=datetime.datetime.combine(now().date(), datetime.time.max)).exclude(status__in=[self.model.STATUS.PAID, self.model.STATUS.CANCELED])

    def not_overdue(self):
        return self.filter(Q(date_due__gt=datetime.datetime.combine(now().date(), datetime.time.max)) | Q(status__in=[self.model.STATUS.PAID, self.model.STATUS.CANCELED]))

    def paid(self):
        return self.filter(status=self.model.STATUS.PAID)

    def unpaid(self):
        return self.exclude(status__in=[self.model.STATUS.PAID, self.model.STATUS.CANCELED])

    def valid(self):
        return self.exclude(status__in=[self.model.STATUS.RETURNED, self.model.STATUS.CANCELED])

    def lock(self):
        """ Lock table.

        Locks the object model table so that atomic update is possible.
        Simultaneous database access request pend until the lock is unlock()'ed.

        Note: If you need to lock multiple tables, you need to do lock them
        all in one SQL clause and this function is not enough. To avoid
        dead lock, all tables must be locked in the same order.

        If no lock mode is specified, then ACCESS EXCLUSIVE, the most restrictive mode, is used.
        Read more: https://www.postgresql.org/docs/9.4/static/sql-lock.html
        """
        cursor = connection.cursor()
        table = self.model._meta.db_table
        cursor.execute("LOCK TABLE %s" % table)


class ItemQuerySet(QuerySet):
    def with_tag(self, tag):
        return self.filter(tag=tag)
