from django.conf import settings

# The default reply to email
COTIMAIL_REPLY_EMAIL = getattr(settings, 'COTIMAIL_REPLY_EMAIL', 'reply@example.com')
COTIMAIL_SENDER = getattr(settings, 'COTIMAIL_SENDER', 'App <no-reply@example.com>')


# A list of apps supporting the notice model
# Each item should point to the notices.py of each app

# Example:
# COTIMAIL_APPS = [
#     'booking.notices',
# ]

COTIMAIL_APPS = getattr(settings, 'COTIMAIL_APPS', [])

COTIMAIL_INLINE_CSS_LOCAL = getattr(settings, 'COTIMAIL_INLINE_CSS_LOCAL', False)

COTIMAIL_INLINE_CSS_MANDRILL = getattr(settings, 'COTIMAIL_INLINE_CSS_MANDRILL', True)

COTIMAIL_QUEUE_MAIL = getattr(settings, 'COTIMAIL_QUEUE_MAIL', True)

COTIMAIL_LOG_MAIL = getattr(settings, 'COTIMAIL_LOG_MAIL', True)

# Mail queueing requires the log to track unsent mail, so we must force COTIMAIL_LOG_MAIL to be True if COTIMAIL_QUEUE_MAIL is True
if COTIMAIL_QUEUE_MAIL == True:
	COTIMAIL_LOG_MAIL = True

COTIMAIL_LOCK_WAIT_TIMEOUT = getattr(settings, 'COTIMAIL_LOCK_WAIT_TIMEOUT', -1)

	