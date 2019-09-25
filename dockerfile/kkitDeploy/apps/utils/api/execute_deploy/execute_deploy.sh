#!/bin/bash
#b8_yang@163.com
scriptName=$0
deployName=$2
deployObjectPath=$1
all_num=1
#echo $scriptName
#echo $deployName
#echo $deployObjectPath
source $deployObjectPath/$deployName/base.config
bash_path=$(cd "$(dirname "$0")";pwd)


if [[ "$(whoami)" != "root" ]]; then
	echo "please run this script as root ." >&2
	exit 1
fi

echo -e "\033[31m 核心驱动脚本开始运行，关注我的个人公众号“devops的那些事”让我们开始这段感情吧！Please continue to enter or ctrl+C to cancel \033[0m"

#yum update
yum_update(){
	yum update -y
}
#configure yum source
yum_config(){

  test -d /etc/yum.repos.d/bak/ || yum install wget epel-release -y && cd /etc/yum.repos.d/ && mkdir bak && mv -f *.repo bak/ && wget -O /etc/yum.repos.d/CentOS-Base.repo http://mirrors.aliyun.com/repo/Centos-7.repo && wget -O /etc/yum.repos.d/epel.repo http://mirrors.aliyun.com/repo/epel-7.repo && yum clean all && yum makecache

}

yum_init(){
num=0
while true ; do
let num+=1
yum -y install iotop iftop yum-utils net-tools git lrzsz expect gcc gcc-c++ make cmake libxml2-devel openssl-devel curl curl-devel unzip sudo ntp libaio-devel wget vim ncurses-devel autoconf automake zlib-devel  python-devel bash-completion
if [[ $? -eq 0 ]] ; then
echo The command execute OK!
#sed -i "s/yum_init/#Invalid_yum_init/g" $bash_path/$scriptName
break;
else
if [[ num -gt 3 ]];then
echo "你登录 "$masterip" 瞅瞅咋回事？一直无法yum包"
break
fi
fi
done
}
#firewalld
iptables_config(){
if [[ `ps -ef | grep firewalld |wc -l` -gt 1 ]];then
  systemctl stop firewalld.service
  systemctl disable firewalld.service
fi
#  iptables -P FORWARD ACCEPT
}
#system config
system_config(){

if [[ `grep "SELINUX=disabled" /etc/selinux/config` ]];then
  echo "pass"
else
  sed -i "s/SELINUX=enforcing/SELINUX=disabled/g" /etc/selinux/config
  setenforce 0
fi

if [[ `ps -ef | grep chrony |wc -l` -eq 1 ]];then
  timedatectl set-local-rtc 1 && timedatectl set-timezone Asia/Shanghai
  yum -y install chrony && systemctl start chronyd.service && systemctl enable chronyd.service
  systemctl restart chronyd.service
fi
}


ulimit_config(){
if [[ `grep 'ulimit' /etc/rc.local` ]];then
echo "pass"
else
echo "ulimit -SHn 102400" >> /etc/rc.local
  cat >> /etc/security/limits.conf << EOF
  *           soft   nofile       102400
  *           hard   nofile       102400
  *           soft   nproc        102400
  *           hard   nproc        102400
  *           soft  memlock      unlimited 
  *           hard  memlock      unlimited
EOF
fi
}

ssh_config(){

if [[ `grep 'UserKnownHostsFile' /etc/ssh/ssh_config` ]];then
echo "pass"
else
sed -i "2i StrictHostKeyChecking no\nUserKnownHostsFile /dev/null" /etc/ssh/ssh_config
fi
}

get_localip(){
ipaddr=$(ip addr | awk '/^[0-9]+: / {}; /inet.*global/ {print gensub(/(.*)\/(.*)/, "\\1", "g", $2)}' | grep $ip_segment)
echo "$ipaddr"
}

change_hosts(){
cd $bash_path
num=0
for host in ${hostip[@]}
do
if [[ `grep "$host" /etc/hosts` ]];then

echo "hosts修改完毕！！！"
else
let num+=1

if [[ $host == `get_localip` ]];then
`hostnamectl set-hostname $hostname$num`
echo $host `hostname` >> /etc/hosts
else
echo $host $hostname$num >> /etc/hosts
fi

fi
done
}


rootssh_trust(){
cd $bash_path

if [[ `get_localip` != $masterip ]];then

if [[ ! -f /root/.ssh/id_rsa.pub ]];then
echo '###########init'
expect ssh_trust_init.exp $root_passwd $masterip
else
echo '###########add'
expect ssh_trust_add.exp $root_passwd $masterip
fi
echo $deployObjectPath
echo $deployName
scp -r $deployObjectPath/$deployName root@$masterip:/root

fi

}

main(){
 #yum_update
  #yum_config
  yum_init
  ssh_config
  iptables_config
  system_config
#  ulimit_config
  #change_hosts
  rootssh_trust
  echo "后台准备工作完成，坐稳了！！波哥带你飞！！！"
}
main

