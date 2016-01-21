Installation & Setup
====================

Install using PIP straight from the repository:

    $ pip install git+https://bitbucket.org/guillaumepiot/cotimail.git

If you are a contributor and would like to make source code edit while working on a project, you can install the package in edit mode:

    $ pip install -e git+https://bitbucket.org/guillaumepiot/cotimail.git#egg=cotimail
	
Add `cotimail` to your project settings `INSTALLED_APPS`:

    INSTALLED_APPS = (
        ...
        'cotimail',
     )

Cotimail uses Mandrill ([Djrill](https://github.com/brack3t/Djrill)) to send email, you will need to enter the API key:

    MANDRILL_API_KEY = "<myapp-api-key>"

Instruct Django to use the Djrill email backend:

    EMAIL_BACKEND = "djrill.mail.backends.djrill.DjrillBackend"

Run the migration:

    $ python manage.py migrate cotimail

Settings
--------



**COTIMAIL_REPLY_EMAIL**

Default: `No-reply <noreply@mywebsite.com>`

Defines to default reply to email for all sent notifications. Please note that
this setting can be overridden on a notice basis.

**COTIMAIL_SENDER**

Default: `App <info@example.com>`

Defines to sender email for all sent notifications. Please note that
this setting can be overridden on a notice basis.

**COTIMAIL_APPS**

Default: `[]` (empty list)

List the apps that contains notices to be included in the admin. Cotimail allow you to preview and create email from those notices.

	COTIMAIL_APPS = [
		'booking.notices',
	]

**COTIMAIL_INLINE_CSS_LOCAL**

Default: `False`

Use the local css inlining feature.

**COTIMAIL_INLINE_CSS_MANDRILL**

Default: `True`

Use Mandrill css inlining feature - email max limit is 256KB

**COTIMAIL_QUEUE_MAIL**

Default: `True`
	
Queue mail using logs rather than sending straight away.

**COTIMAIL_LOG_MAIL**

Default: `True`

Save email log in the database, it will be forced to True if COTIMAIL_QUEUE_MAIL is True

**COTIMAIL_LOCK_WAIT_TIMEOUT**

Default: `-1` (Integer)

How long to wait for the lock to become available. Default of -1 means to never 
wait for the lock to become available. This only applies when using crontab 
setup to execute the send_logged_notices management command to send queued 
messages rather than sending immediately.



Enable admin management
-----------------------

You can access the notice logs and send notice emails from the admin. To do so, you will need to provide the URLs to the admin views and optionally add a menu item to navigate to it.

Add the following rule to your `urls.py`:

    url(r'^admin/notification/', include('cotimail.urls', namespace="cotimail")),

Register the menu with the account menu manager (in `admin.py`):

    from account.menu import menu
    menu.register("cotimail", "admin/cotimail/menu.html", 1) # 1 being the order id