'''
Created on Apr 15, 2012

@author: Sergii Kozyrev
'''
'''
'''
import json

'''
' Generating JSON data to response on client request.
'''


def generate_json(urls):
    list_for_json=[]
    if urls:
        for e in urls:
            list_for_json.append({'url':e})
        return json.dumps({'found':list_for_json})
    else:
        return json.dumps({'found':[{"url":"-1"}]})
    





