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

Run the migration:

    $ python manage.py migrate cotimail

Settings
--------

**MANDRILL_API_KEY**

Default: **"myapp-api-key"** (string)

Cotimail uses Mandrill to send email, you will need to enter the API key:

    MANDRILL_API_KEY = "<myapp-api-key>"

**COTIMAIL_REPLY_EMAIL**

Default: "noreply@mywebsite.com"

    COTIMAIL_REPLY_EMAIL = "noreply@mywebsite.com"

**COTIMAIL_APPS**

Default: []

List the apps that contains notices to be included in the admin. Cotimail allow you to preview and create email from those notices.

	# Define a list of apps supporting notices. The list should be pointing to individual notices.py
	COTIMAIL_APPS = [
		'booking.notices',
	]
		
	# Enter your Mandrill APY key
	MANDRILL_API_KEY = "myapp-api-key"
		
	# Setup the Django email backend
	EMAIL_BACKEND = "djrill.mail.backends.djrill.DjrillBackend"

	# Use the local css inlining feature
	# Default: False
	COTIMAIL_INLINE_CSS_LOCAL = getattr(settings, 'COTIMAIL_INLINE_CSS_LOCAL', False)

	# Use MAndrill css inlining feature - email max limit is 256KB
	# Default: True
	COTIMAIL_INLINE_CSS_MANDRILL = getattr(settings, 'COTIMAIL_INLINE_CSS_MANDRILL', True)

	# Queue mail using logs rather than sending straight away
	# Default: True
	COTIMAIL_QUEUE_MAIL = True

	# Save email log in the database, it will be forced to True if COTIMAIL_QUEUE_MAIL is True
	# Default: True
	COTIMAIL_LOG_MAIL = True

	# How long to wait for the lock to become available. Default of -1 means to never wait for the lock to become available.
	# This only applies when using crontab setup to execute the emit_notices management command to send queued messages rather # than sending immediately.
	# Default: -1
	COTIMAIL_LOCK_WAIT_TIMEOUT = -1



Enable admin management
-----------------------

You can access the notice logs and send notice emails from the admin. To do so, you will need to provide the URLs to the admin views and optionally add a menu item to navigate to it.

Add the following rule to your urls.py:

    url(r'^admin/notification/', include('cotimail.urls', namespace="cotimail")),

Register the menu with the account menu manager (in `admin.py`):

    from account.menu import menu
    menu.register("cotimail", "admin/cotimail/menu.html", 1) # 1 being the order id