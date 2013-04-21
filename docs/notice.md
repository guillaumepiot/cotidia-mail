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


Notice**.send([force_now])**

Prepare the notice based on the settings. 
Uses the `COTIMAIL_QUEUE_MAIL` setting to either send it using the `process_and_send` method or log it the database using `log`.

You can force the email to be sent straight away, overriding the `COTIMAIL_QUEUE_MAIL` setting by passing `force_now` as `True`.


Notice**.queue()**

Create an email log as `QUEUED` to be sent by the `send` command. 


Notice**.log(status)**

Log the notice in the database.


Notice**.process_and_send()**

If no notice object is supplied, then it will assume to triggered by the instance itself and will use `self` as the notice object. It will then set the notice attributes for Mandrill API and send the email right away.
