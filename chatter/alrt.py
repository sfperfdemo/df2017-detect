import sys
import configparser
import requests

debugFlag=True

# Credentials
usr=""
pwd=""
clientId=""
clientSecret=""

# App properties
loginUrl=""
grantService=""
userId=""
postUrl=""

# Read property file
def readIni(inifile):
  global usr, pwd, clientId, clientSecret
  global loginUrl, grantService, userId, postUrl

  config = configparser.ConfigParser()
  config.read('prop.ini')

  usr = config['CREDENTIALS']['USERNAME']
  pwd = config['CREDENTIALS']['PASSWORD']
  clientId = config['CREDENTIALS']['CLIENTID']
  clientSecret = config['CREDENTIALS']['CLIENTSECRET']

  loginUrl = config['APP']['LOGINURL']
  grantService = config['APP']['GRANTSERVICE']
  userId = config['APP']['USERID']
  postUrl = config['APP']['POSTURL']
# end readIni

# Authenticate User
def authenticate(url):
  data = {
    'username' : usr,
    'password' : pwd,
    'client_id' : clientId,
    'client_secret' : clientSecret
  }
  headers = {
    'content-type' : 'application/x-www-form-urlencoded'
  }
  req = requests.post(url, data=data, headers=headers)
  if debugFlag:
    print("DEBUG", url, req.status_code, req.reason)
  response = req.json()
  if debugFlag:
    print("DEBUG", response)

  accessToken = response['access_token']
  instanceUrl = response['instance_url']
  if debugFlag:
    print("DEBUG", accessToken, instanceUrl)

  return(accessToken, instanceUrl)
# end authenticate

# Send Chatter Message
def sendMessage(accessToken, url, message):
  data = {
    'feedElementType' : 'FeedItem',
    'subjectId' : userId,
    'text' : message
  }
  headers = {
    'content-type' : 'application/x-www-form-urlencoded',
    'Authorization' : "OAuth " + accessToken
  }
  req = requests.post(url, data=data, headers=headers)
  if debugFlag:
    print("DEBUG", url, req.status_code, req.reason)
  response = req.json()
  if debugFlag:
    print("DEBUG", response)
#end sendMessage

# Start
message = sys.argv[1]
readIni("prop.ini")
(loginAccessToken, loginInstanceUrl) = authenticate(loginUrl+grantService)
sendMessage(loginAccessToken, loginInstanceUrl+postUrl, message)
