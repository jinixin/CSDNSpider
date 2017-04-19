/* 返回每一天的博客总访问量 */
select record_time, sum(read_number) as read_number
from read_number
group by record_time
order by record_time desc;

/* 以每篇博客的阅读数排序所有博客 */
select title, read_number
from id_title
inner join read_number on id_title.id = read_number.id
where record_time = curdate()
order by read_number desc;