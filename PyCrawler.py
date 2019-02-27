# import lxml
import requests
from bs4 import BeautifulSoup
import re


def html2soup(url):
    r = requests.get(url, timeout=1)
    r.encoding = 'utf-8'
    html = r.content
    soup = BeautifulSoup(html, 'lxml')
    return soup


def find_related_url(url, keyword):
    soup = html2soup(url)
    related_url = {}
    related = soup.find_all('div', attrs={'class': 'show74 left'})
    for u in related:
        if keyword in u.a.text:
            related_url[u.a.text]=u.a['href']
    return related_url


def url_list(main_site, start_pos, keyword, limit):
    depth = 0
    start_url = "".join([main_site, start_pos])
    all_related = find_related_url(start_url, keyword)
    while depth < limit:
        print('Search Time:', depth)
        print('Current URLs:', all_related)
        depth = depth+1
        for pos in all_related.values():
            _ = "".join([main_site, pos])
            new_url= find_related_url(_, keyword)
            # print('NEW:', new_url)
            all_related={**all_related, **new_url}
    return all_related


def get_content(url):
    soup = html2soup(url)
    # three contents: title, main body, right columns
    title = soup.find('div', attrs={'class': 'show17'}).text.strip()
    body = soup.find('div', attrs={'class': 'show63'}).text.strip()
    body = respace(body)
    print('Finish parsing')
    return {'title': title, 'body': body}


def respace(text):
    text = text.replace('\n', '')
    text = text.replace('　', '')
    text = text.replace(' ', '')
    return text


def clean_all_space(text):
    _ = ""
    for line in list(line.strip() for line in text):
        _.join(line)
    return _


def writeFile(content_dict):
    with open('{}.txt'.format(content_dict['title']), 'w', encoding='utf-8') as f:
        f.write("{}\n=====\n".format(content_dict['title']))
        f.write("{}".format(content_dict['body']))
    print('Finish writing 《{}》'.format(content_dict['title']))


if __name__ == '__main__':
    main_site = "http://www.cnbridge.cn/"
    start_pos = "2017/1208/551262.html"
    keyword = "BIM"
    time_limit =1
    urls = url_list(main_site, start_pos, keyword, time_limit)
    for _ in urls.values():
        writeFile(get_content("".join([main_site, _])))
