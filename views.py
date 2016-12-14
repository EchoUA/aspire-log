from activity_log.models import ActivityLog
from django.db.models import Q
from django.views.generic import ListView
from django.views.generic.base import TemplateView
from mixins.mixin import GroupRequiredMixin

class ReportsView(GroupRequiredMixin, TemplateView):
    template_name = 'reports/reports.html'
    access_groups_list = [2]

    def get_context_data(self, **kwargs):
        context = super(ReportsView, self).get_context_data(**kwargs)
        context['p_name'] = 'reports'
        context['title'] = 'Reports'
        return context


class ActivityLogView(GroupRequiredMixin, ListView):
    model = ActivityLog
    template_name = 'activity_log/list.html'
    access_groups_list = [2]
    paginate_by = 10

    def get_queryset(self):
        result = ActivityLog.objects.using('activity_log').all()
        if self.request.GET.get('event'):
            event = ' '.join(self.request.GET.get('event').split())
            result = result.filter(Q(result__icontains=event))
        if self.request.GET.get('user'):
            user = ' '.join(self.request.GET.get('user').split())
            result = result.filter(Q(user__icontains=user))
        if self.request.GET.get('affected_user'):
            affected_user = ' '.join(self.request.GET.get('affected_user').split())
            result = result.filter(Q(affected_user__icontains=affected_user))
        if self.request.GET.get('descr'):
            descr = ' '.join(self.request.GET.get('descr').split())
            result = result.filter(Q(action__values__contains=[descr]))
        if self.request.GET.get('start_date'):
            result = result.filter(server_time__gte=self.request.GET.get('start_date'))
        if self.request.GET.get('end_date'):
            result = result.filter(server_time__lt=self.request.GET.get('end_date'))

        return result.order_by('-id')

    def get_paginate_by(self, queryset):
        return self.request.COOKIES.get('theme', self.paginate_by)

    def get_context_data(self, **kwargs):
        context = super(ActivityLogView, self).get_context_data(**kwargs)
        context['p_name'] = 'activity_log'
        context['title'] = 'Activity log'
        return context
