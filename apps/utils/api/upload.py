import os
from django.core.cache import cache
from rest_framework.views import APIView
from rest_framework.views import Response, status
from kkitDeploy import settings
from . import handleCommand

__all__ = [
'Upload','changeBaseConfig','UnRarUploadFile'
]

class Upload(APIView):
    response = Response({
        'detail': '脚本已经 上传完毕！',
    }, status=status.HTTP_200_OK)
    def post(self,request):

        deployName=request.data.get("deployName")

        if deployName:
            myFile = request.FILES.get("file", None)
            if myFile:
                dir = settings.scriptPackage+deployName+"/conf.d"
                destination = open(os.path.join(dir, myFile.name),
                                   'wb+')
                for chunk in myFile.chunks():
                    destination.write(chunk)
                destination.close()

            return self.response
        else:
            myFile = request.FILES.get("file", None)
            if myFile:
                dir = settings.scriptPackage
                destination = open(os.path.join(dir, myFile.name),
                                   'wb+')
                for chunk in myFile.chunks():
                    destination.write(chunk)
                destination.close()

            return self.response

class changeBaseConfig(APIView):


    def __init__(self,fileObject,dir,ObjectName):
        self.fileObject = fileObject
        self.dir = dir
        self.ObjectName = ObjectName
    def changeConfig(self):
        if self.ObjectName:
            try:
                dir = self.dir
                destination = open(os.path.join(dir, self.ObjectName),
                                   'wb+')
                destination.write((self.fileObject).encode())
                destination.close()

                return "配置文件修改成功"
            except Exception as e:
                return e


class UnRarUploadFile(APIView):

    def post(self,request):
        rarFileName=request.data.get('name')
        result,info=handleCommand.UnRar(rarFileName)
        if result:
            name = rarFileName.split('.')
            redisResult, redisInfo =handleCommand.readBaseConfig(name[0])

            if redisResult:
                response = Response({
                    'detail': redisInfo,
                }, status=status.HTTP_200_OK)
                customData = cache.get('customData')
                if customData:
                    customData.append(name[0])
                    customData=list(set(customData))
                    cache.set("customData", customData, None)
                    return response
                else:
                    response = Response({
                        'detail': redisInfo,
                    }, status=status.HTTP_200_OK)
                    tmpList = []
                    tmpList.append(name[0])
                    cache.set("customData", tmpList, None)
                    return response
            else:
                response = Response({
                    'detail': redisInfo,
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                return response
        else:
            response = Response({
                'detail': info,
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return response