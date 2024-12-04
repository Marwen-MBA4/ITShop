from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from .models import ProductReview,UserAddressBook

class SignupForm(UserCreationForm):
    class Meta:
        model=User
        fields=('first_name','last_name','email','username','password1','password2')
        
# Review Add Form
class ReviewAdd(forms.ModelForm):
    class Meta:
        model = ProductReview
        fields = ('review_text','review_rating')
        
# AddressBook Add Form
class AddressBookForm(forms.ModelForm):
    class Meta:
        model = UserAddressBook
        fields = ('address','mobile','status')
        
# ProfileEdit
class ProfileForm(UserChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].help_text = 'Raw passwords are not stored, so there is no way to see this user’s password, but you can change the password using <a href="/accounts/password_change/"> this form</a>.'
    class Meta:
        model = User
        fields=('first_name','last_name','email','username')