from rest_framework.response import Response
from users.models import Profile
from users.api.serializers import ProfilePublicSerializer
from rest_framework.decorators import api_view

import time
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from users.utils import mask_name


@api_view(["GET"])
def public_profile_list(request):
    profiles = Profile.objects.filter(is_public=True)
    profiles_serializer = ProfilePublicSerializer(profiles, many=True)
    time.sleep(3)
    return Response(profiles_serializer.data)


@require_http_methods(["GET"])
def original_public_profile_list(request):
    profiles = Profile.objects.filter(is_public=True)

    profile_list = []
    for profile in profiles:
        profile_list.append(
            {
                "avatar": profile.avatar.url,
                "masked_name": mask_name(profile.full_name or profile.user.username),
                "education": profile.get_education_display(),
                "slug": profile.slug,
            }
        )
    time.sleep(5)
    return JsonResponse(profile_list, safe=False)
