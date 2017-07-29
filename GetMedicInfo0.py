import lxml
import xlwt
import requests
from lxml import etree
import time

url_root = "https://www.315jiage.cn/x-ChangWei/"
home_page = "https://www.315jiage.cn/"
page_brief = ""
t0 = time.time()
print("起始时间",t0)

def getRequest(url):
    """
    try to get the page at most 10 times
    'except' block :if the exception occurs 
    'else' block: if no exception occurs
    """
    for x in range(10):
        try:
            r = requests.get(url)
        except:
            continue
        else:
            break
    return r

def getPageBrief(cur_url):
    content_list = []
    next_page_url = ""
    try:
        r = getRequest(cur_url)
        r.encoding = 'utf-8'
        html = etree.HTML(r.text)
        tmpl = html.xpath("//div[@class='title text-oneline']/a/@href")
        # last() means the last attribution
        next_addr = html.xpath("//div[@class='pager']//li[last()-1]/a")[0].attrib["href"][3:]
    except:
        print("It is the last page")
        next_addr = ""
        tmpl = []
    finally:
        next_page_url = home_page + next_addr
        print(next_page_url)
        content_list = map(lambda x:home_page+x[3:],tmpl)
        return content_list, next_page_url

def getContent(url):
    details_list = []
    try:
        r = getRequest(url)
        r.encoding = 'utf-8'
        html = etree.HTML(r.text)
        tmpl = html.xpath("//div[@id='content']//u")
        for x in tmpl:
#            print(x.xpath("string(.)"))
            details_list.append(x.xpath("string(.)"))

# .xpath("string(.)") to get the whole content in the tag, ignoring the effect of the sub tag
# if there exsit at least two properties, and operator allows you to combine them. for example: "//div[@id='content and @class='button']"
# Search XPath rules tosee more details
        details_list.append(html.xpath("//div[@id='content']/p[last()]")[0].xpath("string(.)"))
        details_list.append(html.xpath("//div[@id='tab1']")[0].xpath("string(.)"))
    except:
        print("error ocoured",url)
    return details_list

xls_content = []
cur_page_url = url_root
while True:
    content_list,next_page_url = getPageBrief(cur_page_url)
    for x in content_list:
        xls_content.append(getContent(x))
    if len(next_page_url) > len(home_page):
        cur_page_url = next_page_url
    else:
        print("over")
        break

#写入至xls文件中
#style0 = xlwt.easyxf('font: name Times New Roman, color-index red, bold on', num_format_str='#,##0.00')
wb = xlwt.Workbook()
ws = wb.add_sheet("test1")
for row_index,row in enumerate(xls_content):
    for col_index,col in enumerate(row):
        ws.write(row_index,col_index,col)

wb.save(url_root.split('/')[-2]+".xls")
print("Saved successed! 共用时：",time.time() - t0)
