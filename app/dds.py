#!/usr/bin/python

import multiprocessing
import containerstats
import etcd
import platform
import docker
import time
import os
import requests

dockerconnection = docker.Client(base_url='unix://var/run/docker.sock', timeout=2)
dockerconnection.close()

def getstats(obj):
    etcd.CreateDir(DDS_ETCD_URL, platform.node() + '/' + obj.containername, DDS_CONTAINER_TTL)
    etcd.SetValue(DDS_ETCD_URL, platform.node() + '/' + obj.containername + '/cpuusage',
                 obj.getcontainercpuusage(dockerconnection)['cpuusage'])
    etcd.SetValue(DDS_ETCD_URL, platform.node() + '/' + obj.containername + '/memusage',
                  obj.getcontainermemusage(dockerconnection)['memusage'])
    etcd.SetValue(DDS_ETCD_URL, platform.node() + '/' + obj.containername + '/memusagepercent',
                  obj.getcontainermemusage(dockerconnection)['memusagepercent'])
    etcd.SetValue(DDS_ETCD_URL, platform.node() + '/' + obj.containername + '/netrx',
                  obj.getcontainernetusage(dockerconnection)['netrx'])
    etcd.SetValue(DDS_ETCD_URL, platform.node() + '/' + obj.containername + '/nettx',
                  obj.getcontainernetusage(dockerconnection)['nettx'])
    return True


if __name__ == '__main__':

    if 'DDS_ETCD_URL' in os.environ:
        DDS_ETCD_URL = os.environ['DDS_ETCD_URL']
    else:
        DDS_ETCD_URL = 'http://127.0.0.1:4001/v2/keys/'

    if 'DDS_CONCURRENCY_LEVEL' in os.environ:
        DDS_CONCURRENCY_LEVEL = os.environ['DDS_CONCURRENCY_LEVEL']
    else:
        DDS_CONCURRENCY_LEVEL = 8

    # start values
    DDS_HOST_TTL = 120
    DDS_CONTAINER_TTL = 30


    while True:
        newpool = multiprocessing.Pool(processes=DDS_CONCURRENCY_LEVEL)
        etcd.CreateDir(DDS_ETCD_URL, platform.node(), ttl=DDS_HOST_TTL)
        containerlist = containerstats.getrunningcontainers(dockerconnection)
        objlist = []
        for container in containerlist:
            objlist.append(containerstats.ContainerStats(container))
        gatherstart = time.time()
        # when i.e. container stop during data gathering timeout generated
        try:
            newpool.map(getstats, objlist)
        except requests.packages.urllib3.exceptions.ReadTimeoutError:
            pass
        newpool.close()
        gatherstop = time.time()
        gatherduration = int(gatherstop - gatherstart)
        DDS_HOST_TTL = gatherduration * 5
        DDS_CONTAINER_TTL = gatherduration * 3
        time.sleep(gatherduration)
