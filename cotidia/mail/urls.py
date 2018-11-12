from django.urls import path
from cotidia.mail.views.admin import notice, emaillog

app_name = 'cotidia.mail'

urlpatterns = [
    path(
        '',
        notice.list,
        name="list"
    ),
    path(
        '<slug>',
        notice.preview,
        name="template_preview_html"
    ),
    path(
        '<slug>/text',
        notice.preview,
        {
            'text': 'text'
        },
        name="template_preview_text",
    ),

    path(
        'new/<slug>',
        emaillog.new_email,
        name="new_email"),
    path(
        'logs/',
        emaillog.EmailLogList.as_view(),
        name="emaillog-list"),
    path(
        'edit/<int:pk>',
        emaillog.edit_email,
        name="emaillog-update"),
    path(
        'delete/<int:pk>',
        emaillog.EmailLogDelete.as_view(),
        name="emaillog-delete"),
    path(
        'preview/<int:pk>',
        emaillog.EmailLogDetail.as_view(),
        name="emaillog-detail"),
    path(
        'preview/standalone/<int:pk>',
        emaillog.email_preview_standalone,
        name="email_preview_standalone"),
    path(
        'send/<int:pk>',
        emaillog.email_send,
        name="email_sent"),
    path(
        'logs/',
        emaillog.EmailLogList.as_view(),
        name="logs"),
]
