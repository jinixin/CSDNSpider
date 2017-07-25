# CSDNSpider
Crawling the read number of every blog in CSDN everyday.


## 目的  
* 每天自动记录某用户的每篇CSDN博客访问量

* 提供博客备份功能，把博客的文字信息备份到数据库

* 博客数据可视化
    * 最近十天博客的日访问量
    * 博客每篇文章最近十天的访问增量
    * 当前博客每篇文章的访问量

* 通过网络随时随地获取博客的访问情况
    * 比如：http://blog.csdn.net/jinixin/article/details/75193997

## 安装
* 通过<code>pip install -r requirements</code>安装所需包

* <code>export CSDN_URL=某用户CSDN博客地址</code>（如：http://blog.csdn.net/jinixin ）  
<code>export DB_USER=数据库用户</code>  
<code>export DB_PWD=数据库密码</code>  
通过上面三条语句分别将待爬取地址，数据库信息写入环境；或者在脚本中直接替换，通过命令行参数将待爬取地址传入

* 创建“blog_csdn”数据库后，向MySQL导入“blog_csdn.sql”文件


## 运行
#### 记录访问量
* 通过<code>crontab -e</code>设置Linux定时任务  
<code>1 0 * * * nohup /绝对路径/crawler/blogPageViews.py 2>>/绝对路径/blogPageViews.log &</code>  
(这样该脚本会在每天的00:01自动运行，注意修改具体路径)

* 若不设置定时任务，也可每天在命令行键入“./blogPageViews.py”

#### 备份博客
* 这个不需要每天都运行，需要时命令行键入“./blogBackup.py”即可

#### 可视化数据
* 通过<code>crontab -e</code>设置Linux定时任务  
<code>5 0 * * * nohup /绝对路径/analyse/blogImages.py 2>>/绝对路径/blogImages.log &</code>  
(这样该脚本会在每天的00:05自动运行，注意修改具体路径)

* 若不设置定时任务，也可每天在命令行键入“./blogImages.py”

* Mac用户运行时若报错，请参考该[链接](https://stackoverflow.com/questions/21784641/installation-issue-with-matplotlib-python)；图片中文乱码，请参考该[链接](https://www.zhihu.com/question/25404709)  

* 效果图  

![最近十天博客的日访问量](http://i4.buimg.com/596409/a3b23dcec3ecb4e9.png)
![博客每篇文章最近十天的访问增量 ](http://i4.buimg.com/596409/f5c8fc3682dba249.png)

#### 运行服务器
* 命令行键入“./server.py”即可，默认端口是5000  

* 随时随地通过网络访问”http://服务器IP地址:端口/picture/图片名”  获取图片；三张图片名称分别为：article_view_num，everyday_view_num，ten_day_add_num


## 技术
* Python语言，Flask框架  

* MySQL提供数据存储  

* Requests模块获取网页，BeautifulSoup与re模块提取目标元素  

* Matplotlib用于绘图，数据可视化

## 未来
* 博客中的图片没能备份，以后图片也要备份

* 继续丰富图表类型

* 提供部署脚本，实现快速部署

#### 如有好点子，可通过jinixin#qq.com告诉我，或直接加入该项目，谢谢 ：）


