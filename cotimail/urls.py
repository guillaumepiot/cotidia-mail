from django.conf.urls import patterns, include, url

urlpatterns = patterns('cotimail.views', 

    # url(r'^list/$', 'email_list', name="email_list"),
    url(r'^list/(?P<id>[-\d]+)/$', 'email_preview', name="email_preview"),
    url(r'^sent/(?P<id>[-\d]+)/', 'email_sent', name="email_sent"),
    url(r'^$', 'notices_list', name="notices_list"),
    url(r'^logs/$', 'cotimail_logs', name="cotimail_logs"),
    url(r'^(?P<log_id>[\d]+)/$', 'log_context', name="cotimail_log_context"),
    url(r'^new/(?P<slug>[-\w]+)/$', 'new_email', name="new_email"),
    url(r'^edit/(?P<id>[-\d]+)/$', 'edit_email', name="edit_email"),

)