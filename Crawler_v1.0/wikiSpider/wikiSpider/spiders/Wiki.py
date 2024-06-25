import scrapy
from wikiSpider.items import WikispiderItem


class WikiSpider(scrapy.Spider):
    name = "Wiki"
    allowed_domains = ["zh.wikipedia.org"]
    start_urls = ["https://zh.wikipedia.org/zh-cn/%E8%B3%B4%E6%B8%85%E5%BE%B7"]

    def parse(self, response):
        # 存放每个person的数据
        items = []

        # 保存person属性数据
        item = WikispiderItem()

        ### 先处理可以直接爬取的数据
        ## 由于每个人的个人资料不同，所以干脆直接全部爬取
        # 姓名
        name = response.xpath('//*[@id="firstHeading"]/span/text()').get()
        # 年龄
        age = response.xpath("//span[@class='noprint ForceAgeToShow']/text()[2]").get().strip('）')

        # 职位：考虑到有些人不存在此选项，所以取第一个职位信息，若无则置空
        current_position = response.xpath("//tr[following-sibling::tr[1][contains(., '现任')]]")[0].xpath('string(.)').get().strip()
        
        # 政党
        political_parties = response.xpath("//tr[th[@scope='row' and contains(text(), '政党')]]/td/a/text()").get().strip()
        
        # 职业
        career = response.xpath("//tr[th[@scope='row' and contains(text(), '职业')]]/td/div/ul/li/text()").getall()
        
        # 配偶
        spouse = response.xpath("//tr[th[@scope='row' and contains(text(), '配偶')]]/td/a/text()").get().strip()
        
        # 儿女
        children = response.xpath("//tr[th[@scope='row' and contains(text(), '儿女')]]/td/text()[1]").get().strip()
        
        # 亲属
        relatives = response.xpath("//tr[th[@scope='row' and contains(text(), '亲属')]]/td//text()").extract()
        
        # 居住地
        residence = response.xpath("//tr[th[@scope='row' and contains(text(), '居住地')]]/td/a/text()").get().strip()
        
        # 最高学历
        highest_degree = response.xpath("//div[text()='学历']/following::ul/li/ul/ul/li[last()]/a/text()").get()
        highest_degree += response.xpath("//div[text()='学历']/following::ul/li/ul/ul/li[last()]/text()").get()
        
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
            re = response.xpath(location).get()
            if re:
                aveSup_elections += float(re.strip().strip('%'))
        aveSup_elections /= number_of_elections
        aveSup_elections = f"{aveSup_elections:.3f}%"

        # 选举成功率
        sucRate_elections = 0
        for i in range(2, number_of_elections + 2):
            location = "//h2/span[@id='選舉紀錄']/following::table[1]/tbody/tr[" + str(i) + "]/td[last()-1]/@rowspan"
            re = response.xpath(location).get()
            if re:
                sucRate_elections += int(re)
        sucRate_elections = sucRate_elections / number_of_elections * 100
        sucRate_elections = f"{sucRate_elections}%"
        
        item['name'] = name
        item['age'] = age
        item['current_position'] = current_position
        item['political_parties'] = political_parties
        item['career'] = career
        item['spouse'] = spouse
        item['children'] = children
        item['relatives'] = relatives
        item['residence'] = residence
        item['highest_degree'] = highest_degree
        item['time_in_politics'] = time_in_politics
        item['number_of_elections'] = number_of_elections
        item['aveSup_elections'] = aveSup_elections
        item['sucRate_elections'] = sucRate_elections


        return item
