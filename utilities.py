from datetime import datetime
from activity_log.models import ActivityLog
from profiles.models import Profiles
import pytz
from django.contrib import messages

__author__ = 'andrew'


def activity_log(request=None, response=None, affected_user=None, security=None, tranzaction=None):
    if not request.get_host() == 'testserver':
        impersonate = None
        af_user = None
        result = 'Page viewed'
        page_title = None

        if hasattr(request, 'user'):
            if request.user.is_authenticated() and hasattr(response, 'context_data'):
                actions = {}
                if request.is_ajax():
                    actions['is_ajax'] = 'True'
                    result = 'Ajax request success'
                else:
                    actions['is_ajax'] = 'False'
                user = u'[{}] {} {}'.format(request.user.id, request.user.first_name, request.user.last_name)
                user_id = request.user.id
                actions['ip_address'] = '{}'.format(request.META['REMOTE_ADDR'])
                if request.POST:
                    post = request.POST.dict()
                    if 'password' in post:
                        post['password'] = '********'
                    if 'new_password' in post:
                        post['new_password'] = '********'
                    if 'pin' in post:
                        post['pin'] = '****'
                    if 'new_pin' in post:
                        post['new_pin'] = '****'
                    actions['POST'] = u'{}'.format(post)
                if request.GET:
                    actions['GET'] = u'{}'.format(request.GET.dict())
                actions['user_agent'] = request.META['HTTP_USER_AGENT']
                actions['current_url'] = request.build_absolute_uri()
                if request.session.get('original_user'):
                    impersonate_user = Profiles.objects.get(id=request.session.get('original_user'))
                    impersonate = u'[{}] {} {}'.format(impersonate_user.id, impersonate_user.first_name,
                                                       impersonate_user.last_name)
                if response:
                    if hasattr(response, 'context_data'):
                        page_title = response.context_data.get('title')

                user_timezone = pytz.timezone(request.user.timezone) if request.user.timezone else pytz.utc
                result_time = datetime.utcnow()
                result_time.replace(tzinfo=pytz.utc).astimezone(user_timezone)

                if messages.get_messages(request):
                    result = u''

                    m_copy = messages.get_messages(request)

                    for msg in m_copy:
                        result += u'{}'.format(msg.message)

                    if request.method == 'POST':
                        m_copy.used = False

                if affected_user:
                    af_user = u'[{}] {} {}'.format(affected_user.id, affected_user.first_name, affected_user.last_name)

                ActivityLog.objects.using('activity_log').create(user=user, user_id=user_id,
                                                                 local_time=result_time, impersonate_by=impersonate,
                                                                 action=actions, result=result, affected_user=af_user,
                                                                 tranzaction=tranzaction, page_title=page_title)
