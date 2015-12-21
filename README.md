# Distributed Docker Stats
It's a tool that collects containers resource usage and put them into etcd, so it makes its distributed across docker hosts. 

## Detailed
Using resource usage grabbed from docker API via docker-py python module. To speed things up collecting data is started concurrently via multiprocessing.
Host and containers keys are set with etcd TTL.

## Runtime configuration
Environment variables on container run:
* DDS_ETCD_URL - full URL path to etcd 
* DDS_CONCURRENCY_LEVEL - how many processes running (default: 8)

## Available metrics per container
* nettx - network TX in bytes
* netrx - network RX in bytes
* cpuusage - CPU usage in percentage
* memusage - memory usage in bytes
* memusagepercent - memory usage in percentage

## Limitations
* etcd only via http and without authentication
* scalabilty issues 
* no I/O stats
* no client available yet
* not yet battle tested - rather concept now

## Sample usage
1. Clone github repo:
`$ git clone https://github.com/witalisoft/dds.git`
2. Build container image:
`$ sudo docker build -t dds:latest -f Dockerfile .`
3. Run container:
`$ sudo docker run -d -h setyourhostname -v /var/run/docker.sock:/var/run/docker.sock -e DDS_ETCD_URL="http://172.17.0.1:4001/v2/keys/" dds:latest`
4. Application is available under:
`$ curl http://172.17.0.1:4001/v2/keys/?recursive=true 2>/dev/null | python -m json.tool | less`
```json
{
                "createdIndex": 3436,
                "dir": true,
                "expiration": "2015-12-21T11:42:44.058363419Z",
                "key": "/setyourhostname",
                "modifiedIndex": 3436,
                "nodes": [
                    {
                        "createdIndex": 3438,
                        "dir": true,
                        "key": "/setyourhostname/cranky_goldstine",
                        "modifiedIndex": 3438,
                        "nodes": [
                            {
                                "createdIndex": 3520,
                                "key": "/setyourhostname/cranky_goldstine/memusagepercent",
                                "modifiedIndex": 3520,
                                "value": "0.0"
                            },
```
