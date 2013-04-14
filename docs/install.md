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

Setup a reply to email:

	COTIMAIL_REPLY_EMAIL = 'noreply@mywebsite.com'

Define a list of apps supporting notices. The list should be pointing to individual notices.py

	COTIMAIL_APPS = [
		'booking.notices',
	]
	
