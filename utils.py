import requests
import time
import os
import re
import requests

class Downloader(object):
    def __init__(self,filename='',dest=''):
        self.filename = filename
        self.dest = dest
        self.stoping = False
    async def downloadFile(self,url='',progressfunc=None,args=None):
        req = requests.get(url, stream = True,allow_redirects=True)
        if req.status_code == 200:
            file_size = req_file_size(req)
            file_name = get_url_file_name(url,req)
            if self.filename!='':
                file_name = self.filename
            file_wr = open(self.dest+file_name,'wb')
            chunk_por = 0
            chunkrandom = 100
            total = file_size
            time_start = time.time()
            time_total = 0
            size_per_second = 0
            for chunk in req.iter_content(chunk_size = 1024):
                    if self.stoping:break
                    chunk_por += len(chunk)
                    size_per_second+=len(chunk);
                    tcurrent = time.time() - time_start
                    time_total += tcurrent
                    time_start = time.time()
                    if time_total>=1:
                        if progressfunc:
                            await progressfunc(self,file_name,chunk_por,total,size_per_second,args)
                        time_total = 0
                        size_per_second = 0
                    file_wr.write(chunk)
            file_wr.close()
            return self.dest+file_name
        return self.dest+self.filename
    async def stop(self):self.stoping=True

class TGDownloaderProgress(object):
    def __init__(self,filename='',progressfunc=None,args=None):
        self.file_name = filename
        self.handle = progressfunc
        self.args = args
        self.time_start = time.time()
        self.time_total = 0
        self.size_per_second = 0
        self.last_read = 0
    async def progress_callback(self,current,total):
        self.size_per_second += current - self.last_read
        self.last_read = current
        if self.handle:
           await self.handle(self, self.file_name, current, total, self.size_per_second, self.args)
        self.size_per_second = 0

def sizeof_fmt(num, suffix='B'):
    for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)

def req_file_size(req):
    try:
        return int(req.headers['content-length'])
    except:
        return 0

def get_url_file_name(url,req):
    try:
        if "Content-Disposition" in req.headers.keys():
                name = str(req.headers["Content-Disposition"]).replace('attachment; ','')
                name = name.replace('filename=','').replace('"','')
                return name
        else:
            import urllib
            urlfix = urllib.parse.unquote(url,encoding='utf-8', errors='replace')
            tokens = str(urlfix).split('/');
            return tokens[len(tokens)-1]
    except:
        import urllib
        urlfix = urllib.parse.unquote(url,encoding='utf-8', errors='replace')
        tokens = str(urlfix).split('/');
        return tokens[len(tokens)-1]
    return ''

def get_file_size(file):
    file_size = os.stat(file)
    return file_size.st_size

def createID(count=8):
    from random import randrange
    map = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    id = ''
    i = 0
    while i<count:
        rnd = randrange(len(map))
        id+=map[rnd]
        i+=1
    return id