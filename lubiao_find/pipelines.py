# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


import pymysql


class MysqlPipeline(object):
    def __init__(self):
        self.conn = pymysql.connect(host="127.0.0.1", user="root", passwd="123456", db="sbiao_data", charset="utf8",
                                    use_unicode=True)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        # 经过 ItemLoader 处理过的 item ，如果字段为空，则不返回该字段，因此先做判断
        def if_key(key):
            if dict(item).has_key(key):
                return item[key]
            return ''

        insert_sql = """
                    insert into lubiao(title, service_list, sbiao_category, apply_num, apply_date, inter_class,
                                      apply_name_ch, apply_name_en, apply_addr_ch, apply_addr_en, special_date, 
                                      present_status, image_url, sbiao_detail, sbiao_process, brand_date,
                                      trial_ann_num, trial_ann_date, reg_ann_num, reg_ann_date,
                                      reg_date, agent_name, sbiao_type, if_comm_sbiao, status_record, url)
                    values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
        self.cursor.execute(insert_sql,
                            (if_key("title"), if_key("service_list"), if_key("sbiao_category"), if_key("apply_num"),
                             if_key("apply_date"), if_key("inter_class"), if_key("apply_name_ch"),
                             if_key("apply_name_en"),
                             if_key("apply_addr_ch"), if_key("apply_addr_en"), if_key("special_date"),
                             if_key("present_status"),
                             if_key("image_url"), if_key("sbiao_detail"), if_key("sbiao_process"), if_key("brand_date"),
                             if_key("trial_ann_num"), if_key("trial_ann_date"), if_key("reg_ann_num"),
                             if_key("reg_ann_date"),
                             if_key("reg_date"), if_key("agent_name"),
                             if_key("sbiao_type"), if_key("if_comm_sbiao"), if_key("status_record"), if_key("url")))
        self.conn.commit()
        return item
