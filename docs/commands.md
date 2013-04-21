Commands
========

Send the logged notices
-----------------------

`python manage.py send_logged_notices`

This command will send all the notices with status `QUEUED` or `FAILED`.

The status indicator wil inform whether Mandrill has confirmed positively the API call or not. It will not indicated if the email is actually sent, as only Mandrill will queue it and send it whenever possible.