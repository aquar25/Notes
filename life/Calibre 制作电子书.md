####Calibre 制作电子书

Calibre支持使用Python语言编写脚本，抓取网页内容生成电子书，默认为mobi格式

1. 在抓取新闻的下拉菜单中选择添加自定义新闻源
2. New Recipe---切换到高级模式，默认提供了代码模板，只需要添加自定义的网页来源
3. 编写Recipe文件代码
4. 抓取新闻，选择自定义来源，下载即可


```
#!/usr/bin/env python
# vim:fileencoding=utf-8
from __future__ import unicode_literals, division, absolute_import, print_function
from calibre.web.feeds.news import BasicNewsRecipe

class liaoxuefeng_python(BasicNewsRecipe):
	'''自定义的Recipe都继承自Calibre提供的基类BasicNewsRecipe，必须实现parse_index()方法
	'''
	#电子书名称
    title          = '廖雪峰Python教程3'
    description = 'python教程'
    max_articles_per_feed = 200
    # 设置每隔1s下载一个章节，默认值为0，当网络不好时，可以把这个值调大点
    delay = 1   
    url_prefix = 'http://www.liaoxuefeng.com'
    no_stylesheets = True
    #抓取每一个页面中保留的tag
    keep_only_tags = [{ 'class': 'x-content' }]
    #页面中删除的Tag
    remove_tags=[{'class':'x-wiki-info'}]
    #指定Tag之后的元素都被删除
    remove_tags_after=[{'class':'x-wiki-content'}]
    
    def get_title(self, link):
        return link.contents[0].strip()
    
    def parse_index(self):
    	#index_to_soup()由BasicNewsRecipe实现，使用Beautifulsoup抓取一个网址，并获得这个网页内容的soup对象
        soup = self.index_to_soup('http://www.liaoxuefeng.com/wiki/0014316089557264a6b348958f449949df42a6d3a2e542c000')
 		# 左侧导航栏
        div = soup.find('div', { 'class': 'x-sidebar-left-content' })
 		# 找到每一个章节的标题和对应的URL，Calibre会下载每一个URL的html，使用上面的类属性进行解析
        articles = []
        for link in div.findAll('a'):
            til = self.get_title(link)
            url = self.url_prefix + link['href']
            a = { 'title': til, 'url': url }
 
            articles.append(a)
 		#返回一个列表，这个列表中是多个元组，每个元组是书的一卷('廖雪峰python教程', articles)，每一卷中又有多个章节articles
        tutorial = [('廖雪峰python教程', articles)]
 
        return tutorial

```

参考：
[用calibre和python制作电子书---Python和Git教程](http://www.cnblogs.com/ckzhou/p/4162835.html)