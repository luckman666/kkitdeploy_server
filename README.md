**项目简介**：

项目主要使用docker的方式一键部署各类应用及工具。目前已经有7个大类，几十种工具实现一键部署。并且根据个人实际情况进行自定义部署。

kkitDeploy是波哥抽离了kkit3.0的一个功能模块开源给大家。


vue前端项目地址：
https://github.com/luckman666/kkitdeploy_dashboard

shellscript项目地址：
https://github.com/luckman666/kkitdeploy_script

python项目地址：
https://github.com/luckman666/kkitdeploy_server


该项目没借助传统的ansible、Saltstack或者clustershell来二次开发。ansible是kkit3.0和远程动作核心驱动，Saltstack在kkit1.0的核心驱动（kkit1.0已经被我开源至github）.

通过集成了上述两个工具后发现了不少缺点，所以在设计kkitDeploy的时候就自己写了个驱动来完成所有的动作。

**项目架构及开发语言（以后补图）：**

项目采用前后端分离设计，主要由VUE前端+django后台+shell脚本驱动三大块组成：
由于项目的特殊行，采用了redis作为该项目的核心存储。其中websocket为项目的核心数据传递方式。整体页面简洁，操作简单。

**项目使用手册：**

项目整体布局分两大块：

![image](https://upload-images.jianshu.io/upload_images/14069013-2726d15317587395?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

左边为菜单栏，右边为信息栏。

![image](https://upload-images.jianshu.io/upload_images/14069013-f3c03383ee624a61?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

菜单栏供我们选择要部署的类别，工具，及工具的版本和集群方式（以k8s为例）

![image](https://upload-images.jianshu.io/upload_images/14069013-4dde7d9a5cfef879?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

当我们选择完毕想要部署的项目后右侧信息栏会自动出现相应的配置参数。根据实际情况按照我所列举的格式进行配置后点击提交后台开始自动部署。并且将实时反馈后台执行日志（如下图）

![image](https://upload-images.jianshu.io/upload_images/14069013-35055a6531e200fa?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

部署进行时不可以刷新页面或者关闭页面。后台部署完毕会在右侧信息栏底部有相应的提示。

对于yml描述性文件部署的方式是另一种模式，例如我们部署nginx

![image](https://upload-images.jianshu.io/upload_images/14069013-aca0ebb145cad381?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

这一步修改的信息是我们要部署到哪里去。修改完信息后点击提交。

![image](https://upload-images.jianshu.io/upload_images/14069013-4f17996ee02c5db0?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

这一步是要我们修改yml文件，你要部署一个什么样的nginx。这个文件就是yml文件

而针对nginx的特殊性我们要配置各种后端的重定向业务，所以我们这里在部署nginx之前勾选配置再选择提交按钮：

![image](https://upload-images.jianshu.io/upload_images/14069013-12a63cbdab0bcf42?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

![image](https://upload-images.jianshu.io/upload_images/14069013-bce31e26bdb22123?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

可以上传不同的base.conf，而我们注意到上面nginx的yml配置参数里面的这一项

![image](https://upload-images.jianshu.io/upload_images/14069013-5127e723d04a4614?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

你所上传的所有配置文件都会上传至conf目录，所以在映射关系上必须要这么写，否则找不到。

也许有朋友觉得波哥预制的脚本不够丰富或者写的不够好，波哥也预留了自定义脚本的接口。之前的博文也交了大家如何利用波哥给大家的模板自定义功能插件了。自定义模板地址：

```
https://github.com/luckman666/deployYmlDemo.git
```

相关教程阅读该项目的README.md

让我们自定义完自己的插件过后点击上传  

![image](https://upload-images.jianshu.io/upload_images/14069013-d276faa826088be8?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

![image](https://upload-images.jianshu.io/upload_images/14069013-0e1b385c7b968ee8?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

将插件脚本文件夹rar压缩后，上传rar包。

![image](https://upload-images.jianshu.io/upload_images/14069013-51f43bf65733b441?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

![image](https://upload-images.jianshu.io/upload_images/14069013-ec11ce854e3d4305?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

点击确定后就可以在自定义选项卡中找到您上传的插件

![image](https://upload-images.jianshu.io/upload_images/14069013-253e8977eb3e0632?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

相关配置参数也自动上传到服务器

![image](https://upload-images.jianshu.io/upload_images/14069013-e4dfe48f324b17cc?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

然后的部署流程就和之前一样了。

PS：请自定义的插件名称不要使用原名称，例如nginx，redis。这样会覆盖我的原有脚本，而为了防止脚本出错更改不及时，波哥设计了每周都会同步云端的脚本script脚本，所以每次更新完毕之后都会覆盖回来。

请自定义脚本的同学加上个性化设计例如：myNginx等等。

那么如何部署我们的kkitdeploy呢？

```
git clone https://github.com/luckman666/kkitdeploy_install.git
cd kkitdeploy_install && chmod 755 -R .
# 修改base.config里面的参数
./kkitdeploy.sh
```

部署完毕访问服务器IP即可，默认是80端口，登录认证设计的是假认证，直接点击登录即可。

重启项目：

```

# 关闭
docker-compose -f *.yml down -v 
# 启动
docker-compose -f *.yml up -d
```

相关详细介绍和使用教程我会在后面陆续更新。该项目波哥长期维护。如果项目有问题，请在公众号留言。

项目的更新及任何问题都会在公众号统一发布及回复，公众号也会给该项目设计专题栏目。以后将很少发布独立脚本，各类实用工具及脚本会统一由kkitDeploy版本迭代后更新。

你们的支持就是波哥的动力，请帮忙转发和start哦！

* * *

扫码关注，回复“全栈资料”会有

意想不到的收获哦


![image](https://upload-images.jianshu.io/upload_images/14069013-9e9bed4ff95ffc41?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)



**长按识别二维码关注我们**




