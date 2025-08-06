from django import forms
from django.core.files.uploadedfile import UploadedFile

from ..models import Profile

import re


class ProfileForm(forms.models.ModelForm):

    class Meta:
        model = Profile
        fields = [
            "full_name",
            "age",
            "education",
            "avatar",
        ]
        labels = {
            "full_name": "姓名",
            "age": "年齡",
            "education": "教育程度",
            "avatar": "頭像",
        }
        widgets = {
            "full_name": forms.TextInput(attrs={"placeholder": "請輸入全名"}),
            "age": forms.NumberInput(attrs={"placeholder": "請輸入年齡"}),
            "education": forms.Select(),
            "avatar": forms.FileInput(
                attrs={
                    "accept": "image/png,image/jpeg,image/jpg",
                }
            ),
        }
        error_messages = {
            "full_name": {
                "required": "請輸入姓名",
                "max_length": "姓名超過長度限制",
            },
            "age": {
                "required": "請輸入年齡",
                "invalid": "請輸入有效的年齡",
                "min_value": "年齡不能為負數",
            },
            "education": {"required": "請選擇教育程度"},
            "avatar": {"invalid": "請上傳有效的圖片格式"},
        }

    def clean_full_name(self):
        full_name = self.cleaned_data.get("full_name")
        if not re.match(r"^[\u4e00-\u9fa5a-zA-Z0-9\s]+$", full_name):
            raise forms.ValidationError("姓名只能包含中文、英文和數字")
        return full_name

    def clean_avatar(self):
        avatar = self.cleaned_data.get("avatar")
        if avatar and isinstance(avatar, UploadedFile):
            valid_extensions = ["png", "jpg", "jpeg"]
            if not avatar.name.lower().endswith(tuple(valid_extensions)):
                raise forms.ValidationError("請上傳有效的圖片格式（PNG或JPEG）")
            max_size = 2 * 1024 * 1024
            if avatar.size > max_size:
                raise forms.ValidationError("圖片大小不能超過2MB")

            if avatar.content_type not in ["image/png", "image/jpeg"]:
                raise forms.ValidationError("請上傳有效的圖片格式（PNG或JPEG）")

        return avatar

    def save(self, commit=True):
        profile = super().save(commit=False)

        for field in ["full_name", "age", "education", "avatar"]:
            input_value = self.cleaned_data.get(field)
            if input_value in [None, "", "None"]:
                setattr(profile, field, getattr(self.instance, field))

        if commit:
            profile.save()
        return profile
