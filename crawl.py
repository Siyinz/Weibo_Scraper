from urllib.request import urlopen
from urllib.request import Request
from urllib.parse import quote
import ssl
import urllib.request

from bs4 import BeautifulSoup

import my_io
import re

import microblog

# 用于延时
import time

# 用于生成延时随机数
import random

import sys

import tools

import os

############################################################### 
ssl._create_default_https_context = ssl._create_unverified_context
response = urllib.request.urlopen('https://www.python.org')

'''
设置要爬取的url
mobile高级搜索设置
返回要每一天要爬取的第一个url
'''
def set_first_url(keyword, start_time, end_time,rand):
    ori = 'https://weibo.cn/search/?advancedfilter=1'

    keyword = 'keyword=' + quote(keyword)  # 必须是英文或者中文转码，也就是说必须是ASCII

    sort = 'sort=time'

    smblog = '搜索'

    url_smblog = 'smblog=' +  quote(smblog)  

    #rand 会变，每换一个话题，都要在浏览器中重新获取rand值
    rand = 'rand=' + str(rand)
    others = 'p=r&' + rand + '&p=r'

    connector = '&'

    start_time = 'starttime=' + start_time
    end_time = 'endtime=' + end_time
 
    url = ori +  connector + keyword + connector + start_time \
        + connector + end_time + connector + sort \
        + connector + url_smblog + connector + others

    return url

###############################################################
############################################################### 

'''
设置要爬取的下一页的url
返回要爬取的url
还没测试
'''
def set_next_url(keyword, start_time, end_time, page_number):

    ori = "https://weibo.cn/search/mblog?hideSearchFrame="
    keyword = 'keyword=' + quote(keyword)  # 必须是英文或者中文转码，也就是说必须是ASCII
    advanced_setting = 'advancedfilter=1'

    sort = 'sort=time'

    page = 'page=' + str(page_number)  
    connector = '&'

    start_time = 'starttime=' + start_time
    end_time = 'endtime=' + end_time

    url = ori +  connector + keyword + connector + advanced_setting \
        + connector + start_time + connector + end_time \
        + connector + sort + connector + page

    return url

############################################################### 
'''
下载给定url的网页
返回值：网页的 字符串 形式
如果返回 -1，说明爬取失败， 那么马上 进行数据的存储
'''
def downloadHtml(url):
    
    user_agents = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36",
    #"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Safari/605.1.15",
    #"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36"
    ]
    
    # 一定要保持这几个账号保持登陆状态，否则会导向登陆页面，导致爬取失败
    # 在同一个浏览器环境下，登陆另外一个账号会把前一个账号挤掉，所以要在隐身模式下登陆，然后再关掉
    cookies = [
            '_T_WM=f407cc2ef2c8de9a07072e10aae7c160; WEIBOCN_WM=3349; H5_wentry=H5; backURL=https%3A%2F%2Fweibo.cn; SUB=_2A25ydzbzDeRhGeBM71AY-SjKyzqIHXVRmFq7rDV6PUNbktANLXP1kW1NRPm7ChXhWIg15SyLU6i37RRC4eqk0P8L; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5UkaVanhOeLjb3W2lSnNkT5JpX5KzhUgL.FoqEShz41Kqcehq2dJLoI7fegHSWK.x8-oe7e02p; SUHB=0Ry6_yqCpCI3eC; SSOLoginState=1601390243; ALF=1603982243',
            #'_T_WM=0c6e83e35dfe7098159e25dc74835697; WEIBOCN_WM=3349; H5_wentry=H5; backURL=https%3A%2F%2Fweibo.cn%2F; SUB=_2A25ycOxQDeRhGeBM71AY-SjKyzqIHXVRmvQYrDV6PUNbktANLXmlkW1NRPm7ChfXZ9yJKFk3Lo92eVQqsotlc4Wh; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5UkaVanhOeLjb3W2lSnNkT5JpX5KzhUgL.FoqEShz41Kqcehq2dJLoI7fegHSWK.x8-oe7e02p; SUHB=0vJY4uYi-WEkoX; SSOLoginState=1601477632; ALF=1604069632'
            #'ALF=1604068807; SSOLoginState=1601476807; SUB=_2A25ycOiXDeRhGeBM71AY-SjKyzqIHXVRmojfrDV6PUNbktAKLUnFkW1NRPm7CnMrJ3KieGx_1v9IXwEyPHJX6Cb4; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5UkaVanhOeLjb3W2lSnNkT5JpX5KzhUgL.FoqEShz41Kqcehq2dJLoI7fegHSWK.x8-oe7e02p; SUHB=0nl-5772ZzFg6c; _T_WM=b3138de4aa650c5de8271cdf8d67cc4e'
            ]

    # 模拟了真实的浏览器，包括 cookie,user-agent等元素，最好是在进入了某一个电影的评论页面，再获取header
    headers = { 
		'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
		'Accept-Language':'en,zh-CN;q=0.9,zh;q=0.8,la;q=0.7,und;q=0.6',
		'Cache-Control':'max-age=0',
		'Connection':'keep-alive',
		'Cookie': random.choice(cookies),
        'Host':'weibo.cn',
		'Upgrade-Insecure-Requests':'1',
		'User-Agent': random.choice(user_agents)
		}  

    req = Request(url=url, headers=headers)
    
    html = -1 # 如果返回 -1，说明爬取失败， 那么马上 进行数据的存储
    
    # 解决爬取失败问题
    try:
        html = urlopen(req).read().decode('utf-8')
    except Exception as e:
        print(e)
        return html
    return html

###############################################################
'''
用beautifulsoap 修补一下网页
'''
def fix_html(html_str):
    # 修补html
    soup = BeautifulSoup(html_str,'html.parser', from_encoding="gb18030")
    fixed_html = soup.prettify()
    
    return fixed_html

############################################################### 
'''
对网页内容进行解析，得到
1、昵称
2、主页地址
3、所在地区（详细地址）
4、点赞数，转发数，评论数
5、发微博的时间
6、微博内容
7、地址
8、性别
获取还有多少页没有爬的信息
返回爬取完一个页面后得到的 微博集合(microblog_quene) + 下页信息
result的返回值有
    1、dayover 爬取结束，该天爬取结束         'dayover'
    2、next_page            整型
    3、爬取失败，重新爬取     'nexttry'
    4、exit 退出程序
'''
def parse_main_content(html_str):

    result = 'default'
    
    # 解析每一条微博
    microblog_quene = []
    
    soup = BeautifulSoup(html_str,'html.parser')
    
    allpage = 'default'
    
    # 该天没有微博
    re_no_weibo = '抱歉，未找到.*相关结果'
    if re.search(re_no_weibo, html_str): # 无微博
        result = 'dayover'
        info = '该天没有搜索到相关微博'
        log(info)
        return microblog_quene, result, allpage
    
    # 获取微博条数信息
    weibo_nums = -1
    re_weibo_nums = '共\d*条'
    if re.search(re_weibo_nums, html_str): # 有条数信息
        weibo_nums_str = re.findall(re_weibo_nums,html_str)[0]
        weibo_nums = (int)(weibo_nums_str[1:len(weibo_nums_str)-1])
    else: # 无条数信息，网页有问题
        result = 'nexttry'
        info = '爬取到的信息有错误，需要重新爬取该页面'
        log(info)
        return microblog_quene, result, allpage
    
     
    # 获取包含 class 为 c ，存在id属性的 div  很重要
    microblog_soups = soup.find_all('div', attrs = {'class' : 'c'}, id = re.compile('.*'))
    
    # 获取页面信息，看看还有多少页面没有爬取,这里可能会出问题，导致page_info为none，
    # 问题可能出在：爬取到的信息出错，需要重新爬一遍
    page_info = soup.find('div',attrs = {'class' : 'pa'})
    
     # 没有微博，但是显示了条数，这是一个特殊情况，说明到了最后一页了，要停止爬取
    if len(microblog_soups) == 0 and weibo_nums != -1:
        result = 'dayover'
        info = '爬取到了最后一页，但是没有数据，特殊情况，结束爬取'
        log(info)
        return microblog_quene, result, allpage 

    if page_info == None: # 无上下页信息
        if len(microblog_soups) > 0: # 有微博
            result = 'dayover'
            info = '该天的微博只有一页'
            log(info)
        else:# 无微博，无上下也信息：页面爬取失败
            result = 'nexttry'
            info = '爬取到的信息有错误，需要重新爬取该页面'
            log(info)
            return microblog_quene, result, allpage
    else: # 有上下页信息
        page_info = page_info.get_text().strip()

        result = 'dayover'
        if page_info.find('下页') == -1: # 没有找到下页，说明到了最后一页
            return microblog_quene, result, allpage
        else:
            re_str = r'[1-9][0-9]*/[1-9][0-9]*页'  ## 匹配的结果  1/100页
            ss = re.findall(re_str, page_info)[0]

            # 获取下一页
            nextpage = int(ss[0 : ss.find('/')]) + 1
            result = nextpage
            allpage = int(ss[ss.find('/') + 1 : ss.find('页')])

    # 对每一条blog进行遍历爬取
    for microblog_soup in microblog_soups:

        # 获取昵称
        # nickname = microblog_soup.find('a',attrs = {'class' : 'nk'})
        # # 进行判空处理，防止程序异常退出
        # if nickname == None: # 页面爬取失败，重新爬取
        #     result = 'nexttry'
        #     info = '爬取到的信息有错误，需要重新爬取该页面'
        #     log(info)
        #     return microblog_quene, result, allpage
        # else:
        #     nickname = nickname.get_text().strip()

        # 获取用户主页  https://weibo.cn/a813689091
        # index = microblog_soup.find('a',attrs = {'class' : 'nk'}).get('href')
        # # 进行判空处理，防止程序异常退出
        # if index == None: # 页面爬取失败，重新爬取
        #     result = 'nexttry'
        #     info = '爬取到的信息有错误，需要重新爬取该页面'
        #     log(info)
        #     return microblog_quene, result, allpage
        # else:
        #     index = index.strip()
        # print('index : ' + index + '\n')

        # 地址和性别
        # sex,location = parse_user(index)

        # 爬取用户主页的时候遇到问题,可能被禁掉
        # if sex == -1 or sex == -2:
        #     info = '爬取用户主页失败'
        #     log(info)
        #     try_times = 3
        #     while try_times > 0:
        #         try_times = try_times - 1
        #         if sex == -2: # 解析网页的时候失败，说明返回的网页有问题，要重新爬取
        #             time_delay = random.randint(10,20)
        #         else :
        #             time_delay = 60 #* 6 # 爬取网页失败，6分钟后进行第二次尝试
        #         time.sleep(time_delay)
        #         info = '爬取用户主页失败,尝试重新爬取'
        #         log(info)
        #         sex,location = parse_user(index) # 第二次尝试
        #         if sex != -1 and sex != -2:
        #             break
        #     if try_times == 0: ## 尝试三次后仍然不成功
        #         result = 'exit'
        #         return microblog_quene, result, allpage

        # 获取用户内容,内容中间有很多空格，需要删减
        # content需要分 是转发的，还是原创的
        divs = microblog_soup.find_all('div')
        ss = ''
        flag = 0 # 表示不是转发的 2 表示是转发的  双重保险，只有出现了 ‘转发理由’ 和 ‘转发了’，才能证明这条微博是转发的
        aim_div = divs[0]
        for div in divs:
            ss = div.get_text().strip()
            if ss.find('转发理由:') != -1 or ss.find('转发了') != -1:
                if ss.find('转发理由:') != -1: # 确认是转发的微博后定位到内容div
                    aim_div = div
                flag = flag + 1

        if flag == 2: # 表示这条微博是转发的
            ss = aim_div.get_text().strip()
            content = ss[ss.find('转发理由') + 5 : ss.find('赞[0]')]
        else: # 这条微博是原创的微博
            content = microblog_soup.find('span',attrs = {'class' : 'ctt'}).get_text().strip()

        # print('content:' + content + '\n')

        # 获取时间   03月15日 23:26
        try:
            time1 = microblog_soup.find('span',attrs = {'class' : 'ct'}).get_text().strip()
            re_fore_year = r'[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]'
            if re.search(re_fore_year, time1): # 表示爬取的事去年的数据
                time1 = time1[:19]
            else: # 爬取的是今年的数据
                time1 = time1[:12]
        except AttributeError:
            time1 = 'NA'
        # print('time:' + time + '\n')

        ## 用来匹配评论数、转发数等数字
        # re_num = '[0-9]*'

        # # 获取点赞数  例如：0
        # re_str = u'https://weibo.cn/attitude.*' # 正则表达式，用来匹配href的值
        # try:
        #     thumb_up = microblog_soup.find('a', href = re.compile(re_str)).get_text().strip()
        #     thumb_up_count = int(re.findall(re_num,thumb_up[2:])[0])
        # except AttributeError:
        #     thumb_up_count = 0
        # # print('thumb_up_count:' + str(thumb_up_count) + '\n')

        # # 获取转发数  例如：0
        # re_str = u'https://weibo.cn/repost.*'  # 正则表达式，用来匹配href的值
        # try: 
        #     repost = microblog_soup.find('a', href = re.compile(re_str)).get_text().strip()
        #     repost_count = int(re.findall(re_num,repost[3:])[0])
        # except AttributeError:
        #     repost_count = 0
        # # print('repost_count:' + str(repost_count) + '\n')

        # # 获取评论数  例如：0
        # re_str = u'https://weibo.cn/comment.*' # 正则表达式，用来匹配href的值
        # # 如果用户转发了别人的微博，那么这里评论会有两个，第一个是原文评论，第二个才是用户的评论
        # try: 
        #     comment = microblog_soup.find_all('a', attrs = {'class' : 'cc'}, href = re.compile(re_str))
        #     commentlen = len(comment)
        #     if commentlen == 1: # 不是转发
        #         comment = comment[0].get_text().strip()
        #     else:
        #         comment = comment[1].get_text().strip()
        #     try:
        #         comment_count = int(float(re.findall(re_num,comment[3:])[0]))
        #     except ValueError:
        #         comment_count = 0
        # except AttributeError:
        #     comment_count = 0

        #print('comment_count:' + str(comment_count ) + '\n')

        #print('============================================================')

        # new 一个微博的类,装入上面爬取到的信息
        microblog_item = microblog.microblog()

        # microblog_item.set_neckname(nickname)
        # microblog_item.set_index(index)
        # microblog_item.set_location(location)
        # microblog_item.set_comment_count(comment_count)
        # microblog_item.set_sex(sex)
        # microblog_item.set_repost_count(repost_count)
        # microblog_item.set_thumb_up_count(thumb_up_count)
        microblog_item.set_time(time1)  # 这里忘记改了。。。
        microblog_item.set_content(content)

        microblog_quene.append(microblog_item)

    return microblog_quene, result, allpage

############################################################### 
'''
根据用户主页的url，爬取用户的相关信息，例如性别、所在地等信息
还可以爬取更多信息，例如学历，是否为大V
返回性别和位置
如果返回 -1 -1,则表示爬取失败，重新爬取
如果返回 -2 -2，则表示爬取的内容有错误，需要重新爬取
'''
def parse_user(url):

    sex = -2
    location = -2

    # 获取原网页
    html_source = downloadHtml(url)

    # 爬取失败
    if html_source == -1:
        return html_source, html_source

    # 修补网页
    fixed_html = fix_html(html_source)

    soup = BeautifulSoup(fixed_html, "html.parser")

    user_soup = soup.find('div',attrs = {'class' : 'u'})

    # 判断是否爬取的内容有错误
    if user_soup == None:
        return sex,location 

    # 性别和地址所在的字符串
    sex_location = user_soup.find('span',attrs = {'class' : 'ctt'})

    # 判断是否爬取的内容有错误
    if sex_location == None:
        return sex,location 

    sex_location = sex_location.get_text().strip()


    # 写正则表达式取出性别和地址
    re_str = r'男/.{0,6}|女/.{0,8}'
    sex_location = re.findall(re_str,sex_location)[0]
    sex = sex_location[:1]
    location = sex_location[2:]

    #print(sex)
    #print(location)
    #print("-----------------------------------")

    return sex,location

###############################################################

'''
在系统运行中打log
'''
def log(ss):

    # 绝对路径
    abs_path = os.path.abspath('.')

    path = abs_path + '/' + '暂时爬取到的数据/logs.txt'
    my_io.log(ss,path)

    print(ss)


###############################################################
'''
向csv文件中写入数据,超过50条就存储
如果config == 1,全部存储
否则超过50条就存储
'''
def write_data(microblogs,path,config):

    if config == 1: # 全部存储
        my_io.write_csv(path,microblogs)
        microblogs.clear()
        info = '写入剩余数据成功'
        log(info)
    else: # 满50条才存储
        if len(microblogs) > 50:
            my_io.write_csv(path,microblogs)
            microblogs.clear()
            info = '写入50条数据成功'
            log(info)

    return microblogs

###############################################################
'''
爬取网页失败，进行第二次尝试
'''
def next_try_downloadhtml(url):

    time_delay = 30 #* 6 # 6分钟后进行第二次尝试
    time.sleep(time_delay)

    # 获取原网页
    html_source = downloadHtml(url)

    return html_source


###############################################################

'''
# 按照日期进行爬取
'''
def crawl_as_days(dayslist,keyword,path,sleep_time_shangjie,sleep_time_xiajie,rand):

    ## 如果是断点续爬，那么就不用在这里初始化
    # attrs = ['昵称','性别','所在地','时间','内容','点赞数','转发数','评论数','主页']
    # my_io.init_csv(path,attrs)

    for day in dayslist:

        first_url = set_first_url(keyword, day, day,rand)

        # 爬取第一个页面
        # 打印出url，方便分析
        info = "首页url: \n" + first_url
        log(info)

        # 获取原网页
        html_source = downloadHtml(first_url) 
        if html_source == -1:# 爬取失败
            info = "-------------首页爬取失败，正在尝试第二次爬取-------------"
            log(info)
            try_times = 3  # 尝试爬取三次
            while try_times > 0:
                try_times = try_times - 1
                html_source = next_try_downloadhtml(first_url)
                if html_source == -1:
                    continue
                else: # 第二次爬取尝试成功
                    info = "-------------尝试再次爬取成功-------------"
                    log(info)
                    break

            if try_times == 0: # 爬取失败了
                info = '尝试三次后爬取失败，退出程序'
                log(info)
                sys.exit()
        else: # 首页爬取成功
            pass

        # 修补网页
        fixed_html = fix_html(html_source)

        microblogs =  []
        # 解析第一页的内容
        microblog_quene, result,allpage = parse_main_content(fixed_html)

        # 合并爬取到的BLOG
        microblogs = microblogs + microblog_quene

        if result == 'dayover': # 说明只有一页，存储完继续下一天的爬取
            write_data(microblogs,path,1)
            continue # 接着爬取下一天的

        # 满50条就存储
        write_data(microblogs,path,2)

        old_nextpage = 1

        error_count = 1 # 如果爬取的页面一直有问题，说明可能下一页不是正常的页面，所以我们要及时跳出来

        nextpage = result
        ##############################################################
        # 开始爬取 第 n 页  n >= 2
        while True:
            # 由于第一个页面没有明确的下一页的url，所以还是在浏览器中测试，然后，找到下一页的规律
            # 下面的链接，nextpage是重点，其他和之前的没啥区别

            '''
            1、dayover 爬取结束，该天爬取结束         'dayover'
            2、next_page            整型
            3、爬取失败，重新爬取     'nexttry'
            4、exit 退出程序
            '''
            next_url = set_next_url(keyword, day, day, nextpage)

            info = '\n\n------------第 ' + str(nextpage) +  ' 页'  +  ' // 总页数: ' + str(allpage) +'-------------- \n\n'
            log(info)
            info = 'next_url ： \n' + next_url + '\n\n'
            log(info)

            html_source = downloadHtml(next_url)

            # 爬取失败
            if html_source == -1:
                info = "-------------爬取失败 顺序页爬取失败-------------"
                log(info)
                try_times = 3  # 尝试爬取三次
                while try_times > 0:
                    try_times = try_times - 1
                    html_source = next_try_downloadhtml(next_url)
                    if html_source == -1:
                        continue
                    else: # 第二次爬取尝试成功
                        info = "-------------尝试再次爬取成功-------------"
                        log(info)
                        break

                if try_times == 0: # 爬取失败了
                    info = '尝试三次后爬取失败,遇到反爬虫'
                    log(info)
                    # saved_url = first_url
                    sys.exit()


            fixed_html = fix_html(html_source)
            microblog_quene, result, allpage = parse_main_content(fixed_html)

            if result == 'exit': # 遇到爬虫
                info = "-------------遇到反爬虫-------------"
                log(info)
                sys.exit()

            if result == 'nexttry': # 爬取的网页哟问题，需要重新爬取
                error_count = error_count + 1 
                if error_count == 6: # 尝试六次后，依旧有问题，说明可能爬到了不是想要的页面
                    error_count = 0
                    break
                else:
                    nextpage = old_nextpage
                    continue

            if result == 'dayover': # 一天的内容已经爬取完成
                break

            nextpage = result

            microblogs = microblogs + microblog_quene

            # 如果nextpage有效，就存储nextpage，用来防止nextpage无效时
            old_nextpage = nextpage

            # 满50条就存储
            write_data(microblogs,path,2)

            # 延时，防止被反爬虫，这个时间需要不断测试，达到一个平衡点
            sleep_time = random.randint(sleep_time_xiajie,sleep_time_shangjie)
            time.sleep(sleep_time)

        # 爬完一天的数据，进行一次存储
        write_data(microblogs,path,1)


if __name__ == "__main__":

    # url Demo
    # https://weibo.cn/search/mblog?hideSearchFrame=&keyword=%E5%8D%8E%E4%B8%BA&advancedfilter=1&starttime=20180501&endtime=20180501&sort=time&page=8

    keyword = "红卫兵"
    abs_path = os.path.abspath('.')
    path = abs_path +'/红卫兵/' + keyword + '2013-2014.csv'
    startday = '20140910'
    endday = '20200930'
    dayslist = tools.get_day_list(startday, endday)

    sleep_time_shangjie = 3
    sleep_time_xiajie = 1
    rand = 6724 # rand是一个随机数
    crawl_as_days(dayslist,keyword,path,sleep_time_shangjie,sleep_time_xiajie,rand)