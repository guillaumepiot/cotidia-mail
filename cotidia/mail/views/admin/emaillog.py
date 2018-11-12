import json
import django_filters

from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render
from django.template.defaultfilters import linebreaksbr
from django.contrib.auth.decorators import login_required, permission_required
from django.urls import reverse
from django.contrib import messages

from cotidia.mail.models import EmailLog, EMAIL_LOG_STATUS
from cotidia.mail.forms import NoticeForm
from cotidia.mail.utils import getNoticeClass, getNoticeNames

from cotidia.admin.views import (
    AdminDetailView,
    AdminListView,
    AdminDeleteView
)


class EmailLogFilter(django_filters.FilterSet):
    identifier = django_filters.ChoiceFilter(
        choices=tuple(getNoticeNames()),
        label="Name"
    )
    status = django_filters.ChoiceFilter(
        choices=EMAIL_LOG_STATUS,
        label="Status"
    )

    class Meta:
        model = EmailLog
        fields = ['identifier', 'status']


class EmailLogList(AdminListView):
    columns = (
        ('Type', 'name'),
        ('Recipients', 'recipients'),
        ('Date sent', 'date_sent'),
        ('Status', 'status'),
    )
    model = EmailLog
    add_view = False
    filterset = EmailLogFilter
    row_actions = ['view']
    row_click_action = 'detail'


class EmailLogDetail(AdminDetailView):
    model = EmailLog
    template_type = 'centered'
    fieldsets = [
        {
            "legend": "Member details",
            "fields": [
                [
                    {
                        "label": "Subject",
                        "field": "subject",
                    },
                    {
                        "label": "Status",
                        "field": "status",
                    }
                ],
                [
                    {
                        "label": "From",
                        "field": "sender",
                    },
                    {
                        "label": "To",
                        "field": "recipients",
                    }
                ],
                [
                    {
                        "label": "Reply-To",
                        "field": "reply_to",
                    },
                    {
                        "label": "CC",
                        "field": "cc",
                    },
                ],
                {
                    "label": "BCC",
                    "field": "bcc",
                },
                [
                    {
                        "label": "Date sent",
                        "field": "date_sent",
                    },
                    {
                        "label": "Created",
                        "field": "date_created",
                    },
                ]
            ]
        },
        {
            "legend": "Email preview",
            "template_name": "admin/mail/emaillog/inline_preview.html"
        }
    ]


class EmailLogDelete(AdminDeleteView):
    model = EmailLog


@login_required
@permission_required('mail.add_emaillog')
def new_email(
        request,
        slug,
        template='admin/mail/emaillog/form.html',
        redirect_url='mail-admin:emaillog-detail'):
    """View to create a new notice instance."""

    notice_class = getNoticeClass(slug)

    if notice_class is None:
        raise Http404('Notice could not be found')

    notice = notice_class()

    if request.method == "POST":
        form = NoticeForm(
            data=request.POST,
            json_fields=notice_class().get_context_editable()
        )
        if form.is_valid():

            clean = form.cleaned_data

            if not clean.get('email'):
                raise Exception('You must have an email field')

            notice = notice_class(
                recipients=clean['email'].split(','),
                notice=slug,
                context=clean,
            )
            log_id = notice.save()

            return HttpResponseRedirect(reverse(redirect_url, args=(log_id,)))
    else:
        form = NoticeForm(
            initial=notice_class.default_context,
            json_fields=notice_class().get_context_editable()
        )

    return render(request, template, {'form': form, 'notice': notice})


@login_required
@permission_required('mail.change_emaillog')
def edit_email(
        request,
        pk,
        template='admin/mail/emaillog/form.html',
        redirect_url='mail-admin:emaillog-detail'):
    """Edit view for a notice instance."""

    log = EmailLog.objects.get(id=pk)
    notice = log.get_object()

    if request.method == "POST":
        form = NoticeForm(
            data=request.POST,
            json_fields=notice.get_context_editable()
        )
        if form.is_valid():
            clean = form.cleaned_data

            log.recipients = json.dumps(clean['email'].split(','))
            log.context_json = json.dumps(clean)

            log.save()

            return HttpResponseRedirect(reverse(redirect_url, args=(log.id,)))
    else:
        form = NoticeForm(
            initial=notice.context,
            json_fields=notice.get_context_editable()
        )

    return render(request, template, {'form': form, 'log': log})


@login_required
@permission_required('mail.change_emaillog')
def email_preview_standalone(
        request,
        pk,
        template='admin/mail/emaillog/preview_standalone.html'):
    """View to preview a notice with only the html email, no page wrapping."""

    log = EmailLog.objects.get(id=pk)

    notice = log.get_object()

    if notice.html_template:
        body_html = notice.get_body_html()
    else:
        body_html = ""

    if notice.text_template:
        body_txt = linebreaksbr(notice.get_body_txt())
    else:
        body_txt = ""

    context = {
        "log": log,
        "body_html": body_html,
        "body_txt": body_txt
    }

    return render(request, template, context)


@login_required
@permission_required('mail.change_emaillog')
def email_send(request, pk, redirect_url='mail-admin:logs'):
    """Send the notice email."""

    log = EmailLog.objects.get(id=pk)
    log.send()
    messages.success(request, "Email has been sent")

    return HttpResponseRedirect(reverse(redirect_url))
