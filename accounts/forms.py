from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth import get_user_model
from django import forms


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = [
            'username',
            'email',
        ]
        
class CustomUserUpdateForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = ['username', 'email',] 
        exclude = ('password', ) 

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'password' in self.fields:
            del self.fields['password']
class CustomUserUpdateForm2(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = ['username', 'email'] 
        exclude = ('password', ) 

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'password' in self.fields:
            del self.fields['password']
        
class CustomUserPasswordUpdateForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['old_password'].label = "기존 비밀번호"
        self.fields['new_password1'].label = "새 비밀번호"
        self.fields['new_password2'].label = "새 비밀번호 (확인)"
        
        for field_name in ['old_password', 'new_password1', 'new_password2']:
            self.fields[field_name].help_text = None

        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'placeholder': field.label,
                'class': 'form-control', 
            })

    class Meta:
        model = get_user_model()
        fields = ['password']
        
class UserProfileForm(forms.ModelForm):
    created_at = forms.DateTimeField(disabled=True, required=False)
    class Meta:
        model = get_user_model()
        # fields = ("username", "profile_picture", 'follows', 'created_at')
        fields = ("username",)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 특정 필드를 읽기 전용으로 설정
        self.fields['username'].disabled = True
        if self.instance and self.instance.created_at:
            self.fields['created_at'].initial = self.instance.created_at