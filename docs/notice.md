Notice definition
=================

Properties
----------

Notice**.headers**

Assign the "Reply-To" header is reply_to attribute exists.


Notice**.get_identifier**

Return the `identifier` attribute as unicode.


Methods
-------

Notice**.get_context([context])**

Create a Django context object from the JSON dictionary (context passed while generate a new notice instance) and returns it.
`context` is optional, for overriding the current context.


Notice**.get_body_html([context])**

Render the template to html using the context.
`context` is optional, for overriding the current context.


Notice**.get_body_txt([context])**

Render the template to txt using the context.
`context` is optional, for overriding the current context.


Notice**.get_subject()**

Return the Notice's subject.


Notice**.send()**

Prepare the notice based on the settings. Either send it using the `process_and_send` method or log it the database using `log`.


Notice**.log(status)**

Log the notice in the database with the right status depending on the settings.
'QUEUED` for logging only
`SENT` for notice send right away


Notice**.process_and_send()**

If no notice object is supplied, then it will assume to triggered by the instance itself and will use `self` as the notice object. It will then set the notice attributes for Mandrill API and send the email right away.
