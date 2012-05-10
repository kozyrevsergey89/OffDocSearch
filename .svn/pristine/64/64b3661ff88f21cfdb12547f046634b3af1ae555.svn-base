'''
Created on Apr 14, 2012

@author: Sergii Kozyrev
'''
'''
how to use web_crawler class:


instantiate new instance (wc) of web crawler

call wc.crawl_web(arg) - it will generate index in wc; arg is profile you SHOULD choose between 'dev' and 'itpro' for now

now you can call wc.lookup('string to lookup') - as an output you will get a list
'''


import urllib
import socket
socket.setdefaulttimeout(10)
# in a true webcrawler you should not use re instead use a DOM parser
import re
# for sorting a nested list
from operator import itemgetter

'''
'    Class for crawling the web
'''
    
class WebCrawler(object):
 
    

    def __init__(self, graph = {}):
        #self.crawled=crawled
        
        self.graph=graph
             
        
    '''
    'Getting page from given url
    '''    
        
    
    def get_page(self, url):
            try:
                f = urllib.urlopen(url)
                page = f.read()
                f.close()
                return page
            except:
                return ""
            return ""
    '''
    'Getting url from page. Outputs url and 
    ''' 
    
    def get_next_target(self, page):
            start_link = page.find('<a href=')
            if start_link == -1:
                return None, 0
            start_quote = page.find('"', start_link)
            end_quote = page.find('"', start_quote + 1)
            url = page[start_quote + 1:end_quote]
            return url, end_quote
    
    '''
    'Union of two lists. Outputs number of added elemants.
    '''
        
    def union(self, p,q):
            cnt = 0
            for e in q:
                if e not in p:
                    p.append(e)
                    cnt += 1
            return cnt
       
    '''
    'Getting list of all links on page
    '''
        
    def get_all_links(self, page):
            links = []
            while True:
                url,endpos = self.get_next_target(page)
                if url:
                    links.append(url)
                    page = page[endpos:]
                else:
                    break
            return links
        
    '''
    'Adding pages to index
    '''    
        
    def add_to_index(self,index, keyword,url):
            if keyword in index:
                if url not in index[keyword]:
                    index[keyword].append(url)
            else:
                index[keyword] = [url]
                
    def split_string(self, source,splitlist):
        return ''.join([ w if w not in splitlist else ' ' for w in source]).split()
    
    '''
    'Parsing words on page
    '''
    
    def add_page_to_index_re(self, index, url,content):
            i = 0
            # it is not a good idea to use regular expression to parse html
            # i did this just to give a quick and dirty result
            # to parse html pages in practice you should use a DOM parser
            regex = re.compile('(?<!script)[>](?![\s\#\'-<]).+?[<]')
    
            for words in regex.findall(content):
                word_list = self.split_string(words, """ ,"!-.()<>[]{};:?!-=`&""")
                for word in word_list:
                    self.add_to_index(index,word,url)
                    i += 1
            return i
    
    '''
    'Formatting short urls to appropriate format
    '''    
        
    def format_url(self, root,page):
            if page[0] == '/':
                return root + page
            return page
    
    '''
    'Before crawling every new url we check if this url is in ckecked profile 
    '''
    
    def trim_to_profile(self, page, list_to_trim):
        for e in list_to_trim:
            if page[:len(e)]== e or page[0]=='/':
                return True
        return False
    
    '''
    'Crawling the web.
    'Here we have two profiles: 'dev' for developers and 'itpro' for IT Professionals.
    'So each time we call tocrawl.pop() we chek if we have gone beyond our profiles' seeds.
    'This method is returning index in form of dictionary {keyword:[list of urls]}.
    'As mentioned above we have two profiles.
    'So we should call crawl_web twice to generate index for each profile.
    'We can provide first argument for this method to specify appropriate profile.
    'Also in this method we have very important side effect - we are generating graph dictionary.
    '''
    
    def crawl_web(self,  arg='dev', max_pages=19,max_depth=5):
            #Here we work with profiles
            profiles={'dev':['http://stackoverflow.com', 'http://developer.android.com'], 'itpro':['http://technet.microsoft.com']}
            tocrawl=[]
            index={}
            depth=[]
            crawled = []
            for e in profiles[arg]:
                tocrawl.append(e)
                depth.append(0)
            while tocrawl and len(crawled) < max_pages:
                page = tocrawl.pop()
                d = depth.pop()
                if page not in crawled and (self.trim_to_profile(page, profiles[arg])):
                    for root in profiles[arg]:
                        page = self.format_url(root,page)
                    content = self.get_page(page)
                    success = self.add_page_to_index_re(index, page,content)
                    outlinks = self.get_all_links(content)
                    self.graph[page] = outlinks
                    if not d == max_depth:
                        cnt = self.union(tocrawl,outlinks)
                        for i in range(cnt):
                            depth.append(d+1)
                    crawled.append(page)
            return index
        
    '''
    'Method to lookup without ranks consideration.
    '''
                
    def lookup(self, index, keyword):
            if keyword in index:
                return index[keyword]
            return None
        
    '''
    'Sorting results
    '''    
        
    def sort_by_score(self, l):
            get_score = itemgetter(0)
            map(get_score,l)
            l = sorted(l,key=get_score)
            l.reverse()
            return l
        
    '''
    'Method to lookup a keyword in index considering ranks.
    'Outputs list of links.
    '''    
        
    def lookup_best(self, index,  keyword, ranks):
            result = []
            result_without_ranks = []
            if keyword in index:
                for url in index[keyword]:
                    if url in ranks:
                        result.append([ranks[url], url])
            if len(result) > 0:
                result = self.sort_by_score(result)
                for e in result:
                    result_without_ranks.append(e[1])
            return result_without_ranks
        
    '''
    'Getting inlinks for each link in graph
    '''    
        
    def get_inlinks(self, page):
            il = {}
            for p in self.graph:
                for ol in self.graph[p]:
                    if ol == page:
                        il[p] = self.graph[p]
            return il
        
    '''
    'Computing ranks 
    '''    
        
    def compute_ranks(self):
            d = 0.8 # damping factor
            numloops = 10
            ranks = {}
            npages = len(self.graph)
            for page in self.graph:
                ranks[page] = 1.0 / npages
            for i in range(0, numloops):
                newranks = {}
                for page in self.graph:
                    newrank = (1 - d) / npages
                    inlinks = self.get_inlinks(page)
                    for il in inlinks:
                        newrank += ((0.8 * ranks[il])/len(inlinks[il]))
                    newranks[page] = newrank
                ranks = newranks
            return ranks