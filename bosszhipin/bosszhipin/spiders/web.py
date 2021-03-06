import scrapy
import re
import time
from bosszhipin.items import BosszhipinItem


class bosszhipinSpider(scrapy.Spider):
    name = 'web'
    # allowed_domains = []
    #起始页
    start_urls = ['https://www.zhipin.com/job_detail/?query=&city=101270100&industry=&position=100205']

    def parse(self, response):
        # 循环搜索结果列表，提取相关内容
        for each in response.xpath('//div[@class = "job-list"]/ul/li'):
            item = BosszhipinItem()
            item['jobName'] = each.xpath('./div/div[1]/h3/a/div[1]/text()').extract_first()
            item['jobType'] = 'web前端'
            item['company'] = each.xpath('./div/div[2]/div/h3/a/text()').extract_first()
            item['companyType'] = each.xpath('./div/div[2]/div/p/text()[1]').extract_first()
            item['salary'] = self.transalary(each.xpath('./div/div[1]/h3/a/span/text()').extract_first())
            item['city'] = each.xpath('./div/div[1]/p/text()[1]').extract_first()
            item['workingExp'] = each.xpath('./div/div[1]/p/text()[2]').extract_first()
            item['eduLevel'] = each.xpath('./div/div[1]/p/text()[3]').extract_first()
            item['welfare'] = ' '
            item['timestate'] = self.trantime(each.xpath('./div/div[3]/p/text()').extract_first())
            item['detail'] = response.urljoin(each.xpath('./div/div[1]/h3/a/@href').extract_first())

            yield item


        # #翻页
        # url = response.xpath('//a[@class = "next"]/@href').extract_first()
        # if url is not None:
        #     page = response.urljoin(url)
        #     yield scrapy.Request(page, callback=self.parse)

    def trantime(self, date):
        match1 = re.match(r'(发布于)(\d+月\d+)日', date)
        if match1:
            timestate = match1.group(2).replace('月', '-')
            loacltime = str(time.strftime("%m-%d", time.localtime()))
            if timestate > loacltime:
                return "2018-"+timestate
            else:
                return "2019-"+timestate
        else:
            timestate = str(time.strftime("%m-%d", time.localtime()))
            return "2019-"+timestate

    def transalary(self, salary):
        result = salary.replace('k', 'K')
        return result












