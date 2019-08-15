#!/bin/bash
bash_path=$(cd "$(dirname "$0")";pwd)
log="./setup.log"  #操作日志存放路径
fsize=2000000
exec 2>>$log  #如果执行过程中有错误信息均输出到日志文件中
updateScript(){
unalias cp
test -d kkitDeployScriptPackage || mkdir kkitDeployScriptPackage 
cd kkitDeployScriptPackage
git clone https://gitee.com/yb2018/kkitDeployScriptPackage.git && cd kkitDeployScriptPackage && cp -rf * .. 
cd $bash_path
rm -rf $bash_path/kkitDeployScriptPackage/kkitDeployScriptPackage
}
updateScript > ./setup.log 2>&1

