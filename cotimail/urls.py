from django.conf.urls import patterns, include, url

urlpatterns = patterns('cotimail.views', 

    #
    # List all available notices
    #
    url(r'^$', 'list', name="list"),
    
    #
    # Create, edit and preview notices
    #
    url(r'^new/(?P<slug>[-\w]+)/$', 'new_email', name="new_email"),
    url(r'^edit/(?P<id>[-\d]+)/$', 'edit_email', name="edit_email"),
    url(r'^preview/(?P<id>[-\d]+)/$', 'email_preview', name="email_preview"),
    url(r'^preview/standalone/(?P<id>[-\d]+)/$', 'email_preview_standalone', name="email_preview_standalone"),
    url(r'^sent/(?P<id>[-\d]+)/', 'email_sent', name="email_sent"),
    url(r'^(?P<log_id>[\d]+)/$', 'log_context', name="log_context"),
    url(r'^logs/$', 'logs', name="logs"),

    #
    # Notice Template Preview in HTML and TEXT versions
    #
    url(r'^(?P<slug>[-\w]+)/$', 'preview', name="template_preview_html"),
    url(r'^(?P<slug>[-\w]+)/(?P<text>text)/$', 'preview', name="template_preview_text"),
)