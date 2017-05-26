import argparse
from scraper.dc_scraper import DCScraper


def parse_args():
    parser = argparse.ArgumentParser(description='中国福利彩票双色球历史数据爬虫')

    help_ = '全量爬取所有历史开奖数据并写入文件'
    parser.add_argument('-a', '--all', help=help_, action='store_true')

    args_ = parser.parse_args()
    return args_


if __name__ == '__main__':
    args = parse_args()
    dc_scraper = DCScraper()
    if args.all:
        total_page = dc_scraper.page_count
        dc_scraper.save_all_history_recorders()
    else:
        print('错误：你必须指定一个参数，请运行-h查看')
