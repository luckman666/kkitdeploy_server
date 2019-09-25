FROM centos:7

MAINTAINER b8_yang@163.com

# 设置编码
ENV LANG en_US.UTF-8

# 同步时间
ENV TZ=Asia/Shanghai
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# 1. 安装基本依赖
RUN yum update -y && yum -y groupinstall "Development tools" && yum install epel-release -y && yum install wget unzip epel-release nginx xz gcc automake zlib-devel openssl-devel net-tools groupinstall development  libxslt-devel libxml2-devel libcurl-devel git iotop iftop yum-utils supervisor net-tools rsync lrzsz expect gcc-c++ make cmake libxml2-devel openssl-devel curl curl-devel libaio-devel ncurses-devel autoconf zlib-devel  python-devel bash-completion zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel readline-devel tk-devel gdbm-devel db4-devel libpcap-devel xz-devel -y && wget https://www.python.org/ftp/python/3.6.7/Python-3.6.7.tar.xz && xz -d Python-3.6.7.tar.xz && tar xvf Python-3.6.7.tar && cd Python-3.6.7 && ./configure && make && make install && rm -rf Python-3.6.7.tar.xz && rm -rf Python-3.6.7 && pip3 install --upgrade pip

#3 部署应用
ADD . /opt
RUN pip3 install -r /opt/kkitDeploy/requirements.txt && rm -rf /opt/kkitDeploy/requirements.txt && cd /opt/rar && make && rm -rf /opt/rar && rm -rf /etc/nginx/nginx.conf && cp /opt/docs/nginx.conf /etc/nginx/nginx.conf && rm -rf /etc/supervisord.conf && cp /opt/docs/supervisorDeploy.conf /etc/supervisord.conf && rm -rf /opt/docs/ && rm -rf /opt/Dockerfile

#4 设置容器
VOLUME /var/log/
VOLUME /opt/kkitDeploy/apps/utils/api/
WORKDIR /opt/kkitDeploy
EXPOSE 80 8002

CMD ["/usr/bin/supervisord"]



