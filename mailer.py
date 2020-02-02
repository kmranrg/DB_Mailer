import sqlite3
import csv
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

db = sqlite3.connect("Student_DB.sqlite")

def createTable():
    # creating table
    db.execute("""create table
               student(rno integer,name text,sub1 integer,
               sub2 integer,sub3 integer,perc integer)""")
    print("Table Created successfully")

def addData():
    list1 =  []
    rno = int(input("Enter roll no:"))
    name = input("Enter name:")
    sub1 = int(input("Enter marks in subject 1(out of 100):"))
    sub2 = int(input("Enter marks in subject 2(out of 100):"))
    sub3 = int(input("Enter marks in subject 3(out of 100):"))
    list1.append(rno)
    list1.append(name)
    list1.append(sub1)
    list1.append(sub2)
    list1.append(sub3)
    perc = (sub1+sub2+sub3)/3
    list1.append(perc)
    db.execute("insert into student values(?,?,?,?,?,?)",list1)
    db.commit()
    print("Data Stored sucessfully!")

def perc():
    rno = [int(input("Enter roll no:"))]
    cursor = db.cursor()
    cursor.execute("select * from student where rno =?",rno)
    list1 = cursor.fetchall()
    print("Percentage:",list1[0][5])
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
    print("Report generated successfully!")
    cursor.close()

def sendReport():
    rno = [int(input("Enter roll no:"))]
    cursor = db.cursor()
    cursor.execute("select * from student where rno =?",rno)
    list1 = cursor.fetchall()
    cursor.close()
    message = MIMEMultipart()
    message["Subject"] = "Report Card"
    message["From"] = "Ukan Team"
    # sender and receiver
    sender = "sender@gmail.com"
    receiver = "receiver@gmail.com"
    # username and password
    username = sender
    password = open("pwd.txt").read()
    str1 = str(list1)
    # creating the mail body
    body = """
<h1>Student Report Card</h1>
<h3>Format: [Roll No,Student Name, Sub 1,Sub 2, Sub 3,Perc %]</h3>
<h3>{str1}<b><h3>
<h4>Thank you</h4>
""".format(str1=str1)
    txt = MIMEText(body,"html")
    message.attach(txt)
    server = smtplib.SMTP("smtp.gmail.com",587)
    server.starttls()
    print("connected with the gmail server")
    server.login(username,password)
    server.sendmail(sender,receiver,message.as_string())
    print("mail sent successfully")
    

while True:
    ch = int(input("""
1. Create table
2. Add data
3. Check Percentage
4. Generate Report
5. Send Report
6. Exit
Enter choice:"""))

    if ch ==1  :
        createTable()
    elif ch ==2:
        addData()
    elif ch ==3:
        perc()
    elif ch==4:
        genReport()
    elif ch ==5:
        sendReport()
    elif ch==6:
        db.close()
        break
    else:
        print("Invalid input!")
        db.close()
