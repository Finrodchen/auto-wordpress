import urllib.request as req
import bs4
import re


url = "https://tsscosecurities.blogspot.com/2020/07/Global-Stock-20200731.html"


request = req.Request(url, headers = {
    "User-Agent":"Mozilla/5.0 (Windows; U; Windows NT 6.1; zh-CN; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15" #到網頁 → F12 → Network → 通常是最上面的那個 → Headers → Request Headers → user-agent
})

with req.urlopen(request) as response:
    data = response.read().decode("utf-8")

root = bs4.BeautifulSoup(data, "html.parser") 
body = root.find("div", class_= "post-body entry-content")
tags = body.find_all(["ul", "li", "h3"])
old_post = root.find("div", class_= "blog-pager")
old_post_link = old_post.find_all(["a"], limit=1, href = re.compile('https'))

# print(root.title.string)
# print()
# print(tags)

print(old_post_link)
