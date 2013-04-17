Installation & Setup
====================

Getting Cotimail
----------------

You can install Cotimail from source by downloading the package from BitBucket: [https://bitbucket.org/guillaumepiot/cotimail](https://bitbucket.org/guillaumepiot/cotimail).

	$ python setup.py install

Though it is easier to install it using PIP:

	$ pip install cotimail

If you are a contributor and would like to make source code edit while working on a project, you can install the package in edit mode:

	$ pip install -e git+https://bitbucket.org/guillaumepiot/cotimail.git#egg=cotimail
	
	
Project setup
-------------

### settings.py

	# Setup a reply to email:
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
