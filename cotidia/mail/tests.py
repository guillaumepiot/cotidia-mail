from django.conf import settings
from django.core import mail
from django.urls import reverse
from django.test import TestCase
from django.test.client import Client

from cotidia.mail.notice import Notice

class NoticeTest(TestCase):

    def test_send_notice_default_values(self):

        notice = Notice()

        notice.send()

        # Test that one message has been sent.
        self.assertEqual(len(mail.outbox), 1)

        # Verify that the subject of the first message is correct.
        self.assertEqual(mail.outbox[0].subject, 'Default subject')

        # Check email attribute values
        email = mail.outbox[0]

        self.assertEqual(email.from_email, 'App <info@example.com>')
        self.assertEqual(email.recipients(), ['Firstname Lastname <firstname.lastname@example.com>',])
        self.assertEqual(email.reply_to, ['No-reply <noreply@mywebsite.com>'])
        self.assertEqual(email.extra_headers, {})
