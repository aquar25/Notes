# Xmind源码编译

1. 下载源码 http://sourceforge.net/projects/xmind3/
2. 下载eclipse indigo for RCP and RAP developers
3. 安装jdk1.7 
4. 拷贝xmind安装目录下plugin目录中源码编译依赖的三个库文件:net.sourceforge.jazzy_0.5.0.jar, org.bouncycastle_1.3.8.jar(or org.bouncycastle_1.4.7.jar), org.json_1.0.0.jar到eclipse的plugin目录下，如果不行就拷贝到dropin目录下
5. 安装gef draw2D [http://www.eclipse.org/gef/downloads/index.php](http://www.eclipse.org/gef/downloads/index.php) 下载draw2D的安装包，解压放到eclipse对应的features和plugin目录
6. 在eclipse的中导入源码根目录的所有工程
7. 修改工程org.xmind.ui.menus的manifes.mf文件中org.eclipse.core.expressions;bundle-version="3.4.400"，从indigo的plugin目录可以找到org.eclipse.core.expressions包的版本为3.4.3，因此要改东这个版本号为3.4.300
8. org.xmind.cathy工程的build path中增加对工程org.xmind.core.io的依赖，否则会提示无法解析的mindmanager的常量定义类
9. 工程中还有一处常量定义找不到的错误，只需要在类似的字符串定义文件中找到一个替换出错的label的名字即可
10. 在运行--运行配置--右键选择eclipse application--New--随便起一个名字，在run a product:中选择org.xmind.cathy.product。可以在Plug-ins标签页下，选择lanuch with:plug-ins selected below only,然后在下方勾选需要的插件，这一点可以保留默认的all workspace and enabled target plug-ins即可。
11. 运行起来的xmind和正式产品相比菜单少了不少内容 一 一+


## Notes

1. Xmind基于eclipse开发，使用了eclipse的插件开发模式，eclipse在3.x和4.x之间有差异，因此不能用最新的luna进行编译
2. eclipse indigo不支持jdk8，而通过查看xmind安装目录下的jre的版本可以知道xmind使用的是jdk7
3. net.xmind.verify_3.5.0.201410310637.jar中LicenseVirify类提供了License验证的方法，可以通过jd-gui来查看源码，从soureforge中下载的源码是没有相关源代码的，包括一些其他的功能也没有，只适合学习基于eclipse的应用程序开发。
4. 在xmind的google code 官网上有编译说明，其中提到

> Select org.xmind.cathy.win32, Select File menu -> Properties -> Java Build Path -> Libraries, Remove org.eclipse.swt.win32.win32.x86_3.4.1.v3449c.jar

但是没有这样操作，也可以正常编译。


