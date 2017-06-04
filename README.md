# CSDNSpider
Crawling the read number of every blog in CSDN everyday.


## 目的  
* 每天自动记录某位用户的每篇CSDN博客访问量

* 提供博客备份功能，把博客的文字信息备份到数据库

* 博客数据可视化
    * 最近十天博客的日访问量
    * 博客每篇文章最近十天的访问增量 
    * 当前博客每篇文章访问量


## 使用
* 通过<code>pip install -r requirements</code>安装所需包

* <code>export CSDN_URL=某用户CSDN博客地址</code>（如：http://blog.csdn.net/jinixin ）  
<code>export DB_USER=数据库用户</code>  
<code>export DB_PWD=数据库密码</code>  
用上面三条语句分别将待爬取地址，数据库信息写入Linux环境变量（也可在blogPageViews.py中直接替换，或通过命令行参数将待爬取地址传入）。

* 创建“blog_csdn”数据库后，向MySQL导入“blog_csdn.sql”文件


## 运行
#### 记录访问量
* 通过<code>crontab -e</code>设置Linux定时任务  
<code>1 0 * * * nohup /root/blogPageViews.py 2>>/root/blogPageViews.log &</code>  
(这样该脚本会在每天的00:01自动运行，注意修改具体路径)

* 若不设置定时任务，也可每天在命令行键入“./blogPageViews.py”

#### 备份博客
* 这个不需要每天都运行，需要时命令行键入“./blogBackup.py”即可

#### 可视化数据
* 需要时命令行键入“./blogImages.py”即可；Mac用户运行时若报错，请参考该[链接](https://stackoverflow.com/questions/21784641/installation-issue-with-matplotlib-python)
* 效果图  

![最近十天博客的日访问量](http://i4.buimg.com/596409/a3b23dcec3ecb4e9.png)
![博客每篇文章最近十天的访问增量 ](http://i4.buimg.com/596409/f5c8fc3682dba249.png)

## 未来
* 博客中的图片没能备份，以后图片也要备份。

* 继续丰富图表类型；加入服务器，将数据直接显示到用户的博客上。

#### 如有好点子，可通过<jinixin@qq.com>告诉我，或直接加入该项目，谢谢


