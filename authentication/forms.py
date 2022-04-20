
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
User = get_user_model()
class UserForm(UserCreationForm):  # Signup form
    class Meta:
        model = User
        fields = ['full_name', 'email', 'username', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for field in self.fields:    # adding class to form input using label
            if field:
                self.fields[field].widget.attrs.update({'class': 'form__input',})

class CustomUserChangeForm(UserChangeForm): #Login form
    class Meta:
        model = User
        fields = ['full_name', 'email', 'username']
