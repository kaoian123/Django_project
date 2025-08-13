from rest_framework.response import Response
from users.models import Profile
from users.api.serializers import ProfilePublicSerializer
from rest_framework.decorators import api_view


@api_view(["GET"])
def public_profile_list(request):
    profiles = Profile.objects.filter(is_public=True)
    profiles_serializer = ProfilePublicSerializer(profiles, many=True)
    import time
    time.sleep(3)
    return Response(profiles_serializer.data)
