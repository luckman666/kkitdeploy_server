from django.urls import path
from ..utils.api import handleCommand
from . import consumers
websocket_urlpatterns=[

    path(r'v1/wInfo/create/', handleCommand.wsScheduleJob),
    # path(r'v1/wInfo/create/', consumers.DeployResult),


    # path(r'v1/wInfo/get/', handleShellCommand.ScheduleJob.as_view()),

]