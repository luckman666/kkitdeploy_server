from django.urls import path
from ..api import handleCommand
from ..api import upload as uploadAPI
from ..api.portScanner import checkPort


urlpatterns=[

    # upload api
    path(r'v1/upload/', uploadAPI.Upload.as_view()),
    # upload api
    path(r'v1/UnRarUploadFile/', uploadAPI.UnRarUploadFile.as_view()),
    path(r'v1/checkPort/', checkPort.checkPort.as_view()),

]