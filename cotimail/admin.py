from django.contrib import admin
from django.forms import forms

from .models import *
from .notice import *

class emailAdmin(admin.ModelAdmin):
	date_hierarchy = 'date_created'
	list_display = ['subject','name','status']
	list_display_links = ['subject']
	list_editable = ['status']
	list_filter = ['subject','name','status']
	search_fields = ['title', 'content']

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

admin.site.register(EmailLog, emailAdmin)



