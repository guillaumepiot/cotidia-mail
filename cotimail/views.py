import inspect, importlib, json


from django.http import HttpResponse, HttpRequest, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.template.defaultfilters import linebreaksbr
from django.contrib.auth.decorators import login_required
from django.conf import settings

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from cotimail import settings as cotimail_settings
from cotimail.models import EmailLog
from cotimail.forms import NoticeForm


def _getNoticeClass(slug):
	for app_module in cotimail_settings.COTIMAIL_APPS:
		# Import module specify in the notification apps setting
		module = importlib.import_module(app_module)

		print(module)

		# Browse through all the classes in that module and pickup the one with an identifier attribute
		for name, obj in inspect.getmembers(module, inspect.isclass):
			# Get classes that ends with Notice and have an identifier attribute
			if obj.__name__.endswith('Notice') and hasattr(obj, 'identifier') and obj.__name__ != 'Notice':
				notice = obj()
				if notice.identifier == slug:
					return obj
	raise Exception('Notice could not be found')

@login_required
def list(request):
	
	template = 'admin/cotimail/list.html'

	NOTICE_MAP = []

	for app_module in cotimail_settings.COTIMAIL_APPS:
		# Import module specify in the notification apps setting
		module = importlib.import_module(app_module)

		# Browse through all the classes in that module and pick up the one with an identifier attribute and ends with 'Notice'
		for name, obj in inspect.getmembers(module, inspect.isclass):
			# Get classes that ends with Notice and have an identifier attribute
			if obj.__name__.endswith('Notice') and hasattr(obj, 'identifier') and obj.__name__ != 'Notice':
				NOTICE_MAP.append(obj())

	return render_to_response(template, {'notice_map':NOTICE_MAP},
		context_instance=RequestContext(request))


@login_required
def log_context(request, log_id):
	
	template = 'admin/cotimail/log_context.html'

	log = EmailLog.objects.get(id = log_id)

	return render_to_response(template, {'log':log},
		context_instance=RequestContext(request))

@login_required
def logs(request):

	logs = EmailLog.objects.all()

	template = 'admin/cotimail/logs.html'

	return render_to_response(template, {'logs': logs},
		context_instance=RequestContext(request))



@login_required
def new_email(request, slug):

	noticeClass = _getNoticeClass(slug)
	print(noticeClass.context)
	if request.method == "POST":
		form = NoticeForm(data=request.POST, json_fields=noticeClass.context_editable)
		if form.is_valid():
			
			clean = form.cleaned_data

			if not clean.get('email'):
				raise Exception('You must have an email field')


			# Initiate the notice with necessary variables
			notice = noticeClass(
				sender = '%s <%s>' % ('Guillaume Piot', 'guillaume@cotidia.com'),
				# A list of recipients emails
				recipients = clean['email'].split(','),
				notice = slug,
				context = clean,
			)

			# Send the notice straight away
			log_id = notice.save()
			return HttpResponseRedirect(reverse('cotimail:email_preview', args=(log_id,)))
	else:
		form = NoticeForm(initial=noticeClass.default_context,json_fields=noticeClass.context_editable)

	template = 'admin/cotimail/email_form.html'

	return render_to_response(template, {'form':form},
		context_instance=RequestContext(request))

@login_required
def edit_email(request, id):

	log = EmailLog.objects.get(id = id)
	notice = log.get_object()



	if request.method == "POST":
		form = NoticeForm(data=request.POST, json_fields=notice.context_editable)
		if form.is_valid():
			clean = form.cleaned_data

			log.recipients = json.dumps(clean['email'].split(','))
			log.context_json = json.dumps(clean)

			log.save()

			return HttpResponseRedirect(reverse('cotimail:email_preview', args=(log.id,)))
	else:
		form = NoticeForm(initial=notice.context, json_fields=notice.context_editable)

	template = 'admin/cotimail/email_form.html'

	return render_to_response(template, {'form':form},
		context_instance=RequestContext(request))

#
# Load a page that will load an iframe with the email in preview
#
@login_required
def email_preview(request, id):

	log = EmailLog.objects.get(id = id)

	template = 'admin/cotimail/email_preview.html'

	return render_to_response(template, {'log': log},
		context_instance=RequestContext(request))

#
# View to return a the rendered email only, to be used for the iframe preview
#
@login_required
def email_preview_standalone(request, id):

	log = EmailLog.objects.get(id = id)

	notice = log.get_object()

	context = notice.context

	body_html = notice.get_body_html()
	body_txt = linebreaksbr(notice.get_body_txt())


	template = 'admin/cotimail/email_preview_standalone.html'

	return render_to_response(template, {'log': log, 'body_html' : body_html},
		context_instance=RequestContext(request))


@login_required
def email_sent(request, id):

	log = EmailLog.objects.get(id = id)

	notice = log.get_object()

	log.send()

	return HttpResponseRedirect(reverse('cotimail:logs'))


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
					if notice.html_template:
						body_html = notice.get_body_html()
					body_txt = linebreaksbr(notice.get_body_txt())

	
	template = 'admin/cotimail/preview.html'


	return render_to_response(template, {'body_html':body_html, 'body_txt':body_txt, 'text':text },
		context_instance=RequestContext(request))
