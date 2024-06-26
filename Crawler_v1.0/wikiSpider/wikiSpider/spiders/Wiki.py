import scrapy
import json
from urllib.parse import quote
from wikiSpider.items import WikispiderItem


class WikiSpider(scrapy.Spider):
    name = "Wiki"
    allowed_domains = ["zh.wikipedia.org"]
    
    def start_requests(self):
        # 固定网址前缀
        base_url = "https://zh.wikipedia.org/wiki"

        # 读取所有person
        file_path = '../../news_ner.json'
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        # 提取所有标记为 "PERSON" 的姓名
        person_names = set([])
        for article in data[:10]:
            for entity in article:
                if entity[1] == "PERSON":
                    person_names.add(entity[0])

        # 动态生成 URL 并发起请求
        for name in person_names:
            # https://zh.wikipedia.org/wiki/%E7%BE%85%E8%87%B4%E6%94%BF
            encoded_name = quote(name, encoding='UTF-8')
            dynamic_url = f"{base_url}/{encoded_name}"
            yield scrapy.Request(url=dynamic_url, callback=self.parse)


    def parse(self, response):
        # 存放每个person的数据
        items = []

        # 保存person属性数据
        item = {}

        ### 先处理可以直接爬取的数据
        ## 由于每个人的个人资料不同，所以合理的做法是取person的个人资料全部属性分别存储

        # 姓名
        re = response.xpath('//*[@id="firstHeading"]/span/text()')
        name = re.get() if len(re) > 0 else None
        item['name'] = name

        # 单纯只爬取个人资料
        res = response.xpath("//tr[th[@colspan='2' and contains(text(), '个人资料')]]/following::tr")

        for re in res:
            re_str = re.xpath('string(.)').get()
            if len(re_str) == 0:
                break

            attr_th = re.xpath('th')
            attr = attr_th.xpath('string(.)').get()
            re_str = re_str.replace(attr, "").strip()
            item[attr] = re_str

        # 职位：考虑到有些人不存在此选项，所以取第一个职位信息，若无则置空
        re = response.xpath("//tr[following-sibling::tr[1][contains(., '现任')]]")
        current_position = re[0].xpath('string(.)').get().strip() if len(re) > 0 else None
        item['current_position'] = current_position
        
        # 最高学历
        re = response.xpath("//div[text()='学历']/following::ul/li/ul/ul/li[last()]")
        highest_degree = re.xpath('string(.)').get() if len(re) > 0 else None
        item['highest_degree'] = highest_degree


        # 必须拥有选举记录数据才能收集以下信息
        re = response.xpath("//h2/span[@id='選舉紀錄']")
        if len(re) > 0 :
            # 从政时长
            start_year = response.xpath("//h2/span[@id='選舉紀錄']/following::table[1]/tbody/tr[2]/td[1]/text()").get().strip()
            latest_year = response.xpath("//h2/span[@id='選舉紀錄']/following::table[1]/tbody/tr[last()]/td[1]/text()").get().strip()
            time_in_politics = int(latest_year) - int(start_year)

            # 参与选举次数
            number_of_elections = len(response.xpath("//h2/span[@id='選舉紀錄']/following::table[1]/tbody/tr")) - 1

            # 选举平均支持率
            aveSup_elections = 0
            for i in range(2, number_of_elections + 2):
                location = "//h2/span[@id='選舉紀錄']/following::table[1]/tbody/tr[" + str(i) + "]/td[contains(text(), '%')]/text()"
                re = response.xpath(location)
                if len(re) > 0:
                    aveSup_elections += float(re.get().strip().strip('%'))
            aveSup_elections /= number_of_elections
            aveSup_elections = f"{aveSup_elections:.3f}%"

            # 选举成功率
            sucRate_elections = 0
            for i in range(2, number_of_elections + 2):
                location = "//h2/span[@id='選舉紀錄']/following::table[1]/tbody/tr[" + str(i) + "]/td[last()-1]/@rowspan"
                re = response.xpath(location)
                if len(re) > 0:
                    sucRate_elections += int(re.get())
                    print(int(re.get()))
            sucRate_elections = sucRate_elections / number_of_elections * 100
            sucRate_elections = sucRate_elections if sucRate_elections <= 100 else 100
            sucRate_elections = f"{sucRate_elections}%"

            item['time_in_politics'] = time_in_politics
            item['number_of_elections'] = number_of_elections
            item['aveSup_elections'] = aveSup_elections
            item['sucRate_elections'] = sucRate_elections


        return item
