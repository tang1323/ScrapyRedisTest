
from scrapy.http import Request
from urllib import parse

# 分布式爬虫的步骤
# -----1导入分布式爬虫类
from scrapy_redis.spiders import RedisSpider


# -----2 继承分布式爬虫类
class CnblogsSpider(RedisSpider):
    name = 'cnblogs'
    # -----3注销：start_urls和allowed_domains
    # # 允许修改的域
    # allowed_domains = ["https://www.cnblogs.com/"]

    # 这个在redis中的lpush得是一样的，不然它会使用默认
    # lpush cnblogs:start_urls https://news.cnblogs.com/

    # ----4 设置redis-key,这个key 随意设置，但是所有爬虫都要从这个key找起始url，也是往里放数据，也从里面取
    # 在redis中输入lpush cnblogs:start_urls https://book.jd.com/booksort.html
    redis_key = 'cnblogs:start_urls'

    # ----5 设置__init__
    def __init__(self, *args, **kwargs):
        # 在初始化的时候是获取domain参数，如果没有则为空字符串。
        domain = kwargs.pop('domain', '')

        # 我们在domain是可能有多个允许的域，所以用domain.split(',')， 用逗号隔开
        # ['www.jd.com', 'list.jd.com', 'p.3.cn']就是这样的域
        # filter要转换成一个列表
        self.allowed_domains = list(filter(None, domain.split(',')))
        super(CnblogsSpider, self).__init__(*args, **kwargs)


    # def start_requests(self):
    #     for url in self.start_urls:
    #         yield Request(url, dont_filter=False)

    """
    如果是要使用布隆过滤器，那就要dont_filter=False,就是要过滤！！！才会使用布隆过滤器，
    这里是重载了这个方法make_request_from_data，使用第一个url的dont_filter=False,但我们不应该第一个url就设置了过滤
    因为第一个过滤那就没有后面的url了，所以只有从第2个url才设置过滤
    """

    # def make_request_from_data(self, data):
    #     req = super().make_request_from_data(data)
    #     req.dont_filter = False
    #     return req

    def parse(self, response):

        """
        1. 获取文章列表中的文章url并交给scrapy下载并进行解析
        2. 获取下一页的url并交给scrapy进行下载，下载完成后交给parse


        :param response:
        :return:
        """


        post_nodes = response.css('.post-item .post-item-text') # 是id就用#,是class就用.,这是获取页面的所有链接
        for post_node in post_nodes:  # 一个一个解析出来
            image_url = post_node.css('.post-item-text .post-item-summary img::attr(src)').extract_first("")  # 解析出图片url
            post_url = post_node.css('.post-item-text a::attr(href)').extract_first("")  # 解析出文章的url
            yield Request(url=parse.urljoin(response.url, post_url), meta={"front_image_url": image_url},
                          callback=self.parse_detail, dont_filter=False)

        # 提取下一页并交给scrapy进行下载
        # next_url = response.css('div.pager a:last-child::text').extract_first("")
        # if next_url == ">":
        #     next_url = response.css('div.pager a:last-child::attr(href)').extract_first("")
        #     yield Request(url=parse.urljoin(response.url, next_url), callback=self.parse, dont_filter=True)

    def parse_detail(self, response):
        pass


