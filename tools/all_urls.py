
# 先开启main运行起来，这个再运行，这个是来增量爬取的这个网站的首页的
import redis
import json

rd = redis.Redis("127.0.0.1", decode_responses=True)

rd.lpush('cnblogs:start_urls', "https://news.cnblogs.com/")


# 数字越大，优先级越高, parse_detail是把这个拿到parse_detail里解析
urls = [("https://news.cnblogs.com/n/656059/", 3, "parse_detail"),
        ("https://news.cnblogs.com/n/656059/", 5, "parse_detail"),
        ("https://news.cnblogs.com/n/656059/", 8, "parse_detail"),
        ("https://news.cnblogs.com/n/656059/", 20, "parse_detail"),

        ]


for url in urls:
    # lpush像一个栈。。。。rpush就像一个队列，可以先进先出,比如左边放数据，右边取数据
    rd.rpush("cnblogs:new_urls", json.dumps(url))












