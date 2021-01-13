import requests
import json
import time
import sys
sys.setrecursionlimit(10000)
from bs4 import BeautifulSoup

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                        'Chrome/51.0.2704.63 Safari/537.36'}

url = "https://www.zhihu.com/api/v4/questions/{}/answers?include=data%5B%2A%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cattachment%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Cis_labeled%2Cpaid_info%2Cpaid_info_content%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cis_recognized%3Bdata%5B%2A%5D.mark_infos%5B%2A%5D.url%3Bdata%5B%2A%5D.author.follower_count%2Cbadge%5B%2A%5D.topics%3Bdata%5B%2A%5D.settings.table_of_content.enabled&limit=5&offset=0&platform=desktop&sort_by=default"


class zhihu():
    current_page = 0
    def parserContent(self,content):
        self.current_page += 1
        content_json = json.loads(content)
        content_data = content_json["data"]
        content_page = content_json["paging"]
        next_url = content_page["next"]
        for data in content_data:
            content_text = data["content"]
            bp = BeautifulSoup(content_text,'html.parser')
            content_img = bp.find_all('img')
            for img_tag in content_img:
                if img_tag is None:
                    continue
                img = img_tag.get('src')
                if "data:image/svg+xml;utf8" in img:
                    continue
                print(img)
                self.download_img(img)


        #循环次数
        page_number = content_page["totals"]
        print((self.current_page / page_number) * 100)
        is_end = content_page["is_end"]
        if is_end is not True:
            self.request(next_url)
        print("抓取完成")

    def request(self,url):
        print(url)
        req = requests.get(url,headers = headers)
        req.encoding = 'utf-8'
        content = req.text
        self.parserContent(content)

    def download_img(self,img_url):
        r = requests.get(img_url, stream=True)
        if r.status_code == 200:
            open('/Users/a10943/Desktop/img/%s.png'%time.time(), 'wb').write(r.content)  # 将内容写入图片
            print("done")
        del r


if __name__ == '__main__':
    zhihu = zhihu()
    id_ = input("请输入问题的ID：")
    zhihu.request(url.format(id_))
