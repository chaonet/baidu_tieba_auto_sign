## 百度贴吧自动签到

## 功能

只需在配置文件`conf.ini`中保存用户名和密码

- 网页版

模拟用网页批量签到

- 客户端版(获得更多经验)

可以自动获取`Cookie`和`BDUSS`，并模拟客户端进行批量签到。

## 起因

帮侄女签到

## 开发环境
```
Python 2.7.9
Mac os 10.10.5
```

windows 平台没有测试过，应该可以使用

## 环境配置
```
# 下载源码
git clone git@github.com:chaonet/baidu_tieba_auto_sign.git
# 或者通过 HTTPS 下载:
git clone https://github.com/chaonet/baidu_tieba_auto_sign.git

cd baidu_tieba_auto_sign

# 安装依赖
virtualenv env/
. ./env/bin/activate
pip install -r requirements.txt
```

## 使用

- 设置账号、密码

以便脚本运行时读取，用于登陆

在`baidu_tieba_auto_sign`目录中创建`conf.ini`文件，内容如下：

```
[main]
username=账号
password=密码
```

或者

在系统的环境变量中设置，方法略……

- 模拟`网页`进行百度贴吧批量签到

```
python sign.py
```

- 模拟`客户端`进行百度贴吧批量签到

```
python baidu-tieba-auto-sign.py
```

## 参考代码

参考并整合了[baidu-tieba-auto-sign](https://github.com/skyline75489/baidu-tieba-auto-sign)和[Tieba-autoSign](https://github.com/Hjyheart/Tieba-autoSign)

## 过程

最初找到的是[baidu-tieba-auto-sign](https://github.com/skyline75489/baidu-tieba-auto-sign)，但要自己获取`Cookie`和`BDUSS`，门槛有点高，于是找到了[Tieba-autoSign](https://github.com/Hjyheart/Tieba-autoSign)，可以顺利签到。

但是发现了一个问题，这是模拟网页签到，而手机客户端签到经验很多啊！禁不住诱惑，开始琢磨。[baidu-tieba-auto-sign](https://github.com/skyline75489/baidu-tieba-auto-sign)是可以模拟客户端的，关键是用脚本实现`Cookie`和`BDUSS`的获取，经过一番搜索，依然一头雾水。

无意中打印[Tieba-autoSign](https://github.com/Hjyheart/Tieba-autoSign)登陆后的`cookie`，惊喜发现里面就有`Cookie`和`BDUSS`。

于是，截取[Tieba-autoSign](https://github.com/Hjyheart/Tieba-autoSign)从开始到登陆成功的代码，将函数修改为返回`Cookie`和`BDUSS`。

[baidu-tieba-auto-sign](https://github.com/skyline75489/baidu-tieba-auto-sign)调用并获取返回的`Cookie`和`BDUSS`作为输入函数，并适当修改 HTTP 头部，测试，成功。

最终，实现只需在配置文件`conf.ini`中保存用户名和密码，可以自动获取`Cookie`和`BDUSS`，并模拟客户端进行批量签到。
