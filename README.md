# ChaoXing Health Sign
超星学习通健康打卡上报

Ver.21.10.02:02

项目地址：<https://github.com/panghaibin/cx_health_sign>

## 特色
 - 支持多用户使用

 - 支持默认表单模板或学校自定义模板

 - 支持多种消息推送渠道，可将打卡上报结果推送给自己

 - 支持将所有打卡结果推送给指定的一人

## 开始使用
### 在 GitHub Actions 上使用

1. `Star`并`Fork`本项目

2. 前往 `Settings`-`Secrets` ， 点击 `New repository secret`

3. 在新建 Secret 的界面上， `Name` 值输入 `USERS` ， `Value` 处输入用户的配置信息，多个用户配置之间使用`英文分号`隔开。
   
   单个用户的配置信息格式如下（[ ]内为可选参数）：
   ```
   username,password,post_type[,school_id,api_type,api_key]
   ```
   
   `username`, `password` 分别是学号和密码
   
   `post_type`是本程序目前支持填报的表单代码，详情见[支持的学校表单](#支持的学校表单)中的[表单代码]一栏
   
   `school_id`是学校代号，获取方法见[学校id获取](#学校id获取)
   
   `api_type`, `api_key`是消息推送类型代号及密钥，详情见[消息推送介绍](#消息推送介绍)
   
   示例如下：
   
   用户需要消息推送服务，并且使用学号登录：
   ```
   20192233,12345Abc,default,209,2,5e58d2264821c69ebcd46c448e7f5fe6
   ```
   
   若用户不使用学号登录，或者不需要使用消息推送服务，则**按照上述格式的顺序**，仅保留需要的参数即可

   例如用户使用手机号而不是学号登录，需要消息推送服务：
   
   ```
   13878000000,5678Zyx,default,2,46d002ca1ed0c82e1c251a9e5893cd62
   ```
   
   使用手机号登录，仅需要基础功能：

   ```
   18866000000,8899Qwe,nnnu
   ```
   
   要注意不能以`,`作为末尾

   多用户时，每个用户的配置信息用英文分号`;`间隔：

   ```
   20192233,12345Abc,default,209,2,5e58d2264821c69ebcd46c448e7f5fe6;13878000000,5678Zyx,default,2,46d002ca1ed0c82e1c251a9e5893cd62;18866000000,8899Qwe,nnnu
   ```

   同样注意末尾不需要有分号`;`  

   完成后点击`Add secret`保存该 Secret
   
4. （可选）用同样的方法添加一个名为 `SEND` 的 Secret ，用于将所有用户的填报结果推送给管理员。

   格式为`api_type,api_key`，例如

   ```
   2,5e58d2264821c69ebcd46c448e7f5fe6
   ```

5. Secret 添加完成后，前往项目的 `Actions` 面板，同意开启并进入 Actions 。然后选择 `Health Report` ，点击 `Enable workflow` 开启工作流。此时 Actions 开启成功，可以点击 `Run workflow` 测试填报一次。

6. 当本项目更新时，你所 Fork 的项目不会自动更新。在你的项目主页上点击 `Fetch upstream`-`Fetch and merge`以更新程序。

### 在自己的服务器上使用

1. 克隆本项目，进入项目文件夹
   ```shell
   git clone https://github.com/panghaibin/cx_health_sign
   cd cx_health_sign
   ```

2. 添加用户
   ```shell
   python3 main.py add
   ```

   部分参数选填，根据提示执行添加用户操作

   获取学校id的方法见[学校id获取](#学校id获取)
   
   要使用消息推送服务，你需要提前注册第三方的消息推送服务以获取密钥，见[消息推送介绍](#消息推送介绍)

3. （可选）设置全局推送

   ```shell
   python3 main.py send
   ```
   
   根据提示操作，设置后所有用户的填报结果都会推送到对应接口


   以上两步也可通过直接创建 `setting.yaml` 文件以保存配置，格式参考 `setting.bak.yal` 。

4. 执行程序
   ```shell
   python3 main.py
   ```
   
   这将会立即填报一次，确保可以正确填报


5. 设置定时填报
   ```shell
   vim /etc/crontab
   ```
   
   向其中添加
   ```
   0 7,12,19 * * * root /usr/bin/python3 /root/cx_health_sign/main.py >> /root/cx_health_sign/output.log
   ```
   请根据实际情况作出修改
   
   保存文件后执行
   ```shell
   crontab /etc/crontab
   ```
   以应用 crontab 配置

## 支持的学校表单
| 表单代码 | 名称 | 备注 |
| :---: | :---: | :---: |
| test  | 测试用表单 | 一个不限时间和次数的填报表单，[表单主页](http://office.chaoxing.com/front/web/apps/forms/fore/apply?id=13243&enc=3a9416c86432c5f667f2b23a88a0123a)
| default | 学习通默认健康打卡表单 | 绝大部分学校所用，[表单主页](http://office.chaoxing.com/front/web/apps/forms/fore/apply?id=7185&enc=f837c93e0de9d9ad82db707b2c27241e)
| nnnu | 南宁师范大学三检 | [早检表单](http://office.chaoxing.com/front/web/apps/forms/fore/apply?id=99778&enc=5affca1a747445b8d3ec9de92612ecae) [午检表单](http://office.chaoxing.com/front/web/apps/forms/fore/apply?id=99781&enc=e4041a9c358a738a1dd8780e8dfeccb6) [晚检表单](http://office.chaoxing.com/front/web/apps/forms/fore/apply?id=99783&enc=cb9894ce56b7e222cb3eab72d0fed834)

如果你的学校未使用默认健康打卡表单，而使用自定义打卡表，但不在本项目支持列表之内，你可以：
 - 自己抓包学习通的表单链接得到 `form_id` 和 `enc` ，在本项目的 `config` 文件夹下新建一个 Python 文件，新建一个继承自 `config._Report` 的类，参考 `test.py` 下或其它文件的适配方法，根据实际情况，对你的学校进行适配。测试通过后即可向本项目 `Pull request` 。
 - 提 Issue 请求适配

## 消息推送介绍
目前支持以下消息推送服务：

| 接口代号 | 名称| 官网 |
| :---: | :---: | :---: |
| 1 | Server酱 | https://sct.ftqq.com/ |
| 2 | 推送加 | https://www.pushplus.plus/ |
| 3 | 推送加（hxtrip域名下） | https://pushplus.hxtrip.com/ |

请前往任意官网注册得到`key`后即可在本项目中使用，在 GitHub Actions 中使用时注意接口代号正确设置。

## 学校id获取
1. 访问 http://passport2.chaoxing.com/login

2. 按下面动图操作
   	
   ![2020/04/15/cdf5a0415014614.gif](http://cdn.z2blog.com/2020/04/15/cdf5a0415014614.gif)
   
   [图片来源](https://github.com/mkdir700/chaoxing_auto_sign/blob/latest/api/readme.md)
   
## Thanks
本项目受到了[mkdir700/chaoxing_auto_sign](https://github.com/mkdir700/chaoxing_auto_sign) 的启发，特此表示感谢！
