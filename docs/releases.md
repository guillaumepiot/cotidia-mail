Releases
========

Version 0.1
-----------

- Ability to preview all email notices available in the application (both in HTML and TXT).
- Ability to send email with a form to override the default context, and select a list of recipients.
- Ability to keep a transaction history from email logs.
- Ability to create email queues from un-sent logged emails, and manageable by a cron job by using a Django command.
- Ability to relate an email notice to any object instance in the application.
- Ability to create notices in a app basis by extending the default notice model.
- Ability to create and send notice from any level in the application, including public views, admin views and signals.