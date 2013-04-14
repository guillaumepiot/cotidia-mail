Templates
=========

Notice templates
----------------

Cotimal uses the [HTML Email Boilerplate](http://htmlemailboilerplate.com/) as a basic architecture.

### Base template (HTML)

The main HTML template to be used by all notice types.

Location: notice/base.html

Variables:

**title**

	{% block title %}{% endblock %}
	
The title of the email. Mainly for reference purpose as it will not be displayed by the email clients.

**content**

	{% block content %}{% endblock %}
	
The main content of the email, provided by partial templates associated directly to each notice type.

<p class="alert alert-info">The default width of the email is set to 600px, to ensure maximum compatibility with most email clients restrictions. More useful information on the [Campaign Monitor website](http://www.campaignmonitor.com/resources/will-it-work/width/).</p>

### Base template (TXT)

The text version fallback for the base, targetted at email clients that doesn't support HTML email. It also improves scores with spam filters.

Location: notice/base.txt

Variables:

**content**

	{% block content %}{% endblock %}
	
<p class="alert alert-info">Please note that the "title" variable is not included as it would be displayed on the email (which we don't want).</p>

### Default template (HTML)

Each notice type will be associated with a partial template, which will inherit from the base template.

Location: notice/default.html

	{% extends 'notice/base.html' %}{% load i18n %}
	{% block title %}Default title{% endblock %}
	{% block content %}

		default content...

	{% endblock %}
	
### Default template (TXT)

A fallback text version for the default notice template.

Location: notice/default.txt

	{% extends 'notice/base.txt' %}{% load i18n %}
	{% block content %}
		Hello!
	{% endblock %}