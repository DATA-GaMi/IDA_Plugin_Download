import json

import requests
import urllib3
#import simplejson as json
from lxml import etree
from pygments import highlight, lexers, formatters

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

plugin_group = {}
plugin_list = []
plugin_items = ("id", "title", "description", "download_url")
plugin_items = dict.fromkeys(plugin_items)
response = requests.get('https://github.com/onethawt/idaplugins-list')

selector = etree.HTML(response.text)

plugin_title = selector.xpath("//html/body/div[1]/div[4]/div/main/turbo-frame/div/div/div/div[2]/div["
                              "1]/readme-toc/div/div[2]/article/ul[2]/li//a/text()")

plugin_description = selector.xpath("//html/body/div[1]/div[4]/div/main/turbo-frame/div/div/div/div[2]/div["
                                    "1]/readme-toc/div/div[2]/article/ul[2]//p/text()")

plugin_url = selector.xpath(
    "//html/body/div[1]/div[4]/div/main/turbo-frame/div/div/div/div[2]/div[1]/readme-toc/div/div["
    "2]/article/ul[2]/li//@href")

for i in range(0, len(plugin_title)):
    plugin_items['id'] = str(i)
    plugin_items['title'] = str(plugin_title[i])
    plugin_items['description'] = str(plugin_description[i-1]).replace(':', '')
    plugin_items['download_url'] = str(plugin_url[i])

    plugin_list.append(plugin_items)
    plugin_items = dict.fromkeys(plugin_items)


with open('ida_plugin.json', 'w') as f:
    print(json.dumps(plugin_list, indent=4), file=f)
