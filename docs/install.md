Installation & Setup
====================

Getting Cotimail
----------------

You can install Cotimail from source by downloading the package from BitBucket: [https://bitbucket.org/guillaumepiot/cotimail](https://bitbucket.org/guillaumepiot/cotimail).

	$ python setup.py install

Though it is easier to install it using PIP: (not published yet)

	$ pip install cotimail

If you are a contributor and would like to make source code edit while working on a project, you can install the package in edit mode:

	$ pip install -e git+https://bitbucket.org/guillaumepiot/cotimail.git#egg=cotimail
	
	
Project setup
-------------

### settings.py

	# Setup a reply to email:
	# Default: reply@example.com
	COTIMAIL_REPLY_EMAIL = 'noreply@mywebsite.com'

	# Define a list of apps supporting notices. The list should be pointing to individual notices.py
	COTIMAIL_APPS = [
		'booking.notices',
	]
		
	# Enter your Mandrill APY key
	MANDRILL_API_KEY = "myapp-api-key"
		
	# Setup the Django email backend
	EMAIL_BACKEND = "djrill.mail.backends.djrill.DjrillBackend"

	# Add cotimail to your installed apps
	INSTALLED_APPS = (
		...
	    'cotimail',
	)

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

You can access the notice logs and send notice emails from the admin. To do so, you will need to provide the URLs to the admin views and optionally add a menu item to navigateto it.

Add the following rule to your urls.py:

	# Notices URL should be before the default admin ones
	url(r'^admin/notices/', include('cotimail.urls')),
	url(r'^admin/', include(admin.site.urls)),

If you are using Admin Tools, add a menu item for the admin

	...
	items.MenuItem(_('Notices'), '/admin/notices/'),
	...
