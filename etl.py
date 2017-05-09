import re
import requests
from bs4 import BeautifulSoup
import datetime
import time
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class TicketCrawler:

    target = "youbike"
    url = "http://data.taipei/youbike"
  #  title_filter = ["i本文已被刪除", "公告", "Re:"]
    
    def __init__(self):
        pass

    def get_last_page_number(self):
        res = requests.get(self.url, verify=False)
        first_page = re.search(r'href="/bbs/' + self.target + '/index(\d+).html">&lsaquo;', res.text).group(1)
        return int(first_page)+1

    def get_content(self, url):
        post = requests.get(url, verify=False)
        soup_post = BeautifulSoup(post.text,'html.parser')
        metanum = soup_post.select('.article-meta-value')
        if(len(metanum)<3):
            return

        # get author, time, content
        post_author_t = soup_post.select('.article-meta-value')[0].text
        post_author = post_author_t[0:post_author_t.find(' (')]
        post_time_t = soup_post.select('.article-meta-value')[3].text
        post_content_t = soup_post.select('#main-content')[0].text
        try:
            post_time = datetime.datetime.strptime(post_time_t, "%a %b  %d %H:%M:%S %Y").strftime('%Y-%m-%d %H:%M:%S')
            post_content = post_content_t[post_content_t.find(post_time_t)+25:post_content_t.rfind('--')].rstrip()
        except Exception as e:
            post_time = "N/A"
            post_content = post_content_t[0:post_content_t.rfind('--')].rstrip()
            
        #print (post_author, post_time, post_content)
        return (post_author, post_time, post_content)


    def get_page(self, page_number):
        
        res = requests.get("https://www.ptt.cc/bbs/" + self.target + "/index" + str(page_number) + ".html", verify=False)
        soup = BeautifulSoup(res.text,'html.parser')

        for entry in soup.select(".r-ent"):

            # get title and type
            post_title = entry.select(".title")[0].text.strip('\n')
            post_type = post_title[1:3]
            
            title_filter = ["本文已被刪除", "公告", "Re:"]
            # remove the title which contain "本文已被刪除", "公告", "Re:"
            title_filter_flag = False
            for text in self.title_filter:
                if text in post_title:
                    title_filter_flag = True
            if title_filter_flag:
                continue

            #get url and pid
            post_url = "https://www.ptt.cc" + entry.select(".title")[0].a.get("href")
            pid = int(re.search(r'/M.(\d+)',entry.select(".title")[0].a.get("href")).group(1))
            
            #print (pid, post_type, post_title)
            #print (post_url)
            
            # get content
            post_content, post_author, post_time = self.get_content(post_url)
            
            # feature extraction
            data = {"pid": pid, "title": post_title, "type": post_type, "content": post_content, "author": post_author, "time": post_time}
            print (data)
            
            break

if __name__ == '__main__':
    crawler = TicketCrawler()
    last_page_num = crawler.get_last_page_number()
    crawler.get_page(last_page_num)
