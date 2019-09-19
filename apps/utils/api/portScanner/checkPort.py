from rest_framework.views import APIView
from ..handleCommand import wsScheduleJob
from string import Template
from kkitDeploy.settings import checkPortPath

class checkPort(APIView):

    def post(self, request):

        checkPortIp=request.data.get('checkPortIp')
        writeConfigTemplate = Template('${s1} ${s2} ${s3} ${s4}')
        writeConfigCmd = writeConfigTemplate.safe_substitute(s1='/usr/bin/python3', s2=checkPortPath+'main.py', s3='-d', s4=checkPortIp)
        wsScheduleJob.cmdScript(writeConfigCmd,writeConfigCmd)
