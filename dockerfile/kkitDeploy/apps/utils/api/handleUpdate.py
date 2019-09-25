import os

import json,redis
from string import Template
from kkitDeploy.settings import redisPool, updateScriptPackage, scriptPackage
redisInstace = redis.Redis(connection_pool=redisPool)

__all__ = [
    'getItemPack'
    ]

class getItemPack():

    def getItem(self):

        os.system("chmod -R 755 "+scriptPackage)
        fetchItemTemplate = Template('${s1} ${s2}')
        fetchItemCmd = fetchItemTemplate.safe_substitute(s1=updateScriptPackage,s2=scriptPackage)
        cmdState=os.system(fetchItemCmd)
        os.system("chmod -R 755 " + scriptPackage)

        outTime=604800
        if cmdState:
            return False
        else:
            redisInstace.set("update","succeed",outTime)
            return True


if __name__ == "__main__":
    getItemPack.getItem()

