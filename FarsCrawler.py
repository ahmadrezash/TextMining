import pandas as pd
from bs4 import BeautifulSoup
import requests

websiteURL = 'https://www.farsnews.com/economy'
homeURL = 'https://www.farsnews.com'
req = requests.get(websiteURL)
html = BeautifulSoup(req.text , 'html.parser')
posts = html.find(class_ = 'ctgnewsmainpane').find_all(class_='topnews')


posts = html.find(class_ = 'ctgnewsmainpane').find_all(class_='topnews')
data = []
for i in posts:
    img     = i.a.img.get('src')
    postUrl = i.a.get('href')
    if i.find_all('div')[1].a.find(class_='newsrotitrCtgTop'):
        whoTell = i.find_all('div')[1].a.find(class_='newsrotitrCtgTop').get_text()
    else:
        whoTell = ''
    title   = i.find_all('div')[1].a.find(class_='ctgtopnewsinfotitle').get_text()
    summery = i.find_all('div')[1].get_text()
    data.append([   whoTell , title , summery ,img ,homeURL+postUrl , 'sample'])

df = pd.DataFrame(data)
df = df.rename(columns = {0 : 'whoTell',
              1 : 'title',
              2 : 'summery',
              3 : 'img',
              4 : 'postUrl',
              5 : 'body'        
                         })

for index, post in df.iterrows():
    req = requests.get(post['postUrl'])
    postHtml = BeautifulSoup(req.text , 'html.parser')
    dirtyText = postHtml.find(class_='nwstxtmainpane').span.find_all('p')
    body = ''
    for i in dirtyText:
        body += i.get_text()
    df.loc[index]['body'] = body
    print(index,'th is Done!')
df


from pony.orm import *
db = Database()
class Post(db.Entity):
    whoTell = str
    title   = Required(str)
    summery = Required(LongStr)
    img     = Required(str)
    postUrl = Required(str)
    body    = Required(LongStr)
db.bind(provider='mysql', host='127.0.0.1', user='root', passwd='1', db='Fars')
db.generate_mapping(check_tables=False, create_tables=True)
for index, post in df.iterrows():
    whoTell = post['whoTell']
    title   = post['title']
    summery = post['summery']
    img     = post['img']
    postUrl = post['postUrl']
    body    = post['body']
    db.insert("post",
             title = title,
             summery = summery,
             img = img,
             postUrl = postUrl,
             body = body)

    