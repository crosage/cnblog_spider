import asyncio

from bs4 import BeautifulSoup
import aiohttp
import aiofiles

path=""
user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.50"
cookies={
    ".CNBlogsCookie":"your cookie",
    ".Cnblogs.AspNetCore.Cookies":"your cookie"
}
prefix="https://www.cnblogs.com/znsbc-13/p/"
async def cnblogs_content(urls:[]):
    index:int=0
    async with aiohttp.ClientSession() as session:
        for url in urls:
            index = index + 1
            try:
                async with session.get(url=url) as resp:
                    if resp.status==200:
                        _bytes=await resp.text()
                        soup=BeautifulSoup(_bytes,features="html.parser")
                        body=soup.find("div",id="cnblogs_post_body")
                        head=soup.find("a",id="cb_post_title_url").get_text()
                        print(f"正在处理第{index}篇博文")
                        async with aiofiles.open(path+str(index)+".html","w",encoding="utf-8") as file:
                            await file.write(str(body))
            except:
                print(f"处理第{index}出现问题 url为{url}")

async def geturls():
    url="https://i.cnblogs.com/api/posts/list"
    urls=[]
    async with aiohttp.ClientSession() as session:
        pages=10000
        for _index in range(1,pages):
            params = {
                "p": _index,
                "t": 1,
                "cfg": 0
            }
            async with session.get(url=url,params=params,cookies=cookies,proxy="http://localhost:7890") as resp:
                _json=await resp.json()
                counts=int(_json["postsCount"])
                pageSize=int(_json["pageSize"])
                for i in _json["postList"]:
                    urls.append(prefix+str(i["id"])+".html")
                if pageSize*_index>=counts:
                    break
    print(f"共{len(urls)}篇博文")
    await cnblogs_content(urls)
path=input("输入要保存的文件路径\n")
asyncio.run(geturls())