#!/usr/bin/python

import requests

def CatchExceptions(func):
    def func_wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception, e:
            print "Cannot connect to etcd"
            print str(e)
            return False

    return func_wrapper

@CatchExceptions
def CreateDir(url, path, ttl=None):
    r = requests.put(url + path, data={'ttl': ttl, 'dir': 'true'})
    if r.status_code == 403:
        requests.put(url + path, data={'ttl': ttl, 'dir': 'true', 'prevExist': 'true'})
    return True


@CatchExceptions
def SetValue(url, path, val, ttl=None):
    requests.put(url + path, data={'value': val, 'ttl': ttl})
    return True
