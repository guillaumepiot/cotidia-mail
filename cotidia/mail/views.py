import json
import django_filters

from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render
from django.template.defaultfilters import linebreaksbr
from django.contrib.auth.decorators import login_required, permission_required
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django import forms
from django.contrib import messages

from cotidia.mail import settings as mail_settings
from cotidia.mail.models import EmailLog, EMAIL_LOG_STATUS
from cotidia.mail.forms import NoticeForm
from cotidia.mail.notice import Notice
from cotidia.mail.utils import getNoticeClass, getNoticeMap, getNoticeNames


@login_required
def list(request, template='admin/mail/list.html'):
    return render(request, template, {'notice_map': getNoticeMap()})


@login_required
def log_context(request, log_id, template='admin/mail/log_context.html'):

    log = EmailLog.objects.get(id=log_id)

    return render(request, template, {'log': log})


STATUS_CHOICES = (
    ('', 'Status'),
) + EMAIL_LOG_STATUS

NOTICE_NAME_CHOICES = (
    ('', 'Template'),
) + tuple(getNoticeNames())


class LogFilter(django_filters.FilterSet):

    identifier = django_filters.ChoiceFilter(
        label="Notice type",
        choices=NOTICE_NAME_CHOICES,
        widget=forms.Select(attrs={'class': 'form__select'}),
        help_text="")

    status = django_filters.ChoiceFilter(
        choices=STATUS_CHOICES,
        widget=forms.Select(attrs={'class': 'form__select'}),
        help_text="")

    class Meta:
        model = EmailLog
        fields = ['identifier', 'status']


@login_required
def logs(request, template='admin/mail/logs.html'):

    logs = EmailLog.objects.all()

    log_filter = LogFilter(request.GET, queryset=logs)

    paginator = Paginator(log_filter, 25)  # Show 25 contacts per page

    page = request.GET.get('page')
    try:
        logs = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        logs = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        logs = paginator.page(paginator.num_pages)

    context = {
        'logs': logs,
        'filter': log_filter,
        'logs': logs,
        'is_paginated': True
        }

    return render(request, template, context)


@login_required
@permission_required('mail.add_emaillog')
def new_email(
        request,
        slug,
        template='admin/mail/email_form.html',
        redirect_url='mail-admin:email_preview'):
    """View to create a new notice instance."""

    noticeClass = getNoticeClass(slug)

    if noticeClass is None:
        raise Http404('Notice could not be found')

    notice = noticeClass()

    if request.method == "POST":
        form = NoticeForm(
            data=request.POST,
            json_fields=noticeClass().get_context_editable()
            )
        if form.is_valid():

            clean = form.cleaned_data

            if not clean.get('email'):
                raise Exception('You must have an email field')

            notice = noticeClass(
                recipients=clean['email'].split(','),
                notice=slug,
                context=clean,
            )
            log_id = notice.save()

            return HttpResponseRedirect(reverse(redirect_url, args=(log_id,)))
    else:
        form = NoticeForm(
            initial=noticeClass.default_context,
            json_fields=noticeClass().get_context_editable()
            )

    return render(request, template, {'form': form, 'notice': notice})


@login_required
@permission_required('mail.change_emaillog')
def edit_email(
        request,
        notice_id,
        template='admin/mail/email_form.html',
        redirect_url='mail-admin:email_preview'):
    """Edit view for a notice instance."""

    log = EmailLog.objects.get(id=notice_id)
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
def email_preview(
        request,
        notice_id,
        template='admin/mail/email_preview.html'):
    """View to preview a notice email."""

    log = EmailLog.objects.get(id=notice_id)

    return render(request, template, {'log': log})


@login_required
def email_preview_standalone(
        request,
        notice_id,
        template='admin/mail/email_preview_standalone.html'
        ):
    """View to preview a notice with only the html email, no page wrapping."""

    log = EmailLog.objects.get(id=notice_id)

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
def email_send(request, notice_id, redirect_url='mail-admin:logs'):
    """Send the notice email."""

    log = EmailLog.objects.get(id=notice_id)
    log.send()
    messages.success(request, "Email has been sent")

    return HttpResponseRedirect(reverse(redirect_url))


@login_required
def preview(request, slug, text=False, template='admin/mail/preview.html'):
    """View to preview a notice template."""

    noticeClass = getNoticeClass(slug)

    if noticeClass is None:
        raise Http404('Notice could not be found')

    notice = noticeClass()

    if notice.html_template:
        body_html = notice.get_body_html()
    else:
        body_html = ""

    if notice.text_template:
        body_txt = linebreaksbr(notice.get_body_txt())
    else:
        body_txt = ""

    context = {
        'body_html': body_html,
        'body_txt': body_txt,
        'text': text
    }
    return render(request, template, context)
