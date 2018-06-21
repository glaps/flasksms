import re
import turbosmsua
from parsxlsx_num import parser
from conf import apipass

patern = re.compile(r'\b\+?3?8?[\( ]?\d{3}[\)\ ]?\d{3}[- ]?\d{2}[- ]?\d{2}\b')



class flov:
    def __init__(self, msg=None, file=None, num=None, user=None):
        self.msg = msg
        self.file = file
        self.num = num
        self.user = user
    def ress(self):
        if self.file and self.num:
            return parser(self.file) + list(set([re.sub(r'[\(\) \-\+]','',i) for i in re.findall(patern,self.num)]))

        elif self.file:
            return parser(self.file)

        elif self.num:
            return list(set(re.findall(patern,self.num)))

def sendsmsto(num,msg,user=None):
    t = turbosmsua.Turbosms(apipass[0], apipass[1])
    return t.send_text(apipass[2], num, msg)

class store:
    data = {}
class New_store:
    def __call__(self,data):
        self.data=data

