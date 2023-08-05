import http
from operator import mod
import string
from tokenize import String
from flask import Flask
from flask import request



app = Flask(__name__)
direction = "-1"
@app.route('/getDirection', methods = ['POST','GET'])
def getDirection():
    global direction
    name = request.data.decode('UTF-8')
    if (name[9] == 'F'):
        direction ='0'
    elif (name[9] =='B'):
        direction ='5'
    elif (name[9] =='R'):
        direction ='1'
    elif (name[9] =='L'):
        direction ='2'
    elif (name[9] =='S'):
        direction ='3'
    else:
        direction ='-1'
    print ("direction is "+ direction)
    return"Recieved"

@app.route('/sendDirection', methods = ['POST','GET'])
def sendDirection():
    global direction
    print("direction sent")
    return direction

if __name__== "__main__":
    app.run('172.28.131.51',port =5635)
