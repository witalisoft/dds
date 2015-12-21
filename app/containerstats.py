#!/usr/bin/python

import json

def getrunningcontainers(connection):
    containerlist = connection.containers()
    containernames = []
    for item in containerlist:
        containernames.append(item['Names'][0].replace('/', ''))
    connection.close()
    return containernames


class ContainerStats(object):
    def __init__(self, containername):
        self.iternum = 1
        self.containerstats = {}
        self.containername = containername

    def getcontainermemusage(self, connection):
        self.containerstats = {}
        containercounters = connection.stats(self.containername)
        for stat in containercounters:
            jstat = json.loads(stat)
            self.containerstats['memusagepercent'] = round((float(jstat['memory_stats']['usage']) / float(
                jstat['memory_stats']['limit'])) * 100, 2)
            self.containerstats['memusage'] = float(jstat['memory_stats']['usage'])
            break
        return self.containerstats

    def getcontainernetusage(self, connection):
        self.containerstats = {}
        containercounters = connection.stats(self.containername)
        for stat in containercounters:
            jstat = json.loads(stat)
            self.containerstats['netrx'] = jstat['network']['rx_bytes']
            self.containerstats['nettx'] = jstat['network']['tx_bytes']
            break
        return self.containerstats

    def getcontainercpuusage(self, connection):
        self.containerstats = {}
        containercounters = connection.stats(self.containername)
        i = 0
        for stat in containercounters:
            jstat = json.loads(stat)
            current_cpu_usage = float(jstat['cpu_stats']['cpu_usage']['total_usage'])
            previous_cpu_usage = float(jstat['precpu_stats']['cpu_usage']['total_usage'])
            current_system_cpu_usage = float(jstat['cpu_stats']['system_cpu_usage'])
            previous_system_cpu_usage = float(jstat['precpu_stats']['system_cpu_usage'])
            try:
                cpu_num = len(jstat['precpu_stats']['cpu_usage']['percpu_usage'])
                cpuusagepercent = round((current_cpu_usage - previous_cpu_usage) / (
                    current_system_cpu_usage - previous_system_cpu_usage) * cpu_num * 100, 2)
                self.containerstats['cpuusage'] = cpuusagepercent
            except TypeError:
                continue

            i += 1
            if i > self.iternum:
                break
        return self.containerstats
