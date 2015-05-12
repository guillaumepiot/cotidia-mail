import inspect, importlib, json
import django_filters

from django.http import HttpResponse, HttpRequest, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.template.defaultfilters import linebreaksbr
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from cotimail import settings as cotimail_settings
from cotimail.models import EmailLog, EMAIL_LOG_STATUS
from cotimail.forms import NoticeForm


def _getNoticeClass(slug):
    for app_module in cotimail_settings.COTIMAIL_APPS:
        # Import module specify in the notification apps setting
        module = importlib.import_module(app_module)

        print(module)

        # Browse through all the classes in that module and pickup the one with an identifier attribute
        for name, obj in inspect.getmembers(module, inspect.isclass):
            # Get classes that ends with Notice and have an identifier attribute
            if obj.__name__.endswith('Notice') and hasattr(obj, 'identifier') and obj.__name__ != 'Notice':
                notice = obj()
                if notice.identifier == slug:
                    return obj
    raise Exception('Notice could not be found')

def _getNoticeNames():
    NOTICE_NAMES = []

    for app_module in cotimail_settings.COTIMAIL_APPS:
        # Import module specify in the notification apps setting
        module = importlib.import_module(app_module)

        # Browse through all the classes in that module and pick up the one with an identifier attribute and ends with 'Notice'
        for name, obj in inspect.getmembers(module, inspect.isclass):
            # Get classes that ends with Notice and have an identifier attribute
            if obj.__name__.endswith('Notice') and hasattr(obj, 'identifier') and obj.__name__ != 'Notice':
                NOTICE_NAMES.append((obj.identifier, obj.name))

    return NOTICE_NAMES

@login_required
def list(request):
    
    template = 'admin/cotimail/list.html'

    NOTICE_MAP = []

    for app_module in cotimail_settings.COTIMAIL_APPS:
        # Import module specify in the notification apps setting
        module = importlib.import_module(app_module)

        # Browse through all the classes in that module and pick up the one with an identifier attribute and ends with 'Notice'
        for name, obj in inspect.getmembers(module, inspect.isclass):
            # Get classes that ends with Notice and have an identifier attribute
            if obj.__name__.endswith('Notice') and hasattr(obj, 'identifier') and obj.__name__ != 'Notice':
                NOTICE_MAP.append(obj())

    NOTICE_MAP = sorted(NOTICE_MAP, key=lambda obj: obj.name)

    return render_to_response(template, {'notice_map':NOTICE_MAP},
        context_instance=RequestContext(request))


@login_required
def log_context(request, log_id):
    
    template = 'admin/cotimail/log_context.html'

    log = EmailLog.objects.get(id = log_id)

    return render_to_response(template, {'log':log},
        context_instance=RequestContext(request))


#
# Create a list of logs with pagination and filters
#

STATUS_CHOICES = (
    ('', 'All'),
) + EMAIL_LOG_STATUS

NOTICE_NAME_CHOICES = (
    ('', 'All'),
) + tuple(_getNoticeNames())

class LogFilter(django_filters.FilterSet):
    status = django_filters.ChoiceFilter(choices=STATUS_CHOICES)#, widget=django_filters.widgets.LinkWidget
    identifier = django_filters.ChoiceFilter(choices=NOTICE_NAME_CHOICES)
    
    class Meta:
        model = EmailLog
        fields = ['identifier', 'status']

@login_required
def logs(request):

    logs = EmailLog.objects.all()

    log_filter = LogFilter(request.GET, queryset=logs)

    paginator = Paginator(log_filter, 25) # Show 25 contacts per page

    page = request.GET.get('page')
    try:
        logs = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        logs = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        logs = paginator.page(paginator.num_pages)

    template = 'admin/cotimail/logs.html'

    return render_to_response(template, {'logs': logs, 'filter': log_filter, 'logs': logs},
        context_instance=RequestContext(request))



@login_required
def new_email(request, slug):

    noticeClass = _getNoticeClass(slug)

    if request.method == "POST":
        form = NoticeForm(data=request.POST, json_fields=noticeClass.context_editable)
        if form.is_valid():
            
            clean = form.cleaned_data

            if not clean.get('email'):
                raise Exception('You must have an email field')


            # Initiate the notice with necessary variables
            notice = noticeClass(
                sender = '%s <%s>' % ('Guillaume Piot', 'guillaume@cotidia.com'),
                # A list of recipients emails
                recipients = clean['email'].split(','),
                notice = slug,
                context = clean,
            )

            # Send the notice straight away
            log_id = notice.save()
            return HttpResponseRedirect(reverse('cotimail:email_preview', args=(log_id,)))
    else:
        form = NoticeForm(json_fields=noticeClass.context_editable)

    template = 'admin/cotimail/email_form.html'

    return render_to_response(template, {'form':form},
        context_instance=RequestContext(request))

@login_required
def edit_email(request, id):

    log = EmailLog.objects.get(id = id)
    notice = log.get_object()



    if request.method == "POST":
        form = NoticeForm(data=request.POST, json_fields=notice.context_editable)
        if form.is_valid():
            clean = form.cleaned_data

            log.recipients = json.dumps(clean['email'].split(','))
            log.context_json = json.dumps(clean)

            log.save()

            return HttpResponseRedirect(reverse('cotimail:email_preview', args=(log.id,)))
    else:
        form = NoticeForm(initial=notice.context, json_fields=notice.context_editable)

    template = 'admin/cotimail/email_form.html'

    return render_to_response(template, {'form':form},
        context_instance=RequestContext(request))

#
# Load a page that will load an iframe with the email in preview
#
@login_required
def email_preview(request, id):

    log = EmailLog.objects.get(id = id)

    template = 'admin/cotimail/email_preview.html'

    return render_to_response(template, {'log': log},
        context_instance=RequestContext(request))

#
# View to return a the rendered email only, to be used for the iframe preview
#
@login_required
def email_preview_standalone(request, id):

    log = EmailLog.objects.get(id = id)

    notice = log.get_object()

    context = notice.context

    body_html = notice.get_body_html()
    body_txt = linebreaksbr(notice.get_body_txt())


    template = 'admin/cotimail/email_preview_standalone.html'

    return render_to_response(template, {'log': log, 'body_html' : body_html},
        context_instance=RequestContext(request))


@login_required
def email_sent(request, id):

    log = EmailLog.objects.get(id = id)

    notice = log.get_object()

    log.send()

    return HttpResponseRedirect(reverse('cotimail:logs'))


@login_required
def preview(request, slug, text=False):

    body_html = ""

    for app_module in cotimail_settings.COTIMAIL_APPS:
        # Import module specify in the notification apps setting
        module = importlib.import_module(app_module)

        # Browse through all the classes in that module and pickup the one with an identifier attribute
        for name, obj in inspect.getmembers(module, inspect.isclass):
            # Get classes that ends with Notice and have an identifier attribute
            if obj.__name__.endswith('Notice') and hasattr(obj, 'identifier') and obj.__name__ != 'Notice':
                notice = obj()
                if notice.identifier == slug:
                    if notice.html_template:
                        body_html = notice.get_body_html()
                    body_txt = linebreaksbr(notice.get_body_txt())

    
    template = 'admin/cotimail/preview.html'


    return render_to_response(template, {'body_html':body_html, 'body_txt':body_txt, 'text':text },
        context_instance=RequestContext(request))
