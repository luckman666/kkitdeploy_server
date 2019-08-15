from rest_framework.views import Response, status
from rest_framework.views import APIView

__all__ = [
    "UserLoginAPI", "UserInfoAPI", "UserLogoutAPI",
    ]

# 用户登录
class UserLoginAPI(APIView):

    def post(self, request, *args, **kwargs):

        return Response(status=status.HTTP_200_OK)

class UserInfoAPI(APIView):

    def get(self, request, *args, **kwargs):
        info_dist={}
        info_dist['username'] = request.user.username
        info_dist['roles'] = ['admin']
        return Response(info_dist, status=status.HTTP_200_OK)

class UserLogoutAPI(APIView):

    def post(self, request, *args, **kwargs):

        return Response(status=status.HTTP_200_OK)