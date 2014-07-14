# About

Cotimail is a transaction email manager for Django. It is built for applications that rely on transactional email to communicate with their users, allowing the management and sending of transactional emails in large quantities. This is all done while keeping control of content, style and history.

It users Djrill (a Mandrill API integration) to send emails, though doesn't use its templating ability as this is done by Cotimail.

Features:

- Preview all email notices available in the application (both in HTML and TXT).
- Send email with a form to override the default context, and select a list of recipients.
- Keep a transaction history from email logs.
- Create email queues from un-sent logged emails, and manageable by a cron job by using a Django command.
- Relate an email notice to any object instance in the application.
- Create notices on a per app basis by extending the default notice model.
- Create and send notices from any level in the application, including public views, admin views and signals.
