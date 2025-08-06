from django import forms
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    email = forms.EmailField(
        label="信箱",
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "請輸入使用者名稱"}),
        error_messages={
            "required": "請輸入使用者名稱",
            "invalid": "請輸入有效的信箱格式",
        },
    )
    password = forms.CharField(
        label="密碼",
        required=True,
        widget=forms.PasswordInput(attrs={"placeholder": "請輸入密碼"}),
        error_messages={"required": "請輸入密碼"},
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")

        if email and password:
            try:
                user_obj = User.objects.get(email=email)
            except User.DoesNotExist:
                raise forms.ValidationError("信箱或密碼錯誤")

            user = authenticate(username=user_obj.username, password=password)
            if user is None:
                raise forms.ValidationError("使用者名稱或密碼錯誤")

            self.user = user
        return cleaned_data

    def login(self, request):
        """用於登錄用戶的輔助方法。"""
        if (
            hasattr(self, "user")
            and self.user is not None
            and self.user.is_authenticated
        ):
            auth_login(request, self.user)
        else:
            raise ValueError("用戶未經驗證，無法登錄。")
