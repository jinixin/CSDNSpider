# CSDNSpider
Crawling the read number of every blog in CSDN everyday.

***

## 中文说明
### 目的
想通过这款工具，每天自动记录某位用户的每篇CSDN博客访问量，并存入数据库。后期希望可以通过图表的形式将数据表现出来，让人们能看到每天每篇博客的访问增长情况，并做一定的分析。
### 使用
* 通过<code>pip install -r requirements</code>安装所需包

* <code>export CSDN_URL=某用户CSDN博客地址</code>
<code>export DB_USER=数据库用户</code>
<code>export DB_PWD=数据库密码</code>
用上面三条语句分别将爬取地址，数据库信息写入Linux环境变量
（你也可以在getBlogCSDN.py中直接替换）

* 通过<code>crontab -e</code>设置Linux定时任务
<code>1 0 * * * nohup /root/getBlogCSDN.py > /root/getBlogCSDN.log &</code>
(这样该脚本会在每天的00:01自动运行，注意修改具体路径)