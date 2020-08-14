from django import forms
from phonenumber_field.formfields import PhoneNumberField
from django.utils.translation import gettext_lazy as _
from django.core.mail import send_mail
from . import models


class ContactForm(forms.ModelForm):
    # sender_request = forms.ModelMultipleChoiceField(queryset=models.Product.objects.all())

    class Meta:
        model = models.ContactUsMessage
        fields = ('sender_name', 'sender_email', 'sender_number', 'sender_message', 'sender_request')
        widgets = {
            'sender_name': forms.TextInput(attrs={
                                                'type': "text",
                                                'class': "form-control",
                                                'id': "name",
                                                'name': "name",
                                                'placeholder': "Enter your name",
                                                'onfocus': "this.placeholder = ''",
                                                'onblur': "this.placeholder = 'Enter your name'",
                                                }),
            'sender_email': forms.EmailInput(attrs={
                                                'type':"email",
                                                'class':"form-control",
                                                'id':"email",
                                                'name':"email",
                                                'placeholder':"Enter email address",
                                                'onfocus':"this.placeholder = ''",
                                                'onblur':"this.placeholder = 'Enter email address'",
                                                }),
            'sender_number': forms.TextInput(attrs={
                                                'type': "text",
                                                'class': "form-control",
                                                'id': "name",
                                                'name': "name",
                                                'placeholder': "+90(535)6832320",
                                                'onfocus': "this.placeholder = ''",
                                                'onblur': "this.placeholder = 'Enter your phone number'",
                                                }),
            'sender_message': forms.Textarea(attrs={
                                                'class':"form-control",
                                                'name':"message",
                                                'id':"message",
                                                'rows':"1",
                                                'placeholder':"Enter Message",
                                                'onfocus':"this.placeholder = ''",
                                                'onblur':"this.placeholder = 'Enter Message'"
                                                }),
            'sender_request': forms.CheckboxSelectMultiple(attrs={'multiple': True})
        }



#     def send_email(self, current_url):
#         name = self.cleaned_data['name']
#         message = self.cleaned_data['message']
#         client_email = self.cleaned_data['client_email']
#         client_phone = self.cleaned_data['client_phone']
#         recipients = ['contact@gammaturkey.com', client_email]
#         mail_subject = 'Gamma Turkey Received Your Message - {}'.format(name)
#
#         message_edited = '''Dear {},
#
# Many thanks for contacting us.
# We have successfully received your below message. Our team will contact you shortly.
#
# ___________________________________________
# The URL address of the form: {}
# {} - Phone Number: {} - eMail Address: {}
#
# {}
#
# ___________________________________________
# Kind Regards,
# Gamma Turkey team
# https://www.gammaturkey.com
# '''
#         message_edited = message_edited.format(name, current_url, name,client_phone, client_email, message)
#         send_mail(mail_subject, message_edited, 'contact@gammaturkey.com', recipients)
#         pass
