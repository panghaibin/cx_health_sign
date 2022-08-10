![cx_health_sign](https://socialify.git.ci/panghaibin/cx_health_sign/image?description=1&forks=1&issues=1&language=1&stargazers=1)

**_注意：本项目对打卡的内容并不关心且一无所知，程序的原理仅仅是获取上一次的表单数据，再将其自动填写。程序不对使用本程序的用户负责，请自行保证表单的正确性与完整性。使用时请自觉遵守相应的约束性条款。_**

项目地址：<https://github.com/panghaibin/cx_health_sign>

最近更新日志：

[2.3.9] - 2022-08-10

适配 武汉生物工程学院 健康打卡

适配 武昌理工学院 健康打卡

适配 咸宁职业技术学院 健康打卡-2

......

[查看全部更新日志](CHANGELOG.md)

## 特色
- 支持在 GitHub Actions 上使用，以及自建服务器、PC等上使用

- 支持为多用户填报，单用户可填报多个表单，适配学校多个表单的情况

- 可支持学校各类自定义打卡表单

- 支持自助适配学校的表单模板（详见 [学习通健康打卡表单自适配指北](https://hbte.ch/1968.html) ）

- 支持[多种消息推送渠道](#消息推送介绍)，可将打卡上报结果推送给自己

- 支持将所有打卡结果推送给指定的一人

## 支持的学校表单
| 表单代码 | 名称 | 备注 |
| :---: | :---: | :---: |
| test  | 测试用表单，不限填报时间和次数 | [表单主页](http://office.chaoxing.com/front/web/apps/forms/fore/apply?id=13243&enc=3a9416c86432c5f667f2b23a88a0123a)
| default | 默认健康打卡表单 | [表单主页](http://office.chaoxing.com/front/web/apps/forms/fore/apply?id=7185&enc=f837c93e0de9d9ad82db707b2c27241e)
| nnnu | 南宁师范大学 两检 | [早检表单](http://office.chaoxing.com/front/web/apps/forms/fore/apply?id=99778&enc=5affca1a747445b8d3ec9de92612ecae) [午检表单](http://office.chaoxing.com/front/web/apps/forms/fore/apply?id=99783&enc=cb9894ce56b7e222cb3eab72d0fed834)
| hnucc | 湖南城建职业技术学院 学生健康信息填报 | [表单主页](https://office.chaoxing.com/front/third/apps/forms/fore/apply?id=86243&enc=de7939f413267efd9a0fd882dca9140b) |
| swut | 山东外国语职业技术大学 健康打卡 | [表单主页](https://office.chaoxing.com/front/web/apps/forms/fore/apply?id=139669&enc=d3fd2b1818f116a76aff41eee80ea348) |
| swut_2 | 山东外国语职业技术大学 午检打卡 | [表单主页](https://office.chaoxing.com/front/web/apps/forms/fore/apply?id=175235&enc=fb50b811a71a357bbb3a87424f7c074c) |
| hnisc | 湖南信息学院 健康打卡 | [表单主页](https://office.chaoxing.com/front/web/apps/forms/fore/apply?id=158324&enc=b08ae0de35d833ebc04ad7c5604f1b43) |
| xnec | 咸宁职业技术学院 健康打卡 | [表单主页](https://office.chaoxing.com/front/web/apps/forms/fore/apply?id=100992&enc=bd1883314d3b5f4b36c91dc1907b5c74) |
| xnec_2 | 咸宁职业技术学院 健康打卡-2 | [表单主页](https://office.chaoxing.com/front/web/apps/forms/fore/apply?id=100244&enc=c30d59556090a358fc0fb4992dd65cc1) |
| qcuwh | 武汉晴川学院 健康打卡 | [表单主页](http://office.chaoxing.com/front/web/apps/forms/fore/apply?id=7185&enc=f837c93e0de9d9ad82db707b2c27241e) |
| hebart | 河北艺术职业学院 健康打卡 | [表单主页](http://office.chaoxing.com/front/web/apps/forms/fore/apply?id=886&enc=c8f7d4f5599544933f7c222b6b44e5c4) |
| cwxu | 南京信息工程大学滨江学院（无锡学院） 健康打卡 | [表单主页](http://office.chaoxing.com/front/web/apps/forms/fore/apply?id=3449&enc=627c625902a1fd27de56172186a3f903) |
| qvtu | 泉州职业技术大学 健康打卡 | [表单主页](http://office.chaoxing.com/front/web/apps/forms/fore/apply?id=200487&enc=b69dd988598ff61b4366fdb1f1962114) |
| hebau | 河北农业大学 健康上报 | [表单主页](http://office.chaoxing.com/front/web/apps/forms/fore/apply?id=204160&enc=a9b79f8b76307cd50a458b843d219ff2) |
| tust | 天津科技大学 本科健康打卡 | [表单主页](http://office.chaoxing.com/front/web/apps/forms/fore/apply?id=14673&enc=ed9e03b2050df7f56003dc0c0fa226d2) |
| wut | 武昌理工学院 本科健康打卡 | [表单主页](http://office.chaoxing.com/front/web/apps/forms/fore/apply?id=89398&enc=75244f75384287c902e57b080c4d1c6d) |
| whsw | 武汉生物工程学院 健康打卡 | [表单主页](http://office.chaoxing.com/front/web/apps/forms/fore/apply?id=174267&enc=2ea539d84f23c7852a021ed77008df9f) |

如果你的学校不在本项目支持列表之内，你可以：
- 自己抓包学习通的表单链接得到 `form id` 和 `enc` ，然后即可自助适配，详细步骤见 [学习通健康打卡表单自适配指北](https://hbte.ch/1968.html) 。适配好并测试通过后，即可向本项目 `Pull Request` 。
- 或者，直接提 Issue 请求适配

本项目支持使用 GitHub Actions 或在自建服务器上使用（阿里云等部分国内云服务IP可能被超星屏蔽，无法使用），通过使用 `crontab` 来定时开启。考虑到不同学校的打卡时间不一样，若使用 GitHub Actions 运行的，建议修改 `.github/workflows/report.yml` 内的定时时间（时区为**UTC时区**）；使用自建服务器的也一样，若为海外服务器也请注意服务器所使用的时区。

## 开始使用
### 方法一  在 GitHub Actions 上使用

1. `Star`并`Fork`本项目

2. 前往 `Settings`-`Secrets`-`Actions` ， 点击 `New repository secret`

3. 在新建 Secret 的界面上， `Name` 值输入 `NEWUSERS` ， `Value` 处输入用户的配置信息，多个用户配置之间使用分号隔开。

    > 在旧版本（1.4.0及以前）中采用的`Name`值为`USERS`，格式也难以阅读。现在的版本`Name`为`NEWUSERS`，并采用如下的便于阅读的设置方案，旧的方案仍然兼容。

    单个用户的配置信息分别由几对`key=value`组成，格式如下（[ ]内为可选参数）：
    ```
    un=username,pd=password,pt=post_type[,si=school_id,at=api_type,ak=api_key]
    ```

    `username`, `password` 分别是用户名（学号或手机号）和密码

    `post_type`是本程序目前支持填报的表单代码，详情见[支持的学校表单](#支持的学校表单)中的[表单代码]一栏。如果需要同时填报多个表单，请使用`|`符号连接不同的表单。如 `swut|swut_2`

    `school_id`是学校代号（仅在学号登录时需要），获取方法见[学校id获取](#学校id获取)

    `api_type`, `api_key`是消息推送类型代号及密钥（可选），详情见[消息推送介绍](#消息推送介绍)

    示例如下：

    使用手机号登录，表单代码为`nnnu`，不需要消息推送，仅需要基础填报功能：

    ```
    un=138xxxx,pw=123xxx,pt=nnnu
    ```

    使用手机号登录，需要同时使用表单代码`swut`和`swut_2`，需要消息推送服务：
    ```
    un=139xxxx,pw=567yyy,pt=swut|swut_2,at=2,ak=xxxx
    ```

    使用学号登录（查询得到学校代码为`209`），表单代码为`default`，需要消息推送服务：

    ```
    un=2019xxxx,pw=789zzz,pt=default,si=209,at=2,ak=xxxx
    ```

    以上几个`key=value`对的顺序可以交换，要注意末尾不能是`,`

    为多个用户设置时，每个用户的配置信息之间，用分号间隔。例如上面三个例子合在一起时：

    ```
    un=138xxxx,pw=123xxx,pt=nnnu;un=139xxxx,pw=567yyy,pt=swut|swut_2,at=2,ak=xxxx;un=2019xxxx,pw=789zzz,pt=default,si=209,at=2,ak=xxxx
    ```

    同样注意末尾不需要有分号`;`

    完成后点击`Add secret`保存该 Secret

4. （可选）用同样的方法添加一个名为 `NEWSEND` 的 Secret ，用于将所有用户的填报结果推送给管理员。

    > 在旧版本（1.4.0及以前）中采用的`Name`值为`SEND`，格式也难以阅读。现在的版本`Name`为`NEWSEND`，并采用如下的便于阅读的设置方案，旧的方案仍然兼容。

    格式为`ai=api_type,ak=api_key`，例如

    ```
    at=2,ak=xxxx
    ```

5. （可选）添加一个名为 `LOGPASS` 的 Secret ，用于将 GitHub Actions 的执行结果日志加密

    设置该 Secret 后会将日志文件用 7z 加密压缩并上传，可在每个 Action 页面的 Artifacts 处下载，使用任意解压软件解压即可查看。

    若不设置该 Secret 则日志直接输出在 Actions 的执行结果页

6. （可选）添加一个名为 `SLEEPTIME` 的 Secret ，以在填报时控制休眠时间

    设置值为 `random` ，每次会随机休眠 30 ~ 360 秒，若不设置默认休眠 5 秒。

7. Secret 添加完成后，前往项目的 `Actions` 面板，同意开启并进入 Actions 。然后选择 `Health Report` ，点击 `Enable workflow` 开启工作流。此时 Actions 开启成功，可以点击 `Run workflow` 测试填报一次。

8. 当本项目更新时，你所 Fork 的项目不会自动更新。可以选择安装 GitHub Apps 中的 [Pull App](https://github.com/apps/pull) ，保持你的 Fork 始终最新。安装时默认会应用到所有项目，建议手动选择需要应用的项目。注意该 App 会强制覆盖你对 Fork 项目的操作，如果你有改动（例如修改了 `.github/workflows/report.yml` ），请注意备份。

    若不安装，需要手动更新时，在你的项目主页上点击 `Fetch upstream`-`Fetch and merge` 即可更新程序。

### 方法二  在自己的服务器上使用

1. 克隆本项目，进入项目文件夹
    ```shell
    git clone https://github.com/panghaibin/cx_health_sign
    cd cx_health_sign
    # 安装依赖
    pip3 install -r requirements.txt
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


以上两步也可通过直接创建 `setting.yaml` 文件以保存配置，格式参考 `setting.bak.yaml` 。

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
    此仅为示意，请根据实际情况作出修改，例如将时间设置正确，脚本的路径正确

    程序在填报时每次填报默认休眠 5s，如果需要自定义休眠时间，如每次休眠 30s：

    ```
    0 7,12,19 * * * root export sleep_time=30 && /usr/bin/python3 /root/cx_health_sign/main.py >> /root/cx_health_sign/output.log
    ```
   
    另外还支持随机休眠30~360s，设置为 `sleep_time=random` 即可

    保存文件后执行
    ```shell
    crontab /etc/crontab
    ```
    以应用 crontab 配置

## 消息推送介绍
目前支持以下消息推送服务：

| 接口代号 | 名称| 官网 |
| :---: | :---: | :---: |
| 1 | Server酱 | https://sct.ftqq.com/ |
| 2 | 推送加 | https://www.pushplus.plus/ |
| 3 | ~~推送加（hxtrip域名下）~~ | ~~https://pushplus.hxtrip.com/~~ 该服务已下线 |

请前往任意官网注册得到`key`后即可在本项目中使用，在 GitHub Actions 中使用时注意接口代号正确设置。

## 学校id获取
1. 访问 http://passport2.chaoxing.com/login

2. 按下面动图操作

    ![2020/04/15/cdf5a0415014614.gif](http://cdn.z2blog.com/2020/04/15/cdf5a0415014614.gif)

    [图片来源](https://github.com/mkdir700/chaoxing_auto_sign/blob/latest/api/readme.md)

## Thanks
本项目受到了[mkdir700/chaoxing_auto_sign](https://github.com/mkdir700/chaoxing_auto_sign) 的启发，特此表示感谢！
