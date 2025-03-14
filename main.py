import requests
from bs4 import BeautifulSoup
import html2text
import os

path = "D:\\myblog\\tmp\\"
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.50"
cookies = {
    ".CNBlogsCookie": " ",
    ".Cnblogs.AspNetCore.Cookies": " ",
}
prefix = "https://www.cnblogs.com/znsbc-13/p/"

def cnblogs_content(urls):
    index = 0
    session = requests.Session()
    for url in urls:
        index += 1
        try:
            resp = session.get(url=url,proxies={"http": "http://localhost:7890", "https": "http://localhost:7890"})
            if resp.status_code == 200:
                soup = BeautifulSoup(resp.text, features="html.parser")
                body = soup.find("div", id="cnblogs_post_body")
                title = soup.find("a", id="cb_post_title_url").get_text().strip()
                date_element = soup.find("a", id="cb_post_title_url")
                date_title = date_element.get('title').replace("发布于", "")
                print(f"正在处理第{index}篇博文 标题为{title} 发布时间{date_title}")
                title=title.replace("/", "_")
                title=title.replace("\\", "_")
                h = html2text.HTML2Text()
                markdown_content = h.handle(str(body))
                markdown_content = f"---\ntitle: {title}\n---\n\n归档于 {date_title}\n\n{markdown_content}\n\n"
                with open(os.path.join(path, title + ".md"), "w", encoding="utf-8") as file:
                    file.write(markdown_content)
        except Exception as e:
            print(f"处理第{index}出现问题 url为{url}, 错误信息：{e}")

def geturls():
    url = "https://i.cnblogs.com/api/posts/list"
    urls = []
    session = requests.Session()
    pages = 10000
    for _index in range(1, pages):
        params = {
            "p": _index,
            "t": 1,
            "cfg": 0,
        }
        resp = session.get(url=url, params=params, cookies=cookies,proxies={"http": "http://127.0.0.1:7890", "https": "http://127.0.0.1:7890"})
        _json = resp.json()
        counts = int(_json["postsCount"])
        pageSize = int(_json["pageSize"])
        for i in _json["postList"]:
            urls.append(prefix + str(i["id"]) + ".html")
        if pageSize * _index >= counts:
            break
    print(f"共{len(urls)}篇博文")
    urls.reverse()
    cnblogs_content(urls)

path = "D:\\myblog\\tmp\\"
geturls()
