import json, datetime

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.template import Context
from django.utils.translation import ugettext_lazy as _ 
from django.utils import formats
from cotimail import settings as cotimail_settings

from .utils import inline_css

# Note about custom notice
# All notice classes name must ends with 'Notice', have a unique 'identifer' attribute and a 'name' attribute
# Those identifiers are necessary from the admin management of notices
#
# You will need to subclass the main Notice class to create custom notices
# For example, a custom notice may look like:
#
# class DefaultNotice(Notice):
# 	name = 'Default notice'
# 	identifier = 'default-notice'

__all__ = ('Notice',)

class Notice(object):
	name = 'Notice'
	identifier = 'notice'
	html_template = 'notice/default.html'
	text_template = 'notice/default.txt'
	subject = u'%s' % _('Default subject')
	body_vars = False

	sender = 'App <no-reply@example.com>'
	recipients = ['Firstname Lastname <firstname.lastname@example.com>',]
	reply_to = cotimail_settings.COTIMAIL_REPLY_EMAIL

	context = {}

	# Mandrill meta data
	# Complete send call API doc available here: https://mandrillapp.com/api/docs/messages.html
	track_opens = False # Boolean
	track_clicks = False # Boolean (If you want to track clicks in HTML only, not plaintext mail, you must not set this property, and instead just set the default in your Mandrill account sending options.)
	auto_text = False # whether or not to automatically generate a text part for messages that are not given text
	auto_html = False # whether or not to automatically generate an HTML part for messages that are not given HTML
	inline_css = True # whether or not to automatically inline all CSS styles provided in the message HTML - only for HTML documents less than 256KB in size
	url_strip_qs = False # whether or not to strip the query string from URLs when aggregating tracked URL data
	preserve_recipients = False # Boolean
	global_merge_vars = {} # a dict -- e.g., { 'company': "ACME", 'offer': "10% off" }
	recipient_merge_vars = {} # a dict whose keys are the recipient email addresses and whose values are dicts of merge vars for each recipient -- e.g., { 'wiley@example.com': { 'offer': "15% off anvils" } }
	tags = '' # a list of strings
	google_analytics_domains = [] # a list of string domain names
	google_analytics_campaign = '' # a string or list of strings
	metadata = {} # a dict
	recipient_metadata = {} # a dict whose keys are the recipient email addresses, and whose values are dicts of metadata for each recipient (similar to recipient_merge_vars)


	def __init__(self, **kwargs):
		for k in kwargs.keys():
		   self.__setattr__(k, kwargs[k])

		  
	def send(self):

		msg = EmailMultiAlternatives(
			subject=self.subject,
			body=self.get_body_txt(),
			from_email=self.sender,
			to=self.recipients,
			headers=self.headers # optional extra headers
		)
		msg.attach_alternative(self.get_body_html(), "text/html")

		# Mandrill options
		msg.track_opens = self.track_opens
		msg.track_clicks = self.track_clicks
		msg.auto_text = self.auto_text
		msg.auto_html = self.auto_html
		msg.inline_css = self.inline_css
		msg.url_strip_qs = self.url_strip_qs
		msg.preserve_recipients = self.preserve_recipients
		msg.global_merge_vars = self.global_merge_vars
		msg.recipient_merge_vars = self.recipient_merge_vars
		msg.tags = self.tags
		msg.google_analytics_domains = self.google_analytics_domains
		msg.google_analytics_campaign = self.google_analytics_campaign
		msg.metadata = self.metadata
		msg.recipient_metadata = self.recipient_metadata

		# Send the message
		msg.send()

	def get_body_html(self, context=False):
		if context:
			email_context = self.get_context(context)
		else:
			email_context = self.get_context()
		body_html = render_to_string(self.html_template, self.body_vars, email_context)
		#body_html = inline_css(body_html)
		return body_html

	def get_body_txt(self, context=False):
		if context:
			email_context = self.get_context(context)
		else:
			email_context = self.get_context()
		return render_to_string(self.text_template, self.body_vars, email_context)

	def get_subject(self):
		return self.subject

	def get_context(self, context=False):
		if context:
			return Context(context)
		else:
			return Context(self.context)
	
	@property
	def headers(self):
		_headers = {}
		if self.reply_to:
			_headers['Reply-To'] = self.reply_to
		return _headers

	@property
	def get_identifier(self):
		return u"%s" % self.identifier




