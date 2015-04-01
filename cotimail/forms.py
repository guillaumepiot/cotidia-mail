from django import forms

class NoticeForm(forms.Form):
	
	first_name = forms.CharField(label='First name', max_length=100)
	last_name = forms.CharField(label='Last name', max_length=100)
	email = forms.EmailField()
	body = forms.CharField(label='Content', max_length=1000, widget = forms.Textarea)

