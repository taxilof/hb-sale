# -*- coding: utf8 -*-
import http.cookiejar
#import urllib.request
import urllib
import json


url_hp = "http://www.hornbach.de"
url_products = "http://www.hornbach.de/mvc/sellout/load-search-results/m.json?_=1486415327126"
post_data = '{"categoryPath":"","pageNumber":0,"pageSize":500,"sortOrder":"sortModePriceAsc","searchVersion":2,"filters":[]}'

url_market = "http://www.hornbach.de/mvc/market/current-market?_=1486416807490"



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
    def http_request(self, req):
        req.unredirected_hdrs["Content-type"] = "application/json;charset=utf-8"
        req.unredirected_hdrs["User-Agent"] = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0"
        
        return req


class Article:
    code = 0
    title = ''
    price_display = ''
    img_url = ''
    link = ''
    def __str__(self):
        return self.code + " " + self.title
    
article_db = []
    
cj = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
opener.add_handler(ChangeTypeProcessor())

opener.addheaders.append(('Referer', 'http://www.hornbach.de/shop/raus-damit/artikelliste.html?rd=m'))

# Cookie(version, name, value, port, port_specified, domain,
# domain_specified, domain_initial_dot, path, path_specified,
# secure, expires, discard, comment, comment_url, rest, rfc2109=False)
#c_conf = cookielib.Cookie(0, 'CookieConfirmation', 'confirmed', None, False, 'www.hornbach.de', False, False, '/', True, False, 3634071505, False, None, None, None, False)
#c_en   = cookielib.Cookie(0, 'cookiesEnabled', '1486588229862', None, False, 'www.hornbach.de', False, False, '/', True, False, 3634071505, False, None, None, None, False)


# WORKING: set market cookie for ulm
c_hbmark = http.cookiejar.Cookie(0, 'hbMarketCookie', '631', None, False, 'www.hornbach.de', False, False, '/', True, False, 3634071505, False, None, None, None, False)
cj.set_cookie(c_hbmark)
# show market id:
# print cj._cookies['www.hornbach.de']['/']['hbMarketCookie'].value

#print opener.open(url_products).read()

#opener.open(url_hp)
title_old = ''
for i in range(1,13):
    post_data = '{"categoryPath":"","pageNumber":'+str(i)+',"pageSize":500,"sortOrder":"sortModePriceAsc","searchVersion":2,"filters":[]}'
    response = opener.open(url_products, bytearray(post_data,'utf-8'))
    products_json = response.read().decode('utf8')
    #print products_json
    products_data = json.loads(products_json)
    for article in products_data['articles']:
        code = article['articleCode']
        title = article['title']
        price = article['allPrices']['displayPrice']['price']
        img_url = article['imageUrl']
        link = article['localizedExternalArticleLink']
        #print  title + ": " + price + " " + link
        if (title_old[0:5] == title[0:5]):
            br = ""
        else:
            br = "<br>"
        title_old = title
        print(br+"<a target='_blank' href='http://www.hornbach.de/"+link+"?rd=m'><img src='http://www.hornbach.de/"+ img_url+"'> "+price+"E </a>")
        
        art = Article()
        art.code = code
        art.title = title
        art.img_url = img_url
        article_db.append(art)
        

