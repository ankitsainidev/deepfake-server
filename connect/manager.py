import json
import os
import time
import json
from django.conf import settings
import pickle
BASE_DIR = settings.BASE_DIR
LINK_FILE_PATH = os.path.join(BASE_DIR,'data','links.txt')
TIME_LIMIT = 600
NOTIFY_AT = 10
class TimeManager:
    def __init__(self, devisions=60,path = os.path.join(BASE_DIR,'data','value.pkl')):
        self.parts = 50
        self.devisions = devisions
        self.path = path
        try:
            self.values = self.read()
        except (FileNotFoundError,EOFError):
            self.values = [[time.time() -TIME_LIMIT for i in range(devisions)] for j in range(self.parts)]
            self.flush()

    def reverse(self,part):
        return int(part)
    def forward(self,i):
        return str(i).rjust(2,'0')
    def flush(self):
        with open(self.path,'wb') as file:
            pickle.dump(self.values,file)
        
    def read(self):
        values = 0
        with open(self.path,'rb') as file:
            values = pickle.load(file)
        return values
man = TimeManager()
def assign_next(part = None):
    response_dict = {}
    response_dict['notify_at'] = NOTIFY_AT
    if part:
        for i,t in enumerate(man.values[man.reverse(part)]):
            if time.time() - t >TIME_LIMIT:
                response_dict['part'] = part
                response_dict['devisions'] = len(man.values[man.reverse(part)])
                response_dict['block'] = i
                return response_dict
    for j in range(man.devisions):

        for i in range(len(man.values)):
            if time.time() - man.values[i][j] >TIME_LIMIT:
                    response_dict['part'] = man.forward(i)
                    response_dict['devisions'] = len(man.values[i])
                    response_dict['block'] = j
                    return response_dict
    return {'completed': True}

def update_time(part,i):
    man.values[man.reverse(part)][i] = time.time()
    man.flush()

def close(part,block,link):
    with open(LINK_FILE_PATH,'a') as links:
        links.write(f'{(link+"  ").ljust(40,"-")}----  {part}-{block}\n')
    man.values[man.reverse(part)][block] = float('inf')
    man.flush()
