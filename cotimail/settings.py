from django.conf import settings

# The default reply to email
COTIMAIL_REPLY_EMAIL = getattr(settings, 'COTIMAIL_REPLY_EMAIL', 'reply@example.com')

# A list of apps supporting the notice model
# Each item should point to the notices.py of each app

# Example:
# COTIMAIL_APPS = [
#     'booking.notices',
# ]

COTIMAIL_APPS = getattr(settings, 'COTIMAIL_APPS', [])

	