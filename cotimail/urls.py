from django.conf.urls import patterns, include, url

urlpatterns = patterns('cotimail.views', 

    # url(r'^list/$', 'email_list', name="email_list"),
    url(r'^list/(?P<id>[-\d]+)/$', 'email_preview', name="email_preview"),
    url(r'^sent/(?P<id>[-\d]+)/', 'email_sent', name="email_sent"),
    url(r'^logs/$', 'cotimail_logs', name="logs"),
    url(r'^$', 'notices_list', name="notices_list"),
    url(r'^new/(?P<slug>[-\w]+)/$', 'new_email', name="new_email"),
    url(r'^edit/(?P<id>[-\d]+)/$', 'edit_email', name="edit_email"),
    url(r'^(?P<log_id>[\d]+)/$', 'log_context', name="log_context"),
    # url(r'^(?P<slug>[-\w]+)/$', 'notice_preview', name="cotimail_notice_preview"),
	# url(r'^(?P<slug>[-\w]+)/(?P<text>text)/$', 'preview', name="cotimail_preview_text"),

)