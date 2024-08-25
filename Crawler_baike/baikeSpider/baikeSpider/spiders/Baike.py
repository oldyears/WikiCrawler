import scrapy
import json
import csv
from urllib.parse import quote


class BaikeSpider(scrapy.Spider):
    name = "Baike"
    # allowed_domains = ["zh.wikipedia.org"]
    base_url = "https://baike.baidu.com/item/"
    
    def start_requests(self):
        file_path = '../../../empty_all_s.txt'
        label_names = []
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = file.readlines()
            for row in reader:
                label_names.append([row.strip().split(' ')[0], row.strip().split(' ')[-1]])
                # print("label:" + row.strip().split(' ')[-1] + " id:" + row.strip().split(' ')[0])

        for id, label in label_names:
            encoded_name = quote(label, encoding='UTF-8')
            dynamic_url = f"{self.base_url}{encoded_name}"
            yield scrapy.Request(url=dynamic_url, callback=self.parse, meta={"id":id})
        # dynamic_url = self.base_url + "袁家军书记"
        # yield scrapy.Request(url=dynamic_url, callback=self.parse, meta={"id":"31"})


    def parse(self, response):
        extra_param = response.meta.get('id')
        items = {}
        items["id"] = str(extra_param)
        # 使用XPath选择class属性为itemWrapper_j8T_O的所有元素
        elements = response.xpath('//*[contains(@class, "itemWrapper")]')
        
        for element in elements:
            # 提取属性名称和属性值
            item_name = element.xpath('.//*[contains(@class, "itemName")]/text()').get().replace('\xa0', '')
            item_value = element.xpath('.//*[contains(@class, "itemValue")]').xpath('string(.)').get()
            item_value = ''.join(item_value).strip()

            if item_name and item_value:
                # items.append({
                #     'attribute': item_name,
                #     'value': item_value
                # })
                items[item_name] = item_value

        # 将结果存储为JSON文件
        # with open('baike_info.json', 'w', encoding='utf-8') as f:
        #     json.dump(items, f, ensure_ascii=False, indent=4)

        # yield {
        #     'status': 'success',
        #     'items': items
        # }
        return items
            
