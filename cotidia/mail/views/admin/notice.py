from django.http import Http404
from django.shortcuts import render
from django.template.defaultfilters import linebreaksbr
from django.contrib.auth.decorators import login_required, permission_required

from cotidia.mail.utils import getNoticeClass, getNoticeMap


@login_required
@permission_required('mail.change_emaillog')
def list(request, template='admin/mail/notice/list.html'):
    return render(request, template, {'notice_map': getNoticeMap()})


@login_required
@permission_required('mail.change_emaillog')
def preview(request, slug, text=False, template='admin/mail/notice/preview.html'):
    """View to preview a notice template."""

    notice_class = getNoticeClass(slug)

    if notice_class is None:
        raise Http404('Notice could not be found')

    notice = notice_class()

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
