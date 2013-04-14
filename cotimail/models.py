from django.db import models 
from django.utils.translation import ugettext_lazy as _ 
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType


class EmailLog(models.Model):

	# Path to template files
	template_html = models.CharField(max_length=250)
	template_text = models.CharField(max_length=250)

	# Representation name of email
	name = models.CharField(max_length=250)

	# The complete subject
	subject = models.TextField()
	# A JSON string of the context
	body_vars = models.TextField()

	# The communication details
	recipients = models.TextField(help_text='A comma separated list of recipients')
	sender = models.EmailField(max_length=250)
	reply_to = models.EmailField(blank=True)

	# Content-object field
	# You can here hook any object the email may relate too
	content_type = models.ForeignKey(ContentType,
			verbose_name=_('content type'),
			related_name="content_type_set_for_%(class)s")
	object_pk = models.TextField(_('object ID'))
	content_object = generic.GenericForeignKey(ct_field="content_type", fk_field="object_pk")

	# Datetime stamp
	date_created = models.DateTimeField(auto_now_add=True)
	date_sent = models.DateTimeField(blank=True, null=True)

	def __unicode__(self):
		return u'%s' % self.subject

	class Meta:
		verbose_name = u'Email log'
		verbose_name_plural = u'Email logs'