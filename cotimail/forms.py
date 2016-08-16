import json
from django import forms
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _

from form_utils.forms import BetterForm

FIELD_CLASS_MAP = {
    'charfield': {
        'field_class':forms.CharField,
        'field_widget':forms.TextInput,
        'max_length':250,
    },
    'textfield': {
        'field_class':forms.CharField,
        'field_widget':forms.Textarea,
        'max_length':50000,
    },
    'choicefield': {
        'field_class':forms.ChoiceField,
        'field_widget':forms.Select,
        'choices': (('','No choices'),)
    }
}

class NoticeForm(BetterForm):
    email = forms.CharField(
        max_length=250,
        widget=forms.TextInput(attrs={'class': 'form__text'})
        )

    def __init__(self, json_fields, *args, **kwargs):

        super(NoticeForm, self).__init__(*args, **kwargs)

        self._fieldsets = [
            ('main', {'fields': ['email'], 'legend': 'Settings'}),
        ]

        self.json_fields = json_fields

        # Go through each fieldset
        for fieldset in self.json_fields:

            fieldset_id = slugify(fieldset['fieldset']).replace('-','_')
            _fields = []
            for field in fieldset['fields']:

                # Get the name of the field
                field_name = '%s_%s' % (fieldset_id, field['name'])
                field_label = field['name'].replace('_', ' ').capitalize()

                # Get the field class from the field map
                field_type = field['type']
                field_class = FIELD_CLASS_MAP[field_type]['field_class']
                if FIELD_CLASS_MAP[field_type].get('field_widget'):
                    field_widget = FIELD_CLASS_MAP[field_type]['field_widget']
                else:
                    field_widget = None

                # Get the required option
                field_required = field['required']

                # Create a new form field

                kwargs = {
                    'required': field_required,
                    'label': field_label
                }

                if field_widget:
                    kwargs['widget'] = field_widget

                if FIELD_CLASS_MAP[field_type].get('max_length'):
                    kwargs['max_length'] = FIELD_CLASS_MAP[field_type]['max_length']

                if field.get('choices'):
                    kwargs['choices'] = field['choices']
                elif FIELD_CLASS_MAP[field_type].get('choices'):
                    kwargs['choices'] = FIELD_CLASS_MAP[field_type]['choices']

                self.fields[field_name] = field_class(**kwargs)

                if field_widget:
                    if field_widget.__name__ == 'Select':
                        self.fields[field_name].widget.attrs = {'class': 'form__select'}
                    if field_widget.__name__ == 'TextInput':
                        self.fields[field_name].widget.attrs = {'class': 'form__text'}
                    if field_widget.__name__ == 'Textarea':
                        self.fields[field_name].widget.attrs = {'class': 'form__text', 'rows': 10}
                else:
                    self.fields[field_name].widget.attrs = {'class': 'form__text'}

                # Push the field name to the temporary field list
                _fields.append(field_name)

            fieldset = (fieldset['fieldset'],{'fields':_fields, 'legend':fieldset['fieldset']})
            self._fieldsets.append(fieldset)

        # if self.instance:
        #     try:
        #         mask_data = json.loads(self.instance.content)
        #     except:
        #         mask_data = None

        #     if mask_data:

        #         # Go through each fieldset
        #         for fieldset in self.json_fields:
        #             fieldset_id = slugify(fieldset['fieldset']).replace('-','_')
        #             for field in fieldset['fields']:

        #                 # Get the name of the field
        #                 field_name = '%s_%s' % (fieldset_id,field['name'])

        #                 # Set the initial value from the current data
        #                 self.fields[field_name].initial = mask_data.get(field_name, '')


    # def save(self, *args, **kwargs):
    #     super(NoticeForm, self).save(*args, **kwargs)

    #     mask_data = {}

    #     # Create the mask data for each field
    #     for fieldset in self.json_fields:
    #         fieldset_id = slugify(fieldset['fieldset']).replace('-','_')
    #         for field in fieldset['fields']:

    #             # Get the field type
    #             field_type = field['type']
    #             # Get the name of the field
    #             field_name = '%s_%s' % (fieldset_id,field['name'])

    #             if field_type in ['pagelinkfield']:
    #                 if self.cleaned_data[field_name]:
    #                     page = self.cleaned_data[field_name]
    #                     mask_data[field_name] = page.id
    #             # elif field_type in ['imagefield', 'filefield']:
    #             #     mask_data[field_name] = self.cleaned_data[field_name].name
    #             else:
    #                 mask_data[field_name] = self.cleaned_data[field_name]

    #     self.instance.content = json.dumps(mask_data)
    #     self.instance.save()

    #     return self.instance
