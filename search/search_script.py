'''
Created on Apr 14, 2012

@author: sergii
'''
#*** CODE STARTS HERE
#****** ************

import urllib
import socket
socket.setdefaulttimeout(10)
# in a true webcrawler you should not use re instead use a DOM parser
import re

def get_page(url):
        try:
            f = urllib.urlopen(url)
            page = f.read()
            f.close()
            return page
        except:
            return ""
        return ""
def get_next_target(page):
        start_link = page.find('<a href=')
        if start_link == -1:
            return None, 0
        start_quote = page.find('"', start_link)
        end_quote = page.find('"', start_quote + 1)
        url = page[start_quote + 1:end_quote]
        return url, end_quote
def union(p,q):
        cnt = 0
        for e in q:
            if e not in p:
                p.append(e)
                cnt += 1
        return cnt
def get_all_links(page):
        links = []
        while True:
            url,endpos = get_next_target(page)
            if url:
                links.append(url)
                page = page[endpos:]
            else:
                break
        return links
def add_to_index(index,keyword,url):
        for entry in index:
            if entry[0] == keyword:
                if url not in entry[1]:
                    entry[1].append(url)
                return
        index.append([keyword,[url]])
def split_string(source,splitlist):
        return ''.join([ w if w not in splitlist else ' ' for w in source]).split()
def add_page_to_index_re(index,url,content):
        i = 0
        # it is not a good idea to use regular expression to parse html
        # i did this just to give a quick and dirty result
        # to parse html pages in practice you should use a DOM parser
        regex = re.compile('(?<!script)[>](?![\s\#\'-<]).+?[<]')

        for words in regex.findall(content):
            word_list = split_string(words, """ ,"!-.()<>[]{};:?!-=`&""")
            for word in word_list:
                add_to_index(index,word,url)
                i += 1
        return i
def format_url(root,page):
        if page[0] == '/':
            return root + page
        return page
def crawl_web(seed,max_pages=10,max_depth=1):
        root = seed
        tocrawl = [seed]
        depth = [0]
        crawled = []
        index = []
        while tocrawl and len(crawled) < max_pages:
            page = tocrawl.pop()
            d = depth.pop()
            if page not in crawled:
                page = format_url(root,page)
                content = get_page(page)
                success = add_page_to_index_re(index,page,content)
                if d != max_depth:
                    cnt = union(tocrawl,get_all_links(content))
                    for i in range(cnt):
                        depth.append(d+1)
                crawled.append(page)
        return index
# code below only runs when this file is run as a script
# if you imported this code into your own module the code
# below would not be accessible by your code
if __name__ == "__main__":
        import optparse
        __version__ = "0.1"
        USAGE   = "%prog [options] <url>"
        VERSION = "%prog v" + __version__
        def parse_options():
                """parse_options() -> opts, args

                Parse any command-line options given returning both
                the parsed options and arguments.
                """
                parser = optparse.OptionParser(usage=USAGE,version=VERSION)
                parser.add_option("-p", "--maxpages",action="store", type="int",
                                      default=10, dest="maxpages",
                                      help="Maximum number of pages to crawl")
                parser.add_option("-d", "--maxdepth",action="store", type="int",
                                      default=1, dest="maxdepth",
                                      help="Maximum depth to traverse")
                parser.add_option("-i", "--index",action="store", type="int",
                                      default=1, dest="index_cnt",
                                      help="Maximum number of index items to print out")
                (opts, args) = parser.parse_args()
                if len(args) < 1:
                    parser.print_help()
                    raise SystemExit, 1
                return opts, args
        def main():
                opts, args = parse_options()
                url = args[0]
                if url[len(url) - 1] == '/':
                    url = url[:len(url) - 1]
                maxdepth = opts.maxdepth
                maxpages = opts.maxpages
                index_cnt = opts.index_cnt
                index = crawl_web(url,maxpages,maxdepth)
                print "Printing index..."
                for i,e in enumerate(index):
                    if i >= index_cnt:
                        return
                    print "'{}' appears in the following urls:".format(e[0])
                    for i,u in enumerate(e[1]):
                        print "    {}".format(u)
        main()
