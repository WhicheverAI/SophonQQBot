#%%
# from bs4 import BeautifulSoup
import requests
from lxml import etree

# # 假设 html_content 是从 HTML 文件中读取的内容
# # with open("查看投票结果.html") as f:
#     # html_content = f.read()
# url = 'https://tp.wjx.top/wjx/join/tpresult.aspx?activity=263363052'

# user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'

# # 创建一个 Session 对象
# session = requests.Session()
# session.headers.update({
#     'User-Agent': user_agent
# })
# # 发送 GET 请求
# response = session.get(url, 
#                         )

# # 检查请求是否成功
# if response.status_code == 200:
#     # 获取 HTML 内容
#     html_content = response.text
# else:
#     print(f"Failed to retrieve content, status code: {response.status_code}")
# html_content

#%%
# # 使用 BeautifulSoup 解析 HTML 内容
# soup = BeautifulSoup(html_content, 'lxml')

# # 找到包含投票信息的表格的所有行

        
# %%
import lxml
lxml.etree._Element
#%%
# def parse(url = 'https://tp.wjx.top/wjx/join/tpresult.aspx?activity=263363052'
#           , rank_limit=15):
#     user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'

#     # 创建一个 Session 对象
#     session = requests.Session()
#     session.headers.update({
#         'User-Agent': user_agent
#     })
#     # 发送 GET 请求
#     response = session.get(url, 
#                             )

#     # 检查请求是否成功
#     if response.status_code == 200:
#         # 获取 HTML 内容
#         html_content = response.text
#     else:
#         print(f"Failed to retrieve content, status code: {response.status_code}")
#         return []
#     tree = etree.HTML(html_content)
#     tree2 = etree.ElementTree(tree)

#     # 提取前15名候选人的信息
#     for i in range(rank_limit):  # 从第2位到第16位，共15个候选人
#         name = None
#         destination = None
#         rate = None
#         xpath = f"//*[@id='divResult']/div[2]/div[{i+2}]/div[2]/div[1]/div[1]"
#         # xpath = f"//*[@id='divResult']/div[2]/div[{i+2}]/div[2]/div[1]/div[2]"
#         candidate_info = tree.xpath(xpath)
#         if candidate_info:
#             # print(candidate_info[0].text)
#             text = candidate_info[0].text
#             # 使用正则表达式匹配并提取姓名和去向
#             import re
#             match = re.search(r'(.+?) 去向：(.+)', text)
#             if match:
#                 name = match.group(1)  # 提取姓名
#                 destination = match.group(2)  # 提取去向
#                 # print(f'姓名: {name}, 去向: {destination}')
#             else:
#                 print('未找到匹配项')
#         xpath = f"//*[@id='divResult']/div[2]/div[{i+2}]/div[2]/div[1]/div[2]"
#         candidate_info = tree2.xpath(xpath)
#         if candidate_info:
#             rate = candidate_info[0].text
#         yield dict(
#             姓名=name, 
#             去向=destination,
#             得票率=rate
#         )
def parse(url = 'https://tp.wjx.top/wjx/join/tpresult.aspx?activity=263363052'
          , rank_limit=15):
    with open('/home/yecm/yecanming/repo/fun/nonebot2-qq-starter/plugins/ranker/结果.txt', 'r') as f:
        lines = f.readlines()
    # lines
    for i in range(0, len(lines), 5):
        name = lines[i].split(" ")[0]
        destination = lines[i+2][5:-1]
        rate = lines[i+3].split(" ")[0]
        d = dict(
                姓名=name, 
                去向=destination,
                得票率=rate
            )
        # print(d)
        yield d

# list(parse())
# %%

# %%
