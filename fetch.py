# -*- coding: utf8 -*-
import http.cookiejar
#import urllib.request
import urllib
import json
from operator import attrgetter

url_hp = "https://www.hornbach.de"
url_products = "https://www.hornbach.de/mvc/sellout/load-search-results/m.json?_=1506789419698"
post_data = '{"categoryPath":"","pageNumber":0,"pageSize":500,"sortOrder":"sortModePriceAsc","searchVersion":2,"filters":[]}'

url_market = "https://www.hornbach.de/mvc/market/current-market?_=1486416807490"



# markets cj._cookies['www.hornbach.de']['/']['hbMarketCookie'].value
# ulm 631
# neu ulm 536
values = {
"categoryPath": "",
"pageNumber": 2,
"pageSize": 72,
"sortOrder": "sortModePriceDesc",
"searchVersion": 2,
"filters": []
}




class ChangeTypeProcessor(urllib.request.BaseHandler):
    def https_request(self, req):
        req.unredirected_hdrs["Content-type"] = "application/json;charset=utf-8"
        req.unredirected_hdrs["User-Agent"] = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0"
        
        return req


class Article:
    code = 0
    title = ''
    price_display = 0
    img_url = ''
    link = ''
    def __str__(self):
        return self.code + " " + self.title
    def __repr__(self):
        return repr((self.name, self.grade, self.age))
    
article_db = []
    
cj = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
opener.add_handler(ChangeTypeProcessor())

opener.addheaders.append(('Referer', 'https://www.hornbach.de/shop/raus-damit/artikelliste.html?rd=m'))

# Cookie(version, name, value, port, port_specified, domain,
# domain_specified, domain_initial_dot, path, path_specified,
# secure, expires, discard, comment, comment_url, rest, rfc2109=False)
#c_conf = cookielib.Cookie(0, 'CookieConfirmation', 'confirmed', None, False, 'www.hornbach.de', False, False, '/', True, False, 3634071505, False, None, None, None, False)
#c_en   = cookielib.Cookie(0, 'cookiesEnabled', '1486588229862', None, False, 'www.hornbach.de', False, False, '/', True, False, 3634071505, False, None, None, None, False)


# WORKING: set market cookie for ulm
c_hbmark = http.cookiejar.Cookie(0, 'hbMarketCookie', '631', None, False, 'www.hornbach.de', False, False, '/', True, True, 3634071505, False, None, None, None, False)
cj.set_cookie(c_hbmark)
# show market id:
#print (cj._cookies['www.hornbach.de']['/']['hbMarketCookie'])

#print opener.open(url_products).read()

title_old = ''
for i in range(1,14):
    post_data = '{"categoryPath":"","pageNumber":'+str(i)+',"pageSize":72,"sortOrder":"sortModePriceAsc","searchVersion":2,"filters":[]}'
    try:
        response = opener.open(url_products, bytearray(post_data,'utf-8'))
    except urllib.error.HTTPError as er:
        print(er.hdrs)
    products_json = response.read().decode('utf8')
    #print products_json
    products_data = json.loads(products_json)
    for article in products_data['articles']:
        art = Article()    
        art.code = article['articleCode']
        art.title = article['title']
        art.price_display = int(article['allPrices']['displayPrice']['price'].replace(',',''))
        art.img_url = article['imageUrl']
        art.link = article['localizedExternalArticleLink']
        article_db.append(art)
        
article_db_sort = sorted(article_db, key=attrgetter('price_display', 'title'))

for art in article_db_sort:
    if (title_old[0:5] == art.title[0:5]):
        br = ""
    else:
        br = "<br>"
    title_old = art.title
    print(br+"<a target='_blank' href='http://www.hornbach.de/"+art.link+"?rd=m'><img src='http://www.hornbach.de/"+ art.img_url+"'> "+str(art.price_display)+"E </a>\r\n")
