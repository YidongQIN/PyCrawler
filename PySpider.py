import requests

"""requests 的高阶用法"""

param = {"wd": "检索关键词"}  # 搜索的信息
r1 = requests.get('http://www.baidu.com/s', params=param)
print(r1.url)

data = {'firstname': 'ALARAK', 'lastname': 'Starcraft'}
r2 = requests.post(
    'http://pythonscraping.com/files/processing.php', data=data)
print(r2.text)
