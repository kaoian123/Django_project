from rest_framework import serializers
from users.models import Profile
from users.utils import mask_name


class ProfilePublicSerializer(serializers.ModelSerializer):
    masked_name = serializers.SerializerMethodField()
    education = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ["avatar", "masked_name", "education", "slug"]

    def get_masked_name(self, obj):
        return mask_name(obj.full_name or obj.user.username)

    def get_education(self, obj):
        return obj.get_education_display()
