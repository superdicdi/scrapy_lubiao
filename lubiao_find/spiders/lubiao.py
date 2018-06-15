# -*- coding: utf-8 -*-
import re
import urlparse

import scrapy

from lubiao_find.items import LubiaoItemLoader, LubiaoFindItem


class LubiaoSpider(scrapy.Spider):
    name = 'lubiao'
    allowed_domains = ['www.chatm.com']
    start_urls = ['http://www.chatm.com/list?keywords=知呱呱']
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
    }

    position = 2

    def parse(self, response):
        get_nodes = response.xpath('//li[@class="clearfix"]')
        for node in get_nodes:
            url = node.xpath("div[1]/div/a/@href").extract_first()
            present_status = node.xpath("div[2]/p[1]/a/span/text()").extract_first()
            service_list = node.xpath("div[2]/p[last()]/span/text()").extract_first()
            yield scrapy.Request(url=urlparse.urljoin(response.url, url), headers=self.headers,
                                 callback=self.parse_detail,
                                 meta={"service_list": service_list, "present_status": present_status})
        # 下一页的按钮动态生成的， html文件包含了总页数，取出该总页数，然后从第二页开始遍历将 url 加入待爬取页面
        page_nums = re.search("(var pageNum).*?(\d+).*", response.text, re.DOTALL)
        if page_nums:
            try:
                num = int(page_nums.group(2))
                while self.position <= num:
                    page = str(self.position)
                    self.position = self.position + 1
                    yield scrapy.Request(
                        url="http://www.chatm.com/list/知呱呱-i0-0-0-{0}.html?c=0".format(page),
                        headers=self.headers,
                        callback=self.parse,
                    )
            except Exception as e:
                print(e)

    def parse_detail(self, response):
        # 使用 ItemLoader ，统一对字段做处理，使代码看起来整洁易读
        item_loader = LubiaoItemLoader(item=LubiaoFindItem(), response=response)
        item_loader.add_xpath("title", '//table/tbody/tr[1]/td/text()')
        item_loader.add_value("service_list", response.meta.get("service_list", ""))
        item_loader.add_value("present_status", response.meta.get("present_status", ""))
        item_loader.add_xpath("apply_num", '//table/tbody/tr[2]/td[1]/text()')
        item_loader.add_xpath("inter_class", '//table/tbody/tr[2]/td[2]/a/text()')
        item_loader.add_xpath("image_url", '//table/tbody/tr[2]/td[3]/div/img/@src')
        item_loader.add_xpath("apply_date", '//table/tbody/tr[3]/td[1]/text()')
        item_loader.add_xpath("reg_date", '//table/tbody/tr[3]/td[2]/text()')
        item_loader.add_xpath("sbiao_type", '//table/tbody/tr[4]/td[1]/text()')
        item_loader.add_xpath("brand_date", '//table/tbody/tr[4]/td[2]/text()')
        item_loader.add_xpath("apply_name_ch", '//table/tbody/tr[5]/td/text()')
        item_loader.add_xpath("apply_name_en", '//table/tbody/tr[6]/td/text()')
        item_loader.add_xpath("apply_addr_ch", '//table/tbody/tr[7]/td/text()')
        item_loader.add_xpath("apply_addr_en", '//table/tbody/tr[8]/td/text()')
        item_loader.add_xpath("agent_name", '//table/tbody/tr[9]/td/div/text()')
        item_loader.add_xpath("trial_ann_num", '//table/tbody/tr[10]/td[1]/text()')
        item_loader.add_xpath("reg_ann_num", '//table/tbody/tr[10]/td[2]/text()')
        item_loader.add_xpath("trial_ann_date", '//table/tbody/tr[11]/td[1]/text()')
        item_loader.add_xpath("reg_ann_date", '//table/tbody/tr[11]/td[2]/text()')
        item_loader.add_xpath("special_date", '//table/tbody/tr[12]/td[1]/text()')
        item_loader.add_xpath("if_comm_sbiao", '//table/tbody/tr[12]/td[2]/text()')
        item_loader.add_xpath("sbiao_detail", '//table/tbody/tr[13]/td[1]/div/text()')
        item_loader.add_xpath("sbiao_category", '//table/tbody/tr[13]/td[2]/text()')
        item_loader.add_xpath("sbiao_process",
                              '//table/tbody/tr[14]/td/div/p/span/text() | //table/tbody/tr[14]/td/div/p/text()')
        item_loader.add_xpath("status_record",
                              '//table/tbody/tr[15]/td/div/p/span/text() | //table/tbody/tr[15]/td/div/p/text()')
        item_loader.add_value("url", response.url)
        lubiao_item = item_loader.load_item()
        yield lubiao_item
