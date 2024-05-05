#MQTT Quiz Application And Python File Created By Adidev-c All Rights Reserved 
import paho.mqtt.client as paho # import paho mqtt library
import pyfirmata, time
board = pyfirmata.Arduino("/dev/ttyUSB0")
print("Arduino Connected Successfully")
ip=input("Enter Your IP:")
score=[]
ansgrp=[]
qn=1
winnerbool=False
servo=board.get_pin('d:9:s')
servo.write(0)
groups=[]
answers=['A','D','C','B','D','B','A','C','B','A','A']
answer='A'
def change_score(name,score,groups):
    global qn
    global answer
    global winner
    global winnerbool
    global ansgrp
    b=groups.index(name[0])
    c=score[b]
    score.pop(b)
    score.insert(b,int(c)+1)
    print(score)
    print(groups)
    qn+=1
    ansgrp=[]
    answer=answers[qn-1]
    print("Question Number:",qn)
    if qn > 10:
        print("\n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n Calculating Score")
        #time.sleep(3)
        for i in range(1,len(groups)+1,1):
            print(i,'-',groups[i-1],':',score[i-1])
        winner=int(input("Winner Group Number:"))
        winner=groups[winner-1]
        print("Winner Is:",winner)
        winnerbool=True
    return score
def trig_action(client, userdata, message):  # this function will be called on receiving messages
    topic = message.topic # topic will be stored to this veriable
    msg = message.payload.decode("utf-8") # message will be decoded and stored to this veriable
    global score
    global groups
    if "Group:" in msg:
        msg=msg.split(':')
        print('Group:',msg[1])
        global groups
        if msg[1] in groups:
            print("Group Already Participating")
        else:
            groups.append(msg[1])
            score.append(0)
            print(groups,score)
    elif ',' in msg:
        a=msg.split(",")
        if a[1]==answer:
            if winnerbool==False:
                ansgrp.append(a[0])
                print("Score Goes To",ansgrp[0])
                print(ansgrp)
                score=change_score(ansgrp,score,groups)
                
            else:
                if a[0]==winner:
                    for i in range(0,180,1):
                        servo.write(i)
                    print("Flag Off Successfull")
                    quit()
    else:
        print('Topic:',topic) 
        print('Message:',msg)

rgbclient = paho.Client() # create paho client object
rgbclient.connect(ip) # to connect with mqtt server (replace ip with your laptop ip)
rgbclient.loop_start() # to start paho client thread 
rgbclient.on_message = trig_action # linking to the function which will be called on receiving message
rgbclient.subscribe('adidev/home/quizz')  # subscribing to a topic

while True:
    pass
 
