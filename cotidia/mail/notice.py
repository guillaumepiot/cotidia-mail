import json
import pickle
import base64
import os.path

from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.utils.timezone import now

from anymail.exceptions import AnymailRecipientsRefused

from cotidia.mail import settings as cotimail_settings
from cotidia.mail.models import EmailLog

# Note about custom notice
# All notice classes name must ends with 'Notice', have a unique 'identifer'
# attribute and a 'name' attribute
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
    subject = 'Default subject'
    body_vars = False

    sender = cotimail_settings.COTIMAIL_SENDER
    recipients = ['Firstname Lastname <firstname.lastname@example.com>']
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

    content_object = False

    #
    # Attachments
    #
    # A list of dictionary containing the raw file data
    # Eg:
    # [
    #     {
    #         "content_type": "application/pdf",
    #         "name": "myfile.txt",
    #         "file_path": "/file/doc.pdf"
    #     }
    # ]
    attachments = []

    def __init__(self, **kwargs):
        for k in kwargs.keys():
            self.__setattr__(k, kwargs[k])

    @property
    def headers(self):
        _headers = {}
        return _headers

    @property
    def get_identifier(self):
        return u"%s" % self.identifier

    # get context dict
    def get_context_dict(self, context=False):
        if context:
            the_context = self.context
            the_context.update(context)
            return the_context
        else:
            the_context = self.default_context.copy()
            the_context.update(self.context)
            return the_context

    # get context json
    def get_context_json(self):
        return json.dumps(self.get_context_dict())

    def get_context(self, context=False):
        if context:
            return self.get_context_dict(context)
        else:
            return self.get_context_dict()

    def get_context_editable(self):
        if hasattr(self, 'context_editable'):
            return self.context_editable
        else:
            return {}

    def render_to_html(self, template, context):
        template = get_template(template)
        return template.render(context)

    #
    # Render the email to the HTML version
    #
    def get_body_html(self, context=False):
        return self.render_to_html(
            self.html_template,
            self.get_context(context)
        )

    #
    # Render the email to the TXT version
    #
    def get_body_txt(self, context=False):
        return self.render_to_html(
            self.text_template,
            self.get_context(context)
        )

    #
    # Render the email to the PDF version
    #
    def get_body_pdf(self, context=False):
        return self.render_to_html(
            self.pdf_template,
            self.get_context(context)
        )

    def get_subject(self):
        # Test if the subject is a path to a template
        try:
            template = get_template(self.subject)
            subject = template.render({}).strip()
            return subject
        except:
            return self.subject

    def send(self, force_now=False, log_id=None):

        if force_now or not cotimail_settings.COTIMAIL_QUEUE_MAIL:
            self._process_and_send()
            if cotimail_settings.COTIMAIL_LOG_MAIL:
                self.log(status='SENT', log_id=log_id)
        else:
            self.log(status='QUEUED', log_id=log_id)

    def queue(self, log_id=None):
        self.log(status='QUEUED', log_id=log_id)

    def save(self, log_id=None):
        log = self.log(status='SAVED', log_id=log_id)
        return log.id

    def log(self, status, log_id=None):
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
        if status == 'SENT':
            email_log.date_sent = now()
        if self.content_object:
            email_log.content_object = self.content_object
        email_log.save()

        return email_log

    def _process_and_send(self):

        if cotimail_settings.RECIPIENTS_OVERRIDE:
            recipients = cotimail_settings.RECIPIENTS_OVERRIDE
        else:
            recipients = self.recipients

        msg = EmailMultiAlternatives(
            subject=self.get_subject(),
            body=self.get_body_txt(),
            from_email=self.sender,
            to=recipients,
            reply_to=[self.reply_to],
            headers=self.headers  # optional extra headers
        )
        if self.html_template:
            msg.attach_alternative(self.get_body_html(), "text/html")

        if self.attachments:
            for attachment in self.attachments:
                if 'file' in attachment and 'filename' in attachment:
                    msg.attach(
                        attachment['filename'],
                        attachment['file'],
                        attachment['content_type']
                    )
                else:
                    msg.attach_file(
                        attachment['file_path'],
                        attachment['content_type']
                    )

        # Send the message
        try:
            response = msg.send()
            return response
        # Ignore refused response, probably spam
        except AnymailRecipientsRefused:
            return None
