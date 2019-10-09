3 - python scripts of read-helper and automated tests

## Reader Plus

### Intro

It contains a bunch of  actions for assistant robots. And it can be kind of plus service for readers.

Lots of simple and repeated actions should be taken to read, like or share articles.  Why should human do such tiring work? There must be some new way leading to better user experience. But I am not the smart one. So I just do it in my way. This is the reason why this project came out and lasted for a not clear time. Hope new ideas and solutions come as soon as possible. Enjoy reading, not clicking and dragging.

Since this project is built under the [LICENSE](./LICENSE) of GPL 3.0 so you can share it under it. If any issue, let me know. Thanks.

### Start

运行脚本即可。以下举例说明。

为了提高代码地毯式比对的效率，需要在项目目录中的主文件夹目录下新建一个`data`文件夹，并在里面放入`user_list.txt`文件：一行一个地址，用来存放可忽略/已关注。

然后，找到该主文件文件夹目录下的`auto_test.py`文件，并对其中的“账号”和“密码”进行自定义，直接运行之，即可。另外还可以对其他相关的参数进行修改、测试。

```
python .\game1night\3\jianshu\auto_test.py

pause
```



### Rebuild

1. 范围，目标：登陆，操作；辅助阅读，互动评价。
2. 阅读文章。
3. 选文章。
4. 处理用户事件。
5. 处理文章事件。



