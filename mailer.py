from tkinter import *
import re
import sqlite3
import csv
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from tkinter import messagebox

db = sqlite3.connect("Student_DB.sqlite")
root = Tk()
root.title("DB Mailer")
root.geometry("280x320")

# raising an exception
class wrongSub(Exception):
    pass
class wrongName(Exception):
    pass
class wrongEmailBasic(Exception):
    pass
class wrongEmailNull(Exception):
    pass
class wrongRollNo(Exception):
    pass

def createTable():
    # creating table
    try:
        db.execute("""create table
               student(rno integer PRIMARY KEY,name text,sub1 integer,
               sub2 integer,sub3 integer,perc integer)""")
        Label(root,text = "Table Created").grid(column=1,row=15)
    except:
        messagebox.showinfo("DB Mailer", "Table already exists")

def addData():
    list1 =  []
    try:
        rno = int(roll.get())
        name = nm.get()
        sub1 = int(s1.get())
        sub2 = int(s2.get())
        sub3 = int(s3.get())
        # checking the sub marks range
        if (sub1 > 100 or sub1 < 0):
            raise wrongSub
        elif (sub2 > 100 or sub2 < 0):
            raise wrongSub
        elif (sub3 > 100 or sub3 < 0):
            raise wrongSub
        elif name.isdigit():
            raise wrongName
        list1.append(rno)
        list1.append(name)
        list1.append(sub1)
        list1.append(sub2)
        list1.append(sub3)
        perc = (sub1+sub2+sub3)/3
        list1.append(perc)
        db.execute("insert into student values(?,?,?,?,?,?)",list1)
        db.commit()
        Label(root,text = "Data Stored").grid(column=1,row=16)
    except wrongSub:
        messagebox.showinfo("DB Mailer", "Enter subject marks b/w 0-100")
    except wrongName:
        messagebox.showinfo("DB Mailer","Incorrect Name")
    # avoiding same roll no entry
    except sqlite3.IntegrityError:
        messagebox.showinfo("DB Mailer", "Roll no. already exists")
    except:
        messagebox.showinfo("DB Mailer", "Invalid Input")


def perc():
    try:
        rno = [int(roll.get())]
        cursor = db.cursor()
        cursor.execute("select * from student where rno =?",rno)
        list1 = cursor.fetchall()
        Label(root,text = "%.2f"% list1[0][5]).grid(column=1,row=17)
        cursor.close()
    except:
        messagebox.showinfo("DB Mailer", "Roll no. not found")
    
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
    Label(root,text = "CSV Generated").grid(column=1,row=18)
    cursor.close()

def sendReport():
    try:
        rno = [int(roll.get())]
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
        # for generating error when roll no is absent
        if len(list1[0][1]) == 0:
            list1[0][1] = list1[0][1]
        elif len(receiver)== 0:
            raise wrongEmailNull
        # for checking '@' in email
        elif not(re.search("\S+@\S+com",receiver)):
            raise wrongEmailBasic
    except IndexError:
        messagebox.showinfo("DB Mailer","Roll no. not found")
    except wrongEmailNull:
        messagebox.showinfo("DB Mailer","Receiver mail-id is empty")
    except wrongEmailBasic:
        messagebox.showinfo("DB Mailer","Missing '@' in email")
    except:
        messagebox.showinfo("DB Mailer","Wrong roll no. or receiver mail")
    try:
        # username and password
        username = sender
        password = open("pwd.txt").read()
    except:
        messagebox.showinfo("DB Mailer","Unable to read Password")
    try:
        str1 = str(list1)
        # creating the mail body
        body = """
<h1>Student Report Card</h1>
<h3>Format: [(Roll No,'Student Name', Sub 1,Sub 2, Sub 3,Perc %)]</h3>
<h3>{str1}<b><h3>
<h4>Thank you</h4>
""".format(str1=str1)
        txt = MIMEText(body,"html")
        message.attach(txt)
        # connecting to Gmail Server
        server = smtplib.SMTP("smtp.gmail.com",587)
        server.starttls()
        server.login(username,password)
        server.sendmail(sender,receiver,message.as_string())
        Label(root,text = "Mail Sent").grid(column=1,row=19)
    except:
        messagebox.showinfo("DB Mailer","Server Error")
    
# taking the input values
Label(root,text = "Roll No:").grid(column=0,row=0)
roll = Entry(root)
roll.grid(column=1,row=0)

Label(root,text = "Name:").grid(column=0,row=2)
nm = Entry(root)
nm.grid(column=1,row=2)

Label(root,text = "Subject 1 Marks(out of 100):").grid(column=0,row=4)
s1 = Entry(root)
s1.grid(column=1,row=4)

Label(root,text = "Subject 2 Marks(out of 100):").grid(column=0,row=6)
s2 = Entry(root)
s2.grid(column=1,row=6)

Label(root,text = "Subject 3 Marks(out of 100):").grid(column=0,row=8)
s3 = Entry(root)
s3.grid(column=1,row=8)

Label(root,text = "Receiver Email Address:").grid(column=0,row=10)
rec = Entry(root)
rec.grid(column=1,row=10)

# creating buttons
btn1 = Button(root,text = "CREATE TABLE",command = createTable).grid(column=0,row=15)
btn2 = Button(root,text = "ADD DATA",command = addData).grid(column=0,row=16)
btn3 = Button(root,text = "CHECK PERCENTAGE",command = perc).grid(column=0,row=17)
btn4 = Button(root,text = "GENERATE CSV REPORT",command = genReport).grid(column=0,row=18)
btn5 = Button(root,text = "SEND REPORT TO MAIL",command = sendReport).grid(column=0,row=19)

# developer info
Label(root,text = "Developer: Kumar Anurag").grid(column=0,row=20)
Label(root,text = "Instagram: kmranrg").grid(column=0,row=21)
Label(root,text = "Twitter: kmranrg").grid(column=0,row=22)

root.mainloop()
