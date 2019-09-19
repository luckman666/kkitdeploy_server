from django.core.cache import cache
from rest_framework.views import APIView,Response, status
from kkitDeploy.settings import redisPool,scriptPackage
from apps.utils.api import handleCommand,handleUpdate
from apps.utils.api.handleUpdate import getItemPack
from apps.utils.api.upload import changeBaseConfig
import json,redis,os


redisInstace = redis.Redis(connection_pool=redisPool)

__all__ = [
'deployCreateAPI','AllTypeAPI','metadataConfigAPI','metadataConfigUpdateAPI','Update'
]



class Update():

    def __init__(self):
        try:
            updataResuslt=redisInstace.get("update")
            if updataResuslt:
                pass
            else:
                handleUpdate.getItemPack.getItem()
        except Exception as e:
            print(e)




class deployCreateAPI(APIView):

    def post(self, request):
        print('request.data',request.data)

class AllTypeAPI(APIView,getItemPack):

    def get(self,*args, **kwargs):
        deployType={}
        metaData = cache.get('metaData')
        customData = cache.get('customData')
        updataResuslt = redisInstace.get("update")
        if updataResuslt:
            pass
        else:
            self.getItem()

        deployType['metaData'] = metaData
        deployType['customData'] = customData
        response = Response({
            json.dumps(deployType),
        }, status=status.HTTP_200_OK)
        return response

class metadataConfigAPI(APIView,Update):
    def post(self, request):
        deployName=request.data.get('deployName')

        try:

            deployObjectConfig = redisInstace.get(deployName)

            response = Response({
                deployObjectConfig
            }, status=status.HTTP_200_OK)
        except Exception as e:
            response = Response({e},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return response

class metadataConfigUpdateAPI(APIView,Update):

    def post(self, request):
        deployName = request.data.get('deployName')
        configFile = request.data.get('configFile')
        redisInstace.set(deployName, configFile)
        deployConfig = deployName + '/base.config'
        try:
            writeConfig = changeBaseConfig(configFile, scriptPackage, deployConfig)
            writeConfigRutl = writeConfig.changeConfig()
            masterIp=handleCommand.fetchMasterIp(scriptPackage + deployConfig)
            writeConfigInfo = {}
            ymkExistStatus=handleCommand.checkYml(deployName)
            if ymkExistStatus:
                ymlData=handleCommand.readYml(deployName)
                writeConfigInfo['ymkFile'] = ymlData
                writeConfigInfo['writeConfigRutl'] = writeConfigRutl
                writeConfigInfo['masterIp'] = masterIp
                writeConfigInfo['deployName'] = deployName
                return Response(writeConfigInfo, status=status.HTTP_200_OK)
            else:
                writeConfigInfo['writeConfigRutl'] = writeConfigRutl
                writeConfigInfo['masterIp'] = masterIp
                writeConfigInfo['deployName'] = deployName
                return Response(writeConfigInfo, status=status.HTTP_200_OK)
        except Exception as e:
            writeConfigInfo = {}
            writeConfigInfo['writeConfigRutl'] = e
            return Response(writeConfigInfo, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class metadataYmlConfigUpdateAPI(APIView,Update):

    def post(self, request):
        deployName = request.data.get('deployName')
        configFile = request.data.get('configFile')

        deployYmlConfig = deployName + '/' + deployName + '.yml'
        deployConfig = deployName + '/base.config'
        try:
            writeConfig = changeBaseConfig(configFile, scriptPackage, deployYmlConfig)
            writeConfigRutl = writeConfig.changeConfig()
            masterIp=handleCommand.fetchMasterIp(scriptPackage + deployConfig)
            writeConfigInfo = {}
            writeConfigInfo['writeConfigRutl'] = writeConfigRutl
            writeConfigInfo['masterIp'] = masterIp
            writeConfigInfo['deployName'] = deployName
            return Response(writeConfigInfo, status=status.HTTP_200_OK)
        except Exception as e:
            writeConfigInfo = {}
            writeConfigInfo['writeConfigRutl'] = e
            return Response(writeConfigInfo, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
