import inspect, importlib

from django.http import HttpResponse, HttpRequest, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.conf import settings

from cotimail import settings as cotimail_settings
from cotimail import notices

@login_required
def list(request):
	
	template = 'admin/cotimail/list.html'

	for app_module in cotimail_settings.COTIMAIL_APPS:
		# Import module specify in the notification apps setting
		module = importlib.import_module(app_module)

		# Browse through all the classes in that module and pick up the one with an identifier attribute and ends with 'Notice'
		for name, obj in inspect.getmembers(module, inspect.isclass):
			# Get classes that ends with Notice and have an identifier attribute
			if obj.__name__.endswith('Notice') and hasattr(obj, 'identifier') and obj.__name__ != 'Notice':
				NOTICE_MAP.append(obj())

	return render_to_response(template, {},
	context_instance=RequestContext(request))


@login_required
def preview(request, slug, text=False):

	body_html = ""

	for app_module in cotimail_settings.COTIMAIL_APPS:
		# Import module specify in the notification apps setting
		module = importlib.import_module(app_module)

		# Browse through all the classes in that module and pickup the one with an identifier attribute
		for name, obj in inspect.getmembers(module, inspect.isclass):
			# Get classes that ends with Notice and have an identifier attribute
			if obj.__name__.endswith('Notice') and hasattr(obj, 'identifier') and obj.__name__ != 'Notice':
				notice = obj()
				if notice.identifier == slug:
					body_html = notice.get_body_html()
					body_txt = notice.get_body_txt()

					# notice = obj(
					#     sender = 'App <info@app.com>',
					#     recipients = ['Guillaume Piot <guillaume@cotidia.com>'],
					#     context = {}
					# )
					# notice.send()
	
	template = 'admin/cotimail/preview.html'


	return render_to_response(template, {'body_html':body_html, 'body_txt':body_txt, 'text':text },
	context_instance=RequestContext(request))