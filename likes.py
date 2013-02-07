import requests
import getpass
import time


def buildUrl(after):
    url = 'http://www.reddit.com/user/' + user + '/liked.json?limit=100'
    if(after is not None):
        url = url + '&after=' + after
    return url


dictionary = {}
likes = []

user = raw_input("Please input the username: ")
prompt = "Please input the password for " + str(user) + ": "
password = getpass.getpass(prompt=prompt)

payload = {"user": user, "passwd": password, "rem": True}
headers = {"User-Agent": "Wabash", "Content-Length": "0"}
r = requests.post('http://www.reddit.com/api/login',
                  params=payload,
                  headers=headers)

redditCookie = r.cookies

after = None
page = 1
while(True):
    print "Getting page " + str(page)
    s = requests.get(buildUrl(after),
                     cookies=redditCookie)
    if(str(s.status_code) == "200"):
        for l in s.json()[u'data'][u'children']:
            likes.append(l)
        after = str(s.json()[u'data'][u'after'])
        if(str(after) == 'None'):
            break
        #Respecting Reddit's 2 second api rule
        time.sleep(2)
        page = page + 1
    else:
        print "Error ", s.status_code
        exit()

for l in likes:
    sub = str(l[u'data'][u'subreddit'])
    if(sub in dictionary):
        dictionary[sub] = dictionary[sub] + 1
    else:
        dictionary[sub] = 1

sortDict = sorted(dictionary.items(), key=lambda x: x[1], reverse=True)

saveString = ""

total = 0
for s in sortDict:
    total = total + s[1]

for s in sortDict:
    percent = str(round(float(s[1]) / float(total), 3) * 100) + "%"
    saveString = saveString + str(s[0]) + ', ' + str(s[1]) + ', ' + \
        percent + '\n'
    print s[0], s[1], percent

f = open('results.csv', 'w')
f.write(saveString)
f.close()
