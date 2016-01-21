from django.conf import settings

COTIMAIL_REPLY_EMAIL = getattr(settings, 'COTIMAIL_REPLY_EMAIL', 'No-reply <noreply@mywebsite.com>')
COTIMAIL_SENDER = getattr(settings, 'COTIMAIL_SENDER', 'App <info@example.com>')
COTIMAIL_APPS = getattr(settings, 'COTIMAIL_APPS', [])
COTIMAIL_INLINE_CSS_LOCAL = getattr(settings, 'COTIMAIL_INLINE_CSS_LOCAL', False)
COTIMAIL_INLINE_CSS_MANDRILL = getattr(settings, 'COTIMAIL_INLINE_CSS_MANDRILL', True)
COTIMAIL_QUEUE_MAIL = getattr(settings, 'COTIMAIL_QUEUE_MAIL', True)
COTIMAIL_LOG_MAIL = getattr(settings, 'COTIMAIL_LOG_MAIL', True)

# Mail queueing requires the log to track unsent mail, so we must force COTIMAIL_LOG_MAIL to be True if COTIMAIL_QUEUE_MAIL is True
if COTIMAIL_QUEUE_MAIL == True:
	COTIMAIL_LOG_MAIL = True

COTIMAIL_LOCK_WAIT_TIMEOUT = getattr(settings, 'COTIMAIL_LOCK_WAIT_TIMEOUT', -1)

#
# In specific scenario, like DEBUG mode, we may want to force all email to be
# sent to a define list of recipients, for testing purpose.
# Set the value as a Python list of emails to enable the behaviour
#
RECIPIENTS_OVERRIDE = getattr(settings, 'COTIMAIL_RECIPIENTS_OVERRIDE', False)
	