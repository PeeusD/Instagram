from django import forms 
from django.contrib.auth import get_user_model
User = get_user_model()


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['picture', 'full_name', 'username', 'email', 'bio', 'website', 'phone_number', 'gender', 'is_private_account',]
        labels = {'is_private_account':'Do you wanna make this account private?'}


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for field in self.fields:
            if field == 'picture':
                self.fields[field].widget.attrs.update({'class': 'edit-profile__avatar',})
                self.fields[field].widget.clear_checkbox_label = 'clear'
                self.fields[field].widget.initial_text = "currently"
                self.fields[field].widget.input_text = "change"
            elif field == 'is_private_account':
                self.fields[field].widget.attrs.update({'class': 'form__label',})
            else:
                self.fields[field].widget.attrs.update({'class': 'form__input',})
