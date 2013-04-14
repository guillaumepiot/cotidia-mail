from django.contrib import admin
from django import forms

from .models import *

# class EmailTemplateAdminForm(forms.ModelForm):
# 	html_template_code = forms.CharField(widget=CodeMirrorTextarea(mode="xml", theme="cobalt", config={ 'fixedGutter': True, 'htmlMode':True }))
	
# 	class Meta:
# 		model = EmailTemplate

# class EmailTemplateAdmin(admin.ModelAdmin):
# 	form = EmailTemplateAdminForm
# 	list_display = ["name", "subject", 'base_template']

# 	fieldsets = (
# 		('Email details', {
# 			'classes': ('default',),
# 			'fields': ('name', 'identifier', 'base_template')
# 		}),
# 		('Sending details', {
# 			'classes': ('default',),
# 			'fields': ('subject', 'reply_to',)
# 		}),
# 		('Template code', {
# 			'classes': ('default',),
# 			'fields': ('html_template_code', 'txt_template_code', )
# 		}),

		
# 	)


# class NoticeAdmin(admin.ModelAdmin):
# 	list_display = ["subject_vars", "recipient", "sender", "notice_type"]


# admin.site.register(EmailTemplate, EmailTemplateAdmin)
# admin.site.register(Notice, NoticeAdmin)