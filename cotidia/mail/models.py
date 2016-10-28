import pickle
import datetime
import json
import codecs

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

from cotidia.mail.utils import getNoticeClass

EMAIL_LOG_STATUS = (
    ('QUEUED', 'Queued'),
    ('SENT', 'Sent'),
    ('FAILED', 'Failed'),
    ('SAVED', 'Saved'),
)


class EmailLog(models.Model):

    # The complete subject
    subject = models.TextField()

    # Pickled notice
    pickled_data = models.TextField()

    # Representation name of email
    name = models.CharField(max_length=250)
    identifier = models.CharField(max_length=250)
    status = models.CharField(choices=EMAIL_LOG_STATUS, max_length=10)

    # Context
    context_json = models.TextField(null=True)

    # The communication details
    recipients = models.TextField(
        help_text='A comma separated list of recipients')
    sender = models.EmailField(max_length=250)
    reply_to = models.EmailField(blank=True)

    # Content-object field
    # You can here hook any object the email may relate too
    content_type = models.ForeignKey(
        ContentType,
        verbose_name=_('content type'),
        related_name="content_type_set_for_%(class)s",
        blank=True,
        null=True)
    object_pk = models.TextField(_('object ID'), blank=True, null=True)
    content_object = GenericForeignKey(
        ct_field="content_type",
        fk_field="object_pk")

    # Datetime stamp
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    date_sent = models.DateTimeField(blank=True, null=True)

    def __unicode__(self):
        return u'%s' % self.subject

    class Meta:
        verbose_name = u'Email log'
        verbose_name_plural = u'Email logs'
        ordering = ('-date_created',)

    def send(self):
        notice_obj = self.get_object()
        send = notice_obj._process_and_send()
        now = datetime.datetime.now()
        if send:
            self.status = 'SENT'
            self.date_sent = now
        else:
            self.status = 'FAILED'
        self.date_updated = now
        self.save()

        if self.status == 'SENT':
            return True
        else:
            return False

    def get_recipients(self):
        if self.recipients:
            try:
                recipients = json.loads(self.recipients)
            except:
                recipients = self.recipients.split(',')
            return recipients
        else:
            return []

    def get_object(self):
        try:
            notice = pickle.loads(
                codecs.decode(self.pickled_data.encode(), "base64")
            )
        except:
            notice_class = getNoticeClass(self.identifier)
            notice = notice_class(
                subject=self.subject,
                recipients=self.recipients,
                sender=self.sender,
                reply_to=self.reply_to,
            )

        # Pass the saved context to the notice directly
        if self.context_json:
            context = json.loads(self.context_json)
            notice.context.update(context)

        return notice
