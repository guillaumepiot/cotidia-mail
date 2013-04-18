from django.conf.urls import patterns, include, url

urlpatterns = patterns('cotimail.views', 

    url(r'^$', 'list', name="cotimail_list"),
    url(r'^(?P<slug>[-\w]+)/$', 'preview', name="cotimail_preview"),
    url(r'^(?P<slug>[-\w]+)/(?P<text>text)/$', 'preview', name="cotimail_preview_text"),
	    
)