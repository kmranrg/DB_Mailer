from tkinter import *
import sqlite3
import csv
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

db = sqlite3.connect("Student_DB.sqlite")
root = Tk()
root.title("DB Mailer")
root.geometry("280x320")


def createTable():
    # creating table
    db.execute("""create table
               student(rno integer,name text,sub1 integer,
               sub2 integer,sub3 integer,perc integer)""")
    Label(root,text = "Table Created").grid(column=1,row=13)

def addData():
    list1 =  []
    rno = int(roll.get())
    name = nm.get()
    sub1 = int(s1.get())
    sub2 = int(s2.get())
    sub3 = int(s3.get())
    list1.append(rno)
    list1.append(name)
    list1.append(sub1)
    list1.append(sub2)
    list1.append(sub3)
    perc = (sub1+sub2+sub3)/3
    list1.append(perc)
    db.execute("insert into student values(?,?,?,?,?,?)",list1)
    db.commit()
    Label(root,text = "Data Stored").grid(column=1,row=14)

def perc():
    rno = [int(roll.get())]
    cursor = db.cursor()
    cursor.execute("select * from student where rno =?",rno)
    list1 = cursor.fetchall()
    Label(root,text = "%.2f"% list1[0][5]).grid(column=1,row=15)
    cursor.close()
    
def genReport():
    title = ["roll_no","name","sub_1","sub_2","sub_3","per %"]
    cursor = db.cursor()
    cursor.execute("select * from student")
    list1 = cursor.fetchall()
    #opening the CSV file
    file = open("report.csv","w",newline = "")
    obj = csv.writer(file)
    obj.writerow(title)
    for i in list1:
        obj.writerow(i)
    Label(root,text = "CSV Generated").grid(column=1,row=16)
    cursor.close()

def sendReport():
    rno = [roll.get()]
    cursor = db.cursor()
    cursor.execute("select * from student where rno =?",rno)
    list1 = cursor.fetchall()
    cursor.close()
    message = MIMEMultipart()
    message["Subject"] = "Report Card"
    message["From"] = "Ukan Team"
    # sender and receiver
    sender = "sender@gmail.com"
    receiver = rec.get()
    # username and password
    username = sender
    password = open("pwd.txt").read()
    str1 = str(list1)
    # creating the mail body
    body = """
<h1>Student Report Card</h1>
<h3>Format: [(Roll No,Student Name, Sub 1,Sub 2, Sub 3,Perc %)]</h3>
<h3>{str1}<b><h3>
<h4>Thank you</h4>
""".format(str1=str1)
    txt = MIMEText(body,"html")
    message.attach(txt)
    server = smtplib.SMTP("smtp.gmail.com",587)
    server.starttls()
    server.login(username,password)
    server.sendmail(sender,receiver,message.as_string())
    Label(root,text = "Mail Sent").grid(column=1,row=17)
    

Label(root,text = "Roll No:").grid(column=0,row=0)
roll = Entry(root)
roll.grid(column=1,row=0)

Label(root,text = "Name:").grid(column=0,row=2)
nm = Entry(root)
nm.grid(column=1,row=2)

Label(root,text = "Suject 1 Marks(out of 100):").grid(column=0,row=4)
s1 = Entry(root)
s1.grid(column=1,row=4)

Label(root,text = "Suject 2 Marks(out of 100):").grid(column=0,row=6)
s2 = Entry(root)
s2.grid(column=1,row=6)

Label(root,text = "Suject 3 Marks(out of 100):").grid(column=0,row=8)
s3 = Entry(root)
s3.grid(column=1,row=8)

Label(root,text = "Receiver Email Address:").grid(column=0,row=10)
rec = Entry(root)
rec.grid(column=1,row=10)

btn1 = Button(root,text = "CREATE TABLE",command = createTable).grid(column=0,row=13)
btn2 = Button(root,text = "ADD DATA",command = addData).grid(column=0,row=14)
btn3 = Button(root,text = "CHECK PERCENTAGE",command = perc).grid(column=0,row=15)
btn4 = Button(root,text = "GENERATE CSV REPORT",command = genReport).grid(column=0,row=16)
btn5 = Button(root,text = "SEND REPORT TO MAIL",command = sendReport).grid(column=0,row=17)

Label(root,text = "Developer: Kumar Anurag").grid(column=0,row=20)
Label(root,text = "Instagram: kmranrg").grid(column=0,row=21)
Label(root,text = "Twitter: kmranrg").grid(column=0,row=22)

root.mainloop()
