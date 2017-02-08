import cookielib
import urllib2
import urllib


url_hp = "http://www.hornbach.de"
url_products = "http://www.hornbach.de/mvc/sellout/load-search-results/m.json?_=1486415327126"
post_data = '{"categoryPath":"","pageNumber":2,"pageSize":72,"sortOrder":"sortModePriceDesc","searchVersion":2,"filters":[]}'

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




class ChangeTypeProcessor(urllib2.BaseHandler):
    def http_request(self, req):
        req.unredirected_hdrs["Content-type"] = "application/json;charset=utf-8"
        req.unredirected_hdrs["User-Agent"] = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0"
        
        return req
        


cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
opener.add_handler(ChangeTypeProcessor())

opener.addheaders.append(('Referer', 'http://www.hornbach.de/shop/raus-damit/artikelliste.html?rd=m'))



#market
print opener.open(url_market).read()
cj._cookies['www.hornbach.de']['/']['hbMarketCookie'].value = '631'
print cj._cookies
print opener.open(url_market).read()
print cj._cookies['www.hornbach.de']['/']['hbMarketCookie'].value

#print opener.open(url_products).read()

#opener.open(url_hp)

#print opener.open(url_products, post_data).read()

