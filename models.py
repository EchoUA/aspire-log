from django.contrib.postgres.fields import HStoreField
from django.db import models
from django.utils.translation import ugettext_lazy as _


class ActivityLog(models.Model):
    user = models.CharField(max_length=100, verbose_name=_('User'), null=True, db_index=True)
    user_id = models.IntegerField(verbose_name=_('User ID'), null=True)
    impersonate_by = models.CharField(max_length=100, verbose_name=_('Impersonate by'), null=True, db_index=True)
    page_title = models.CharField(max_length=100, verbose_name=_('Page title'), null=True)
    result = models.CharField(max_length=1000, verbose_name=_('Event'), db_index=True)
    affected_user = models.CharField(max_length=500, verbose_name=_('Affected user'), null=True, db_index=True)
    tranzaction = models.IntegerField(verbose_name=_('Tranzaction ID'), null=True)
    server_time = models.DateTimeField(auto_now_add=True, null=True)
    local_time = models.DateTimeField(null=True, verbose_name=_('Local time'))
    action = HStoreField(verbose_name=_('User action'))

    class Meta:
        db_table = 'ActivityLog'
        verbose_name = 'Activity Log'
        verbose_name_plural = 'Activity logs'

