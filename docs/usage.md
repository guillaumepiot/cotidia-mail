Usage
=====

Create a new notice
-------------------

Notices are basically an email type where the context and the template may vary. Also, it can be configured with any attributes that Mandrill allows to be passed via the API. A list of the attributes can be find on the [Djrill documentation](https://djrill.readthedocs.org/en/master/usage/sending_mail.html#mandrill-specific-options).

The notice will inherit the BaseNotice class and must follow those guidelines:

- Its class name must always terminate with 'Notice'.
- It must have a 'name' attribute
- It must have an  'identifier' attribute


	from cotimail import Notice

	class CustomNotice(Notice):
		# Use as a list display
		name = 'Custom name' 
		# Use for the preview URL as a slug, so it must not contains spaces or other symbols than lowercase letters and hyphens
		identifier = 'custom-name' 
		# Defines an HTML template for this notice
		html_template = 'path/to/template.html'
		text_template = 'path/to/template.txt'

		# A JSON representation of the context dictionary, which is the format it will be saved as in the EmailLog
		context = {'subject_var': 'My subject variable'}
		
		# Passing on come context variables to build the subject line 
		subject = u'%s %s' % ('Your enquiry for', context['subject_var'])
	
> It is recommend to add you notice template inside the app templates folder to keep it organised.

