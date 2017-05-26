import os
import re
import requests
from bs4 import BeautifulSoup
from requests.exceptions import ConnectionError


class DCScraper(object):
    def __init__(self):
        self._start_url = 'http://kaijiang.zhcw.com/zhcw/html/ssq/list.html'
        self._url_template = "http://kaijiang.zhcw.com/zhcw/html/ssq/list_{}.html"
        self._page_count = self.parse_page_count()
        self._winning_num_file = os.path.join(self.get_data_path(), 'data/winning_num.txt')

    @property
    def page_count(self):
        return self._page_count

    def parse_page_count(self):
        html = self.get_page_detail(self._start_url)
        soup = BeautifulSoup(html, 'lxml')
        tags = soup.select("p strong")
        page_count = int(tags[0].text)
        return page_count

    def get_page_url(self, page_num):
        return self._url_template.format(str(page_num))

    def parse_winning_numbers(self, page_num):
        url = self.get_page_url(page_num)
        html = self.get_page_detail(url)
        soup = BeautifulSoup(html, 'lxml')
        em_tags = soup.find_all('em')
        content = soup.find_all('td', {'align': 'center'})

        with open(self._winning_num_file, 'a') as fp:
            ball_num_in_one_group = 7
            pattern = re.compile("\d{4}-\d{2}-\d{2}", re.S)
            draw_date = re.findall(pattern, str(content))
            for i in range(len(draw_date)):
                start = i * ball_num_in_one_group
                end = start + ball_num_in_one_group
                winning_num = [int(em_tag.get_text()) for em_tag in em_tags[start:end]]
                recorder = "#('{0}','{1}')\n".format(draw_date[i], str(winning_num))
                print("开奖日:%s" % draw_date[i])
                print("中奖号码：%s" % winning_num)
                print("已写入文件")
                print("\n")
                fp.write(str(recorder))

    def save_all_history_recorders(self):
        for page_num in range(self._page_count):
            self.parse_winning_numbers(page_num + 1)

    @staticmethod
    def get_page_detail(page_url):
        try:
            response = requests.get(page_url)
            if response.status_code == 200:
                return response.text
            return None
        except ConnectionError:
            print('Error occurred')
            return None

    @staticmethod
    def get_data_path():
        return os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                os.path.pardir)
        )
