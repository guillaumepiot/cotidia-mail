from django.conf.urls import patterns, include, url
from cotimail import views

urlpatterns = [ 
    #
    # List all available notices
    #
    url(r'^$', views.list, name="list"),
    
    #
    # Create, edit and preview notices
    #
    url(r'^new/(?P<slug>[-\w]+)/$', views.new_email, name="new_email"),
    url(r'^edit/(?P<id>[-\d]+)/$', views.edit_email, name="edit_email"),
    url(r'^preview/(?P<id>[-\d]+)/$', views.email_preview, name="email_preview"),
    url(r'^preview/standalone/(?P<id>[-\d]+)/$', views.email_preview_standalone, name="email_preview_standalone"),
    url(r'^sent/(?P<id>[-\d]+)/', views.email_sent, name="email_sent"),
    url(r'^(?P<log_id>[\d]+)/$', views.log_context, name="log_context"),
    url(r'^logs/$', views.logs, name="logs"),

    #
    # Notice Template Preview in HTML and TEXT versions
    #
    url(r'^(?P<slug>[-\w]+)/$', views.preview, name="template_preview_html"),
    url(r'^(?P<slug>[-\w]+)/(?P<text>text)/$', views.preview, name="template_preview_text"),
]