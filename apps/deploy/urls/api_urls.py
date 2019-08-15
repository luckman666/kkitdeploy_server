from django.urls import path
from ..api import metadata,authority

urlpatterns=[
    path(r'login/', authority.UserLoginAPI.as_view()),
    path(r'userinfo/', authority.UserInfoAPI.as_view()),
    path(r'logout/', authority.UserLogoutAPI.as_view()),

    path(r'v1/metadata/bypage/', metadata.AllTypeAPI.as_view()),
    path(r'v1/metadata/config/bypage/', metadata.metadataConfigAPI.as_view()),
    path(r'v1/metadata/config/update/', metadata.metadataConfigUpdateAPI.as_view()),
    path(r'v1/metadata/ymlconfig/update/', metadata.metadataYmlConfigUpdateAPI.as_view()),

]