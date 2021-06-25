import config
import requests

urlLine = 'https://notify-api.line.me/api/notify'
token = config.LINE_NOTIFY_TOKEN
headers = {
            'content-type':
            'application/x-www-form-urlencoded',
            'Authorization':'Bearer '+token
           }

def send_alert(msg = 'ทดสอบ'):
    r = requests.post(urlLine, headers=headers , data = {'message':msg})
    print(r.text)

def send_pic(path='',msg ='BUY'):
    file = {'imageFile':open(path+'.png','rb')}
    data = ({
            'message':msg
        })
    LINE_HEADERS = {"Authorization":"Bearer "+token}
    session = requests.Session()
    r=session.post(urlLine, headers=LINE_HEADERS, files=file, data=data)
    print(r.text) 


