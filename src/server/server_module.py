'''
Server for search engine
@author: David Mayboroda
'''
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from web_crawler import WebCrawler
from json_generator import generate_json

'''
'OffDocHandler is a class inherited from BaseHTTPRequestHandler.
'So it will handle every http request.
'Each time it get new request, it parse parameters from request.
'After that handler calls lookup_best method with parameters according to parsed request.
'Then generating JSON data from list of outputs links and send it back to requestor. 
'''

class OffDocsHandler(BaseHTTPRequestHandler):
    
    def do_GET(self):
        try:
            global wc_dev, wc_itpro, dev_index, itpro_index, ranks
            self.send_response(200)
            self.send_header('Content-type','text/html')
            self.end_headers()
            prof, key = self.parse_params();
            if prof == "dev":
                self.wfile.write(generate_json(wc_dev.lookup_best(dev_index, key, ranks)))
            elif prof == "itpro":
                self.wfile.write(generate_json(wc_itpro.lookup_best(itpro_index, key, ranks)))
         
        except IOError:
            self.send_error(404,'File Not Found: %s' % self.path)
    
    def parse_params(self):
        qprof = self.path[self.path.find("=")+1 : self.path.find("&")]
        keyword = self.path[self.path.rfind("=")+1: :]
        return qprof, keyword
'''
' Global variables
'''

wc_dev = None
wc_itpro = None
dev_index = None
itpro_index = None
ranks = None

'''
'Instantiating instances of WebCrawler.
'Crawling web based on profile.
'Ranking the crawled web.
'And finally starting web server.
'''


def main():
    try:
        global wc_dev, wc_itpro, dev_index,itpro_index, ranks
        wc_dev = WebCrawler()
        wc_itpro = WebCrawler()
        dev_index=wc_dev.crawl_web("dev")
        itpro_index=wc_itpro.crawl_web("itpro")
        ranks = wc_dev.compute_ranks()
        server = HTTPServer(('192.168.1.225', 8080), OffDocsHandler)
        print 'started http server...'
        server.serve_forever()
    except KeyboardInterrupt:
        print 'shutting down server'
        server.socket.close()

if __name__ == '__main__':
    main()