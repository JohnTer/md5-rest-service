from django import forms
from django.core.exceptions import ValidationError

class MessageForm(object):
    @staticmethod
    def get_invalid_data_dict():
        return {'response': 'invalid data'}



class CreateTaskForm(forms.Form, MessageForm):
    url = forms.URLField()
    email = forms.EmailField(required=False)



class GetTaskForm(forms.Form, MessageForm):
    id = forms.UUIDField()