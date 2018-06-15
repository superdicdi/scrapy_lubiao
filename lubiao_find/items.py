# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, Join, MapCompose


def remove_char(value):
    # 去除包含的换行符、分隔符、制表符等，不然将数据到处为 Excel 文件的时候会很乱
    return value.replace('\n', "").replace('\r', "").replace('\t', "").replace(" ", "")


class LubiaoItemLoader(ItemLoader):
    default_output_processor = TakeFirst()
    default_input_processor = MapCompose(remove_char)


class LubiaoFindItem(scrapy.Item):
    title = scrapy.Field()  # 商标名称
    service_list = scrapy.Field()  # 商品/服务列表
    sbiao_category = scrapy.Field()  # 商标未申请群组
    apply_num = scrapy.Field()  # 申请/注册号
    apply_date = scrapy.Field()  # 申请日期
    reg_date = scrapy.Field()  # 注册时间
    inter_class = scrapy.Field()  # 商标类别
    apply_name_ch = scrapy.Field()  # 申请人名称（中文）
    apply_name_en = scrapy.Field()  # 申请人名称（英文）
    apply_addr_ch = scrapy.Field()  # 申请人地址（中文）
    apply_addr_en = scrapy.Field()  # 申请人地址（英文）
    trial_ann_num = scrapy.Field()  # 初审公告期号
    trial_ann_date = scrapy.Field()  # 初审公告日期
    reg_ann_num = scrapy.Field()  # 注册公告期号
    reg_ann_date = scrapy.Field()  # 注册公告日期
    if_comm_sbiao = scrapy.Field()  # 是否共有商标
    sbiao_type = scrapy.Field()  # 商标类型
    special_date = scrapy.Field()  # 专用权期限
    agent_name = scrapy.Field()  # 代理机构名称
    sbiao_process = scrapy.Field(
        output_processor=Join(",")
    )  # 商标流程
    sbiao_detail = scrapy.Field()  # 商标使用详细
    present_status = scrapy.Field()  # 当前状态
    image_url = scrapy.Field()  # 商标logo的url
    status_record = scrapy.Field(
        output_processor=Join(",")
    )  # 公告流程
    brand_date = scrapy.Field()  # 品牌时间
    url = scrapy.Field()  # 详情页的url
