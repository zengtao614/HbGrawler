
"""
    规范性写法(创建类)
"""

import os
import requests
import re


"""抓取花瓣网指定页面图片https://huaban.com/boards/18976743"""
class HbImagecrawler():
    def __init__(self,mysterious_code=18976743):
        """
        :param mysterious_code: 传入url指定值,默认为18976743
            初始化对象：
        1.创建文件夹用于存放图片
        2.初始化属性
        """
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
        }
        self.mysterious_code = mysterious_code
        self.url = "https://huaban.com/boards/"+str(mysterious_code)
        self.path_name = "C:\\Users\\曾涛\\Desktop\\HbImage"
        self.imgNum = 0
        self.page = 1
        if not os.path.exists(self.path_name):
            os.mkdir(self.path_name)
            print("创建文件夹成功")

    def grabHtml(self,url):
        """
        此方法获取传入的url的网页内容
        :param url: 传入的url地址
        :return: 返回该网页的html内容
        """
        request = requests.get(url,self.headers)
        html = request.content
        return html

    def grabSrcUrl(self,maxNum=100,page=1):
        """
        使用正则找出图片的url路径
        :param maxNum: 下载图片的最大数,默认为100
        :param page: 从第多少页开始爬，默认为1(即第一页)
        :return:
        """
        origin_html = self.grabHtml(self.url).decode("utf-8")
        # 获取app.page["board"]下面的内容
        board_html = re.compile(r'app\.page\["board"\].*').search(origin_html).group()
        # print(board_html)
        # 获取所有file":{}的内容,并把得到的列表转成字符串
        files_html = "".join(re.compile(r'"file":{.*?}').findall(board_html))
        # print(files_html)
        # 获取file下的key值（即图片的url值）
        src_keys = re.compile(r'"key":".*?"').findall(files_html)
        # print(len(src_keys))
        # 获取图片的pin_id，图片介绍url
        src_pins = re.compile(r'"pin_id":[\d]+').findall(board_html)
        # 转成数组类型且不包含重复值
        src_pins_list = []
        for src_pin in src_pins:
            if src_pin not in src_pins_list:
                src_pins_list.append(src_pin)
        # print(len(src_pins_list))
        # 判断当前页数是否大于等于设置的阈值页数
        if self.page >= page:
            for src_key,src_pin in zip(src_keys,src_pins_list):
                src_name = src_pin[9:]+"_"+src_key[7:-1]+".jpg"
                # 此链接图片文件大小更小，效率更高：http://hbimg.huabanimg.com/8bf827dc51f08d1cd3c0e25c5506b3a33e02a2b018152f-FIn34u_fw658
                # 此链接图片文件大小更大，图片更清晰(不确定)：http://img.hb.aicdn.com//8bf827dc51f08d1cd3c0e25c5506b3a33e02a2b018152f-FIn34u_fw658
                src_url = "http://hbimg.huabanimg.com/"+src_key[7:-1]
                # 设置图片下载数的阈值，超过则不再下载
                if self.imgNum == maxNum:
                    print("已经下了"+str(maxNum)+"张图，达到阈值，退出")
                    exit()
                self.downloadImg(src_name,src_url)
                self.imgNum+=1
        try:
            self.url = "https://huaban.com/boards/"+str(self.mysterious_code)+"/?max="+src_pins[-1][9:]
        except:
            print("请求页面为空,一共下了"+str(self.imgNum)+"张图")
        else:
            self.grabSrcUrl(maxNum)
            self.page+=1

    def downloadImg(self,src_name,src_url):
        """
        传入图片的名称和url地址下载该图片
        :param src_name: 图片名（文件的路径：绝对路径或相对路径）
        :param src_url: 图片的url值
        :return:
        """
        with open(self.path_name+"\\"+src_name,"wb") as fp:
            fp.write(self.grabHtml(src_url))
            print(src_name+"下载成功")

if __name__ == '__main__':
    crawler = HbImagecrawler(mysterious_code=45991946)
    # 设置最大爬取的图片数为40，爬取的起始页数为5
    crawler.grabSrcUrl(maxNum=200)