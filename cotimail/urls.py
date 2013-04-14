from django.conf.urls.defaults import * 

urlpatterns = patterns('cotimail.views', 

    url(r'^$', 'list', name="cotimail_list"),
    url(r'^(?P<slug>[-\w]+)/$', 'preview', name="cotimail_preview"),
    url(r'^(?P<slug>[-\w]+)/(?P<text>text)/$', 'preview', name="cotimail_preview_text"),
	    
)