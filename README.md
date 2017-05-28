# CSDNSpider
Crawling the read number of every blog in CSDN everyday.


## 目的  
* 每天自动记录某位用户的每篇CSDN博客访问量

* 提供博客备份功能，把博客的文字信息备份到数据库


## 使用
* 通过<code>pip install -r requirements</code>安装所需包

* <code>export CSDN_URL=某用户CSDN博客地址</code>（如：http://blog.csdn.net/jinixin ）  
<code>export DB_USER=数据库用户</code>  
<code>export DB_PWD=数据库密码</code>  
用上面三条语句分别将待爬取地址，数据库信息写入Linux环境变量。 
（也可以在blogPageViews.py中直接替换，或通过命令行参数将待爬取地址传入）

* 创建“blog_csdn”数据库后，向MySQL导入“blog_csdn.sql”文件


## 运行
#### 记录访问量
* 通过<code>crontab -e</code>设置Linux定时任务  
<code>1 0 * * * nohup /root/blogPageViews.py 2>>/root/blogPageViews.log &</code>  
(这样该脚本会在每天的00:01自动运行，注意修改具体路径)

* 若不设置定时任务，也可每天在命令行键入“./blogPageViews.py”

#### 备份博客
* 这个不需要每天都运行，需要时命令行键入“./blogBackup.py”即可

## 未来
* 博客中的图片没能备份，以后图片也要备份。

* 通过图表的形式将数据表现出来，能看到每天每篇博客的访问增长情况，并做一定的分析。

（如有好的点子，可以通过<jinixin@qq.com>告诉我，或者直接加入进来，谢谢）


