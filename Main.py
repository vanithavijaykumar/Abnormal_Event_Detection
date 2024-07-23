from tkinter import *
import os
from tkinter import filedialog
from pymsgbox import *
import mysql.connector
from tkinter import messagebox
import urllib
import urllib.request
import urllib.parse
import tkinter as tk
from tkinter import ttk

os.environ['OPENCV_VIDEOIO_PRIORITY_MSMF'] = '0'


def endprogram():
    print("\nProgram terminated!")
    sys.exit()


def training():
    global training_screen
    training_screen = Toplevel(main_screen)
    training_screen.title("Training")
    # login_screen.geometry("400x300")
    training_screen.geometry("600x450+650+150")
    training_screen.minsize(120, 1)
    training_screen.maxsize(1604, 881)
    training_screen.resizable(1, 1)
    # login_screen.title("New Toplevel")

    Label(training_screen, text='''Upload Image ''', background="#d9d9d9", disabledforeground="#a3a3a3",
          foreground="#000000", bg="turquoise", width="300", height="2", font=("Calibri", 16)).pack()
    Label(training_screen, text="").pack()
    Label(training_screen, text="").pack()
    Label(training_screen, text="").pack()
    Button(training_screen, text='''Upload Image''', font=(
        'Verdana', 15), height="2", width="30").pack()


# Designing popup for user not found
def testing():
    global testing_screen
    testing_screen = Toplevel(main_screen)
    testing_screen.title("Testing")
    # login_screen.geometry("400x300")
    testing_screen.geometry("600x450+650+150")
    testing_screen.minsize(120, 1)
    testing_screen.maxsize(1604, 881)
    testing_screen.resizable(1, 1)
    # login_screen.title("New Toplevel")

    Label(testing_screen, text='''Upload Image''', background="#d9d9d9", disabledforeground="#a3a3a3",
          foreground="#000000", bg="turquoise", width="300", height="2", font=("Calibri", 16)).pack()
    Label(testing_screen, text="").pack()
    Label(testing_screen, text="").pack()
    Label(testing_screen, text="").pack()
    Button(testing_screen, text='''Upload Image''', font=(
        'Verdana', 15), height="2", width="30").pack()


# Implementing event on login button

def login_verify():
    username1 = username_verify.get()
    password1 = password_verify.get()
    username_login_entry.delete(0, END)
    password_login_entry.delete(0, END)

    list_of_files = os.listdir()
    if username1 in list_of_files:
        file1 = open(username1, "r")
        verify = file1.read().splitlines()
        if password1 in verify:
            Alogin_sucess()

        else:
            password_not_recognised()

    else:
        user_not_found()


# Designing popup for login success

def Alogin_sucess():
    global login_success_screen
    login_success_screen = Toplevel(login_screen)
    login_success_screen.title("Success")
    login_success_screen.geometry("150x100")
    Label(login_success_screen, text="Login Success").pack()
    Button(login_success_screen, text="OK", command=register).pack()


def password_not_recognised():
    global password_not_recog_screen
    password_not_recog_screen = Toplevel(login_screen)
    password_not_recog_screen.title("Success")
    password_not_recog_screen.geometry("150x100")
    Label(password_not_recog_screen, text="Invalid Password ").pack()
    Button(password_not_recog_screen, text="OK").pack()


# Designing popup for user not found
def register_sucess():
    global register_success_screen
    register_success_screen = Toplevel(register_screen)
    register_success_screen.title("Success")
    register_success_screen.geometry("150x100")
    Label(register_success_screen, text="Register Success").pack()
    Button(register_success_screen, text="OK", command=delete_register_success).pack()


def delete_register_success():
    import LiveRecognition  as liv

    liv.att()
    del sys.modules["LiveRecognition"]
    register_success_screen.destroy()
    register_screen.destroy()


def viewrecord():
    import grid  as grid

    grid()
    del sys.modules["grid"]
    register_success_screen.destroy()
    register_screen.destroy()


def viewrentry():
    import entry  as entry

    entry()
    del sys.modules["entry"]
    register_success_screen.destroy()
    register_screen.destroy()


def user_not_found():
    global user_not_found_screen
    user_not_found_screen = Toplevel(login_screen)
    user_not_found_screen.title("Success")
    user_not_found_screen.geometry("150x100")
    Label(user_not_found_screen, text="User Not Found").pack()
    Button(user_not_found_screen, text="OK").pack()


# Deleting popups
def userlog():
    global login_screen
    login_screen = Toplevel(main_screen)
    login_screen.title("Login")
    login_screen.geometry("600x280")
    login_screen.title("Login Form")
    global username_verify
    global password_verify

    username_verify = StringVar()
    password_verify = StringVar()

    global username_login_entry
    global password_login_entry
    label_0 = Label(login_screen, text="Login form", width=20, font=("bold", 20))
    label_0.place(x=90, y=53)

    label_1 = Label(login_screen, text="UserName", width=20, font=("bold", 10))
    label_1.place(x=80, y=130)
    username_login_entry = Entry(login_screen, textvariable=username_verify)
    username_login_entry.place(x=240, y=130)

    label_2 = Label(login_screen, text="Password", width=20, font=("bold", 10))
    label_2.place(x=68, y=180)
    password_login_entry = Entry(login_screen, textvariable=password_verify, show='*')
    password_login_entry.place(x=240, y=180)
    # Button(login_screen,text="Login", command=userlogin,  font=('helvetica', 12, 'bold')).pack(side=BOTTOM)

    bluebutton = Button(login_screen, text="Login", fg="blue", font=('helvetica', 12), command=userlogin)
    bluebutton.place(x=220, y=210)
    bluebutton1 = Button(login_screen, text="Reset", fg="blue", font=('helvetica', 12), command=userlog)
    bluebutton1.place(x=300, y=210)

    bluebutton2 = Button(login_screen, text="New User Register", fg="blue", font=('helvetica', 12), command=register)
    bluebutton2.place(x=300, y=250)


def Adminlog():
    global login_screen
    login_screen = Toplevel(main_screen)
    login_screen.title("Login")
    login_screen.geometry("600x280")
    login_screen.title("Login Form")
    global username_verify
    global password_verify

    username_verify = StringVar()
    password_verify = StringVar()

    global username_login_entry
    global password_login_entry
    label_0 = Label(login_screen, text="Login form", width=20, font=("bold", 20))
    label_0.place(x=90, y=53)

    label_1 = Label(login_screen, text="UserName", width=20, font=("bold", 10))
    label_1.place(x=80, y=130)
    username_login_entry = Entry(login_screen, textvariable=username_verify)
    username_login_entry.place(x=240, y=130)

    label_2 = Label(login_screen, text="Password", width=20, font=("bold", 10))
    label_2.place(x=68, y=180)
    password_login_entry = Entry(login_screen, textvariable=password_verify, show='*')
    password_login_entry.place(x=240, y=180)
    # Button(login_screen,text="Login", command=userlogin,  font=('helvetica', 12, 'bold')).pack(side=BOTTOM)

    bluebutton = Button(login_screen, text="Login", fg="blue", font=('helvetica', 12), command=adminlogin)
    bluebutton.place(x=220, y=210)
    bluebutton1 = Button(login_screen, text="Reset", fg="blue", font=('helvetica', 12), command=Adminlog)
    bluebutton1.place(x=300, y=210)


def adminlogin():
    username1 = username_verify.get()
    password1 = password_verify.get()
    print(username1)
    print(password1)
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1faceiotdb')
    cursor = conn.cursor()
    cursor.execute("SELECT * from admintb where uname='" + username1 + "' and password='" + password1 + "'")
    data = cursor.fetchone()

    if data is None:
        print('Username or Password is wrong')
    else:
        Alogin_sucess()


def userlogin():
    username1 = username_verify.get()
    password1 = password_verify.get()
    print(username1)
    print(password1)
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1faceiotdb')
    cursor = conn.cursor()
    cursor.execute("SELECT * from register where uname='" + username1 + "' and password='" + password1 + "'")
    data = cursor.fetchone()

    if data is None:
        print('Username or Password is wrong')
    else:
        Alogin_sucess()


def register():
    global register_screen
    register_screen = Toplevel(main_screen)
    register_screen.title("New User")
    register_screen.geometry("700x600")
    register_screen.title("New UserRegister Form")
    global name
    global email
    global var
    global address
    global pnumber
    global uname

    name = StringVar()
    email = StringVar()

    address = StringVar()
    pnumber = StringVar()
    uname = StringVar()

    global name1
    global email1
    global var1
    global address1
    global pnumber1
    global uname1

    label_0 = Label(register_screen, text="Criminal Register form", width=20, font=("bold", 20))

    label_0.place(x=90, y=60)
    label_1 = Label(register_screen, text="FullName", width=20, font=("bold", 10))
    label_1.place(x=80, y=130)
    name1 = Entry(register_screen, textvariable=name)
    name1.place(x=240, y=130)
    label_3 = Label(register_screen, text="Email", width=20, font=("bold", 10))
    label_3.place(x=68, y=230)
    email1 = Entry(register_screen, textvariable=email)
    email1.place(x=240, y=230)
    # this creates 'Label' widget for Gender and uses place() method.
    label_4 = Label(register_screen, text="Gender", width=20, font=("bold", 10))
    label_4.place(x=70, y=180)
    # the variable 'var' mentioned here holds Integer Value, by deault 0
    var = IntVar()

    Radiobutton(register_screen, text="Male", padx=5, variable=var, value=1).place(x=235, y=180)
    Radiobutton(register_screen, text="Female", padx=20, variable=var, value=2).place(x=290, y=180)
    ##this creates 'Label' widget for country and uses place() method.
    label_5 = Label(register_screen, text="Address", width=20, font=("bold", 10))
    label_5.place(x=80, y=280)
    address1 = Entry(register_screen, textvariable=address)
    address1.place(x=240, y=280)
    label_6 = Label(register_screen, text="phoneNumber", width=20, font=("bold", 10))
    label_6.place(x=80, y=330)
    pnumber1 = Entry(register_screen, textvariable=pnumber)
    pnumber1.place(x=240, y=330)
    label_7 = Label(register_screen, text="UserName", width=20, font=("bold", 10))
    label_7.place(x=80, y=380)
    uname1 = Entry(register_screen, textvariable=uname)
    uname1.place(x=240, y=380)

    Button(register_screen, text='Submit', width=20, bg="black", fg='white', command=userregister).place(x=180, y=480)
    Button(register_screen, text='reset', width=20, bg="black", fg='white').place(x=380, y=480)
    Button(register_screen, text='ViewRecord', width=20, bg="black", fg='white', command=viewrecord).place(x=580, y=480)
    Button(register_screen, text='ViewRecord', width=20, bg="black", fg='white', command=viewrentry).place(x=10, y=20)


def userregister():
    name1 = name.get()
    gender1 = var.get()
    email1 = email.get()
    address1 = address.get()
    pnumber1 = pnumber.get()
    uname1 = uname.get()

    gen = ''
    if gender1 == 1:
        gen = 'Male'
    else:
        gen = 'Female'

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='1faceiotdb')
    cursor = conn.cursor()
    cursor.execute("insert into regtb values('','" + name1 + "','" + str(
        gen) + "','" + pnumber1 + "','" + email1 + "','" + address1 + "','" + uname1 + "')")
    conn.commit()
    conn.close()
    register_sucess()


def facedet1():
    import LiveRecognition1  as liv

    liv.att()
    del sys.modules["LiveRecognition1"]
    newmotion()


def newmotion():
    import cv2

    cap = cv2.VideoCapture(0)

    # get initial frame
    ret, frame1 = cap.read()
    gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)

    # set up parameters for motion detection
    motion_threshold = 30
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))

    count = 0

    while True:
        # read current frame
        ret, frame2 = cap.read()
        if not ret:
            break
        gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)

        # calculate difference between frames
        frame_diff = cv2.absdiff(gray1, gray2)

        # threshold the difference to detect motion
        _, thresh = cv2.threshold(frame_diff, motion_threshold, 255, cv2.THRESH_BINARY)

        # apply morphological operations to reduce noise and fill gaps
        thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)

        # find contours of motion
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # draw bounding box around each contour and track motion
        for contour in contours:
            (x, y, w, h) = cv2.boundingRect(contour)
            cv2.rectangle(frame2, (x, y), (x + w, y + h), (0, 255, 0), 2)
            count += 1
            if count == 400:
                count = 0
                print('motion')
                import winsound
                import datetime
                import time
                ts = time.time()
                date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                now = time.localtime()
                filename = 'alert.wav'
                winsound.PlaySound(filename, winsound.SND_FILENAME)
                sendmsg("9626746446", "Motion Detected")

                cv2.waitKey(1)
                cap.release()
                cv2.destroyAllWindows()

                cv2.VideoCapture.release(cap)
                test()

                #print(now.tm_hour)
                #if  now.tm_hour >= 12:
                    #if now.tm_min > 00:




                # cap.release()
                # cv2.destroyAllWindows()

        cv2.imshow("Motion Detection and Tracking", frame2)
        if cv2.waitKey(1) == ord('q'):
            break

        # update current frame
        gray1 = gray2

    cap.release()
    cv2.destroyAllWindows()


def test():
    import cv2
    cv2.waitKey(5)
    cv2.destroyAllWindows()
    facedet1()


def sendmsg(targetno,message):
    import requests
    requests.post(
        "http://sms.creativepoint.in/api/push.json?apikey=6555c521622c1&route=transsms&sender=FSSMSS&mobileno=" + targetno + "&text=Dear customer your msg is " + message + "  Sent By FSMSG FSSMSS")



def main_account_screen():
    global main_screen
    main_screen = Tk()
    width = 600
    height = 600
    screen_width = main_screen.winfo_screenwidth()
    screen_height = main_screen.winfo_screenheight()
    x = (screen_width / 2) - (width / 2)
    y = (screen_height / 2) - (height / 2)
    main_screen.geometry("%dx%d+%d+%d" % (width, height, x, y))
    main_screen.resizable(0, 0)
    # main_screen.geometry("300x250")
    main_screen.title("Anomaly Detection")

    Label(text="Anomaly Detection", bg="turquoise", width="300", height="5", font=("Calibri", 16)).pack()

    Button(text="Training", font=(
        'Verdana', 15), height="2", width="30", command=Adminlog, highlightcolor="black").pack(side=TOP)
    Label(text="").pack()

    Button(text="Testing", font=('Verdana', 15), height="2", width="30", command=newmotion).pack(side=TOP)

    Label(text="").pack()

    main_screen.mainloop()


main_account_screen()
