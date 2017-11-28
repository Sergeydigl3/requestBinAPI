from bs4 import BeautifulSoup
import json,traceback,requests,time

class TargetException(Exception):
    def __init__(self, msg):
        self.msg = msg
    def __str__(self):
        return self.msg

class PollingException(Exception):
    def __init__(self, msg):
        self.msg = msg
    def __str__(self):
        return self.msg

class Request:
    def __init__(self, link):
        self.link = link
        self.last=[]
        self.now=[]
        self.__start_polling=False
        self.on_update_target=None
        self.r=requests.Session()
        self.r.headers= {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'}

    def on_update(self, fn):
        self.on_update_target=fn

    def check(self, save_result=False):
        self.now=[]
        self.__html=self.r.get(self.link).text
        self.__soup=BeautifulSoup(self.__html, 'lxml')
        self.__soup=self.__soup.find_all('div', {'class': 'message-wrapper'})
        for i in self.__soup:
            self.now.append({'Form/Post':{}, 'QueryString':{},'Headers': {}})
            i=i.find('div', {'class': 'request-detail'})
            self.__temp_span_4= str(i.find('div', {'class': 'span4'}))
            self.__temp_raw_body=str(i.find('pre', {'class': 'body prettyprint'}))
            self.__temp_span_8=i.find('div', {'class': 'span8'}).find_all('p',{'class':'keypair'})
            if '<h5>QUERYSTRING</h5>\n' in self.__temp_span_4:
                self.__queryraw=self.__temp_span_4.split('<h5>QUERYSTRING</h5>\n')[1]
                self.__queryraw=self.__queryraw[:len(self.__queryraw)-6]\
                    .replace('<p class="keypair"><strong>','')\
                    .split('</p>\n')
                self.__queryraw.pop()
                for i in range(len(self.__queryraw)): self.__queryraw[i]=self.__queryraw[i].split(':</strong> ')
                for i in self.__queryraw:self.now[len(self.now)-1]['QueryString'].update({i[0]:i[1]})
            if not '<div class="span4">\n<h5>FORM/POST PARAMETERS</h5>\n<em>None</em>' in self.__temp_span_4:
                self.__temp_raw_body=self.__temp_raw_body[:len(self.__temp_raw_body)-6].replace('<pre class="body prettyprint">','').split('&amp;')
                for i in range(len(self.__temp_raw_body)): self.__temp_raw_body[i]=self.__temp_raw_body[i].split('=')
                for i in self.__temp_raw_body: self.now[len(self.now) - 1]['Form/Post'].update({i[0]: i[1]})
            for i in self.__temp_span_8:
                d=[str(i.contents[0]).replace('<strong>','').replace(':</strong>',''), str(i.contents[1]).strip()]
                self.now[len(self.now) - 1]['Headers'].update({d[0]: d[1]})
        self.now=json.loads(json.dumps(self.now,ensure_ascii=False))
        if save_result:self.last=self.now
        return self.now



    def polling(self, none_stop=False, delay=5):
        if self.__start_polling==True: raise PollingException("Polling already started")
        if self.on_update_target==None: raise TargetException("Target not found")
        else:
            if none_stop:
                while True:
                    try:
                        self.check()
                        if len(self.now)!=len(self.last):
                            if len(self.last)==0:
                                self.on_update_target(self.last, self.now)
                                self.last = self.now
                            else:
                                if self.last[len(self.last)-1]!=self.now[len(self.now)-1]:
                                    self.on_update_target(self.last, self.now)
                                    self.last=self.now
                    except BaseException: print(traceback.format_exc())
                    time.sleep(delay)
            else:
                try:
                    while True:
                        self.check(save_result=False)
                        if self.now != self.last:
                            if len(self.last)==0:
                                self.on_update_target(self.last, self.now, self.now[0])
                                self.last = self.now
                            else:
                                if self.last and self.now and self.last[0]!=self.now[0]:self.on_update_target(self.last, self.now, self.now[0])
                                self.last = self.now
                        time.sleep(delay)
                except BaseException:
                    print(traceback.format_exc())
                    self.__start_polling=False
