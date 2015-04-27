import json, pickle, base64

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.template import Context
from django.utils.translation import ugettext_lazy as _
from django.utils import formats
from django.forms.models import model_to_dict
from django.utils.timezone import now

from cotimail import settings as cotimail_settings

from .utils import inline_css
from .models import EmailLog

# Note about custom notice
# All notice classes name must ends with 'Notice', have a unique 'identifer' attribute and a 'name' attribute
# Those identifiers are necessary from the admin management of notices
#
# You will need to subclass the main Notice class to create custom notices
# For example, a custom notice may look like:
#
# class DefaultNotice(Notice):
#   name = 'Default notice'
#   identifier = 'default-notice'

__all__ = ('Notice',)

class Notice(object):
    name = 'Notice'
    identifier = 'notice'
    html_template = 'notice/default.html'
    text_template = 'notice/default.txt'
    subject = u'%s' % _('Default subject')
    body_vars = False

    sender = cotimail_settings.COTIMAIL_SENDER
    recipients = ['Firstname Lastname <firstname.lastname@example.com>',]
    reply_to = cotimail_settings.COTIMAIL_REPLY_EMAIL

    default_context = {}
    context = {}
    context_editable = []

    """

    Example editable context:

    context_editable = [
          {
            "fieldset":"Customer",
            "fields":[
                {
                    "name":"email",
                    "type":"charfield",
                    "required":True
                }
            ]
          }
        ]
    """

    first_name = ''
    last_name = ''

    notice = ''
    
    #Hook the notice to an object
    content_object = False

    # Mandrill meta data
    # Complete send call API doc available here: https://mandrillapp.com/api/docs/messages.html
    track_opens = False # Boolean
    track_clicks = False # Boolean (If you want to track clicks in HTML only, not plaintext mail, you must not set this property, and instead just set the default in your Mandrill account sending options.)
    auto_text = False # whether or not to automatically generate a text part for messages that are not given text
    auto_html = False # whether or not to automatically generate an HTML part for messages that are not given HTML
    inline_css = True if cotimail_settings.COTIMAIL_INLINE_CSS_MANDRILL else False # whether or not to automatically inline all CSS styles provided in the message HTML - only for HTML documents less than 256KB in size
    url_strip_qs = False # whether or not to strip the query string from URLs when aggregating tracked URL data
    preserve_recipients = False # Boolean
    global_merge_vars = {} # a dict -- e.g., { 'company': "ACME", 'offer': "10% off" }
    recipient_merge_vars = {} # a dict whose keys are the recipient email addresses and whose values are dicts of merge vars for each recipient -- e.g., { 'wiley@example.com': { 'offer': "15% off anvils" } }
    tags = '' # a list of strings
    google_analytics_domains = [] # a list of string domain names
    google_analytics_campaign = '' # a string or list of strings
    metadata = {} # a dict
    recipient_metadata = {} # a dict whose keys are the recipient email addresses, and whose values are dicts of metadata for each recipient (similar to recipient_merge_vars)
    # Attachments
    # A list of dictionary containing the raw file data
    attachments = [] #[{"content_type": "application/pdf","name": "myfile.txt","file_path": "/file/doc.pdf"}]

    def __init__(self, **kwargs):
        for k in kwargs.keys():
           self.__setattr__(k, kwargs[k])

    @property
    def headers(self):
        _headers = {}
        if self.reply_to:
            _headers['Reply-To'] = self.reply_to
        return _headers

    @property
    def get_identifier(self):
        return u"%s" % self.identifier

# get context dict
    def get_context_dict(self, context=False):
        if context:
            the_context = self.default_context
            the_context.update(context)
            return the_context
        else:
            the_context = self.default_context
            the_context.update(self.context)
            return the_context

# get context json
    def get_context_json(self):
        print self.get_context_dict()
        return json.dumps(self.get_context_dict())

    def get_context(self, context=False):
        if context:
            return Context(self.get_context_dict(context))
        else:
            return Context(self.get_context_dict())

    def get_body_html(self, context=False):
        if context:
            email_context = self.get_context(context)
        else:
            email_context = self.get_context()
        
        body_html = render_to_string(self.html_template, self.body_vars, email_context)
        if cotimail_settings.COTIMAIL_INLINE_CSS_LOCAL:
            body_html = inline_css(body_html)
        return body_html

    def get_body_txt(self, context=False):
        if context:
            email_context = self.get_context(context)
        else:
            email_context = self.get_context()
        return render_to_string(self.text_template, self.body_vars, email_context)

    def get_subject(self):
        return self.subject

    def send(self, force_now=False, log_id = None):

        if force_now or not cotimail_settings.COTIMAIL_QUEUE_MAIL:
            self._process_and_send()
            if cotimail_settings.COTIMAIL_LOG_MAIL:
                self.log(status='SENT', log_id = log_id)
        else:
            self.log(status='QUEUED', log_id = log_id)

    def queue(self, log_id = None):
        self.log(status='QUEUED', log_id = log_id)

    def save(self, log_id = None):
        log = self.log(status='SAVED', log_id = log_id)
        return log.id

    def log(self, status, log_id = None):
        pickled_notice = base64.b64encode(pickle.dumps(self))
        if log_id:
            email_log = EmailLog.object.get(id=log_id)
        else:
            email_log = EmailLog()

        email_log.subject = self.get_subject()
        email_log.pickled_data = pickled_notice
        email_log.name = self.name
        email_log.identifier = self.identifier
        email_log.recipients = json.dumps(self.recipients)
        email_log.sender = self.sender
        email_log.reply_to = self.reply_to
        email_log.status = status
        email_log.context_json = self.get_context_json()
        email_log.notice = self.notice
        if status == 'SENT':
            email_log.date_sent = now()
        if self.content_object:
            email_log.content_object = self.content_object
        email_log.save()

        return email_log


    def _process_and_send(self):

        msg = EmailMultiAlternatives(
            subject=self.get_subject(),
            body=self.get_body_txt(),
            from_email=self.sender,
            to=self.recipients,
            headers=self.headers # optional extra headers
        )
        if self.html_template:
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

        if self.attachments:
            for attachment in self.attachments:
                if attachment.has_key('file') and attachment.has_key('filename'):
                    msg.attach(attachment['filename'], attachment['file'], attachment['content_type'])
                else:
                    msg.attach_file(attachment['file_path'], attachment['content_type'])

        # Send the message
        response = msg.send()

        return response






