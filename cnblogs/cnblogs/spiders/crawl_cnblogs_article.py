# -*- coding: utf-8 -*-
import scrapy


class CrawlCnblogsArticleSpider(scrapy.Spider):
    name = 'crawl_cnblogs_article'
    allowed_domains = ['www.cnblogs.com']
    start_urls = ['http://www.cnblogs.com/']

    def parse(self, response):
        # 详细页面链接
        href = response.xpath('//*[@id="post_list"]/div/div/h3/a/@href').extract()
        # 调用Request，传递url，指定callback
        for url in href:
            yield scrapy.Request(url=url,callback=self.parse_info)

        # 下一页
        next_page = response.xpath('//*[@id="paging_block"]/div/a[last()]/text()').extract()
        if next_page[0] == 'Next >':  # 判断最后一个节点的文本是否是Next >  以此判断是否达到最后一页
            next_page_href = response.xpath('//*[@id="paging_block"]/div/a[last()]/@href').extract()[0]
            #print(response.urljoin(next_page_href))
            yield scrapy.Request(url=response.urljoin(next_page_href),callback=self.parse)

    # 定义一个处理详细页面链接的方法，抓取详细页面数据
    def parse_info(self,response):
        title = response.xpath('//*[@id="cb_post_title_url"]/text()').extract()[0]
        # lxml中xpath里写string则返回一条字符串
        # 但是在scrapy xpath里无论是什么规则，返回的都是列表
        content = response.xpath('string(//*[@id="cnblogs_post_body"])').extract()[0]
        save_dict = {}
        save_dict['title'] = title
        save_dict['content'] = content
        save_dict['href'] = response.url

        w=lambda x:x+"\r\n"
        with open('test.txt','a+',encoding='utf-8') as f:
            f.write(w(save_dict['title']))
            f.write(w('*'*100))
            f.write(w(save_dict['content']))
            f.write(w('-' * 100))
            f.write(w(save_dict['href']))
            f.write(w('=' * 100))