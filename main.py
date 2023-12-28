from flask import Flask, request, redirect
import datetime
from replit import db

app = Flask(__name__)

def getChat(user):
  
  message= ""
  f=open("message.html","r")
  message=f.read()
  f.close()
  keys=db.keys()
  keys=list(keys)
  result=""
  recent=0
  for key in reversed(keys):
    #print(db[key]["userid"])17566042
    
    myMessage= message
    myMessage= myMessage.replace("{username}",db[key]["username"])
    myMessage= myMessage.replace("{timestamp}",key)
    myMessage= myMessage.replace("{message}",db[key]["message"])

    if user== "17566042":
      myMessage= myMessage.replace("{admin}",f"""<a href="/delete?id={key}" style="color:rgb(255,0,0);"> X </a>""")
    else:
      myMessage= myMessage.replace("{admin}","")

    
    result+=myMessage
    recent +=1
    if recent == 5:
      break
  return result
  
    
@app.route("/")
def index():
  page=""
  f=open("chat.html", "r")
  page=f.read()
  f.close()
  page=page.replace("{username}",request.headers["X-Replit-User-Name"])
  page=page.replace("{chats}", getChat(request.headers["X-Replit-User-Id"]))
  return page

@app.route("/add", methods=["POST"])
def add():
  form = request.form
  message= form["message"]
  date=datetime.datetime.now()
  timestamp=datetime.datetime.timestamp(date)
  userid=request.headers["X-Replit-User-Id"]
  username=request.headers["X-Replit-User-Name"]
  #page=f"""{userid} {username} {timestamp} {message}"""
  db[timestamp] = {"userid": userid, "username":username, "message":message}
  return redirect("/")
  
@app.route("/delete", methods=["GET"])
def delete():
  if request.headers["X-Replit-User-Id"] != "17566042":
    return redirect("/")
  results=request.values["id"]
  del db[results]
  return redirect("/")
  

app.run(host='0.0.0.0', port=81)

