import subprocess
import time,re,json,os,rarfile
import paramiko
import json,redis
from kkitDeploy.settings import redisPool,scriptBasePath,scriptPackage,sendScript,sendScriptBasePath
from string import Template
from channels.generic.websocket import WebsocketConsumer
from kkitDeploy.settings import RSA_PRIVATE_KEY_FILE
__all__ = [
'wsScheduleJob','fetchMasterIp','checkYml','UnRar'
]

redisInstace = redis.Redis(connection_pool=redisPool)

class wsScheduleJob(WebsocketConsumer):

    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):

        text_data_json = json.loads(text_data)
        self.masterIp = text_data_json.get("masterIp")
        self.deployName = text_data_json.get("deployName")
        self.deployTimeout = text_data_json.get("TimeOutValue")

        cwd = scriptBasePath
        self.cmdScript("chmod -R 755 .", cwd)

        writeConfigTemplate = Template('${s1} ${s2} ${s3}')
        writeConfigCmd = writeConfigTemplate.safe_substitute(s1=sendScript, s2=scriptPackage, s3=self.deployName)
        cwd = sendScriptBasePath
        self.cmdScript(writeConfigCmd, cwd)

        execTemplate = Template('/root/${s1}/${s2}.sh 1>&2')
        deployCommand = execTemplate.safe_substitute(s1=self.deployName, s2=self.deployName)

        self.runScript(deployCommand)

    def cmdScript(self,cmd,cwd=None):
        number=0
        proc = subprocess.Popen(cmd, shell=True, universal_newlines=True, stderr=subprocess.STDOUT,stdout=subprocess.PIPE,cwd=cwd)
        try:
            for message in iter(proc.stdout.readline, 'b'):

                if message == '' and proc.poll() != None:
                    time.sleep(1)

                    number += 1
                    if number > 5:
                        break
                else:
                    number = 0
                    self.send(json.dumps({'message': message}))

        except Exception as e:

            self.send(json.dumps({'message': e}))

    def runScript(self,deployCommand):

        self.s = paramiko.SSHClient()
        self.s.load_system_host_keys()
        self.s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.key = paramiko.RSAKey.from_private_key_file(RSA_PRIVATE_KEY_FILE)

        self.s.connect(hostname=self.masterIp,
                  port=int(22),
                  username="root",
                  pkey=self.key,
                  timeout=self.deployTimeout)
        stdin, stdout, stderr = self.s.exec_command(deployCommand,get_pty=True)
        number=0
        try:
            while True:
                nextline = stdout.readline().strip()

                if not nextline:
                    time.sleep(1)
                    number +=1
                    if number > 5:
                        self.send(json.dumps({'message': '52j840y$0_j%aa&'}))
                        break
                else:
                    number = 0
                    self.send(json.dumps({'message': nextline}))
        except Exception as e:
            self.send(json.dumps({'message': e}))
        self.s.close()

def fetchMasterIp(fileName):
    fopen = open(fileName, 'r')
    file_read = fopen.read()
    comment = re.compile(r'masterip="(.*?)"')
    ret = comment.findall(file_read)[0]
    return ret

def checkYml(fileName):

    ymlTemplate = Template('${s1}/${s2}/${s3}.yml')
    ymlFile = ymlTemplate.safe_substitute(s1=scriptPackage, s2=fileName,s3=fileName)
    status = os.path.isfile(ymlFile)
    return status

def readYml(fileName):
    ymlTemplate = Template('${s1}/${s2}/${s3}.yml')
    ymlFile = ymlTemplate.safe_substitute(s1=scriptPackage, s2=fileName,s3=fileName)
    yml = open(ymlFile,"r")
    ymlInfo = yml.read()
    return ymlInfo

def UnRar(fileName):

    rarTemplate = Template('${s1}${s2}')
    rarFilePach = rarTemplate.safe_substitute(s1=scriptPackage, s2=fileName)
    UnRarTemplate = Template('${s1}')
    UnRarFilePach = UnRarTemplate.safe_substitute(s1=scriptPackage)
    try:
        rf = rarfile.RarFile(rarFilePach)
        rf.extractall(UnRarFilePach)
        return True,"脚本已经 上传完毕！"
    except Exception as e:
        return False,e

def readBaseConfig(fileName):
    baseTemplate = Template('${s1}/${s2}/${s3}')
    baseFile = baseTemplate.safe_substitute(s1=scriptPackage, s2=fileName,s3='base.config')
    try:
        base = open(baseFile,"r")
        baseConfigInfo = base.read()
        redisInstace.set(fileName,baseConfigInfo)
        return True, "脚本已经上传完毕并成功初始化了数据！"
    except Exception as e:
        return False, e
