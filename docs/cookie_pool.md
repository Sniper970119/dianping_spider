# Sniper

### 关于cookie以及cookie池的一些碎碎念

#### Cookie：

Cookie在配置文件中使用大写，主要是因为这样在浏览器中可以在cookie栏中直接右击然后复制，粘贴即可（至少firefox是这样）。

#### Cookie池：

原理是通过多个cookie，来降低程序（而不是cookie）被ban的几率（其实也确实可以通过随机cookie在一定程度上降低cookie被ban的几率）。

由于本人并没有多个账号（其实也是懒，也是自信），没有对cookie池部分代码进行测试。如有问题欢迎指出。

需要在cookies.txt中配置cookie，一行一个cookie，从浏览器中复制出来把“Cookie：”删掉就好了，会自动处理前后空白字符。

但是并不会检查文件格式，也就意味着如果没有按照标准格式来，程序可能会异常终止而没有相关提示。