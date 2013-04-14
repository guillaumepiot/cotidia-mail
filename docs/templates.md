Templates
=========

Notice templates
----------------

Cotimal uses the [HTML Email Boilerplate](http://htmlemailboilerplate.com/) as a basic architecture.

### Base template (HTML)

The main HTML template to be used by all notice types.

_Location: notice/base.html_

Variables:

	{% block title %}{% endblock %}
	
The title of the email. Mainly for reference purpose as it will not be displayed by the email clients.

	{% block content %}{% endblock %}
	
The main content of the email, provided by partial templates associated directly to each notice type.

> The default width of the email is set to 600px, to ensure maximum compatibility with most email clients restrictions. More useful information on the [Campaign Monitor website](http://www.campaignmonitor.com/resources/will-it-work/width/).

### Base template (TXT)

The text version fallback for the base, targetted at email clients that doesn't support HTML email. It also improves scores with spam filters.

_Location: notice/base.txt_

Variables:

	{% block content %}{% endblock %}
	
> Please note that the "title" variable is not included as it would be displayed on the email (which we don't want).

### Default template (HTML)

Each notice type will be associated with a partial template, which will inherit from the base template.

_Location: notice/default.html_

	{% extends 'notice/base.html' %}{% load i18n %}
	{% block title %}Default title{% endblock %}
	{% block content %}

		default content...

	{% endblock %}
	
### Default template (TXT)

A fallback text version for the default notice template.

_Location: notice/default.txt_

	{% extends 'notice/base.txt' %}{% load i18n %}
	{% block content %}
		Hello!
	{% endblock %}