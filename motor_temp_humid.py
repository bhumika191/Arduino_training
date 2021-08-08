#import modules
 
from tkinter import *
import os
import time
import serial
import threading
import continuous_threading
# Designing window for registration

ser = serial.Serial(port='/dev/ttyUSB0', baudrate=9600)
 
def register():
    global register_screen
    register_screen = Toplevel(main_screen)
    register_screen.title("Register")
    register_screen.geometry("300x250")
 
    global username
    global password
    global username_entry
    global password_entry
    username = StringVar()
    password = StringVar()
 
    Label(register_screen, text="Please enter details below", bg="lightblue").pack()
    Label(register_screen, text="").pack()
    username_lable = Label(register_screen, text="Username * ")
    username_lable.pack()
    username_entry = Entry(register_screen, textvariable=username)
    username_entry.pack()
    Label(register_screen, text="").pack()
    password_lable = Label(register_screen, text="Password * ")
    password_lable.pack()
    password_entry = Entry(register_screen, textvariable=password, show='*')
    password_entry.pack()
    Label(register_screen, text="").pack()
    Button(register_screen, text="Register", width=10, height=1, bg="lightblue", command = register_user).pack()
 
 
# Designing window for login 
 
def login():
    global login_screen
    login_screen = Toplevel(main_screen)
    login_screen.title("Login")
    login_screen.geometry("300x250")
    Label(login_screen, text="Please enter details below to login").pack()
    Label(login_screen, text="").pack()
 
    global username_verify
    global password_verify
 
    username_verify = StringVar()
    password_verify = StringVar()
 
    global username_login_entry
    global password_login_entry
 
    Label(login_screen, text="Username * ").pack()
    username_login_entry = Entry(login_screen, textvariable=username_verify)
    username_login_entry.pack()
    Label(login_screen, text="").pack()
    Label(login_screen, text="Password * ").pack()
    password_login_entry = Entry(login_screen, textvariable=password_verify, show= '*')
    password_login_entry.pack()
    Label(login_screen, text="").pack()
    Button(login_screen, text="Login", width=10, height=1, command = login_verify).pack()
    
 
# Implementing event on register button
 
def register_user():
 
    username_info = username.get()
    password_info = password.get()
 
    file = open(username_info, "w")
    file.write(username_info + "\n")
    file.write(password_info)
    file.close()
 
    username_entry.delete(0, END)
    password_entry.delete(0, END)

    Label(register_screen, text="").pack()
    Label(register_screen, text="Registration Success", fg="green", font=("calibri 11 bold")).pack()
 
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
            login_sucess()
 
        else:
           # password_not_recognised
            Label(login_screen, text="").pack()
            Label(login_screen, text="Wrong Password", fg="red",font="calibri 11 bold").pack()
 
    else:
        #user_not_found
        Label(login_screen, text="").pack()
        Label(login_screen, text="user not found", fg="red",font="calibri 11 bold").pack()
 
# Designing popup for login success
 
def login_sucess():
     Label(login_screen, text="").pack()
     Label(login_screen, text="login successful", fg="green",font="calibri 11 bold").pack()
     login_screen.after(10000, lambda: login_screen.destroy() )
     led_motor()


def led_motor():
    print("Reset Arduino")
    ser.write(bytes('L', 'UTF-8'))

    global Ledmotor_screen
    Ledmotor_screen = Toplevel(main_screen)
    Ledmotor_screen.title("LED & MOTOR Control")
    Ledmotor_screen.geometry("300x500")

    t1 = continuous_threading.PeriodicThread(0.1, readserial)
    t1.start()

        #label to display the status
    global varLabel    
    varLabel = IntVar()
    tkLabel = Label(textvariable=varLabel, )
    varLabel.set("LED & MOTOR STATUS")
    tkLabel.pack()
    
    #button1 - ON
    button1 = IntVar()
    button1state = Button(Ledmotor_screen,
        text="START",
        command=on_button,
        height = 3,
        width = 3,
        bg='darkgreen',
        activebackground='green',
        fg='white'
    )
    button1state.pack(side='top', ipadx=10, padx=10, pady=15)
    
    #button2 - OFF
    button2 = IntVar()
    button2state = Button(Ledmotor_screen,
        text="STOP",
        command=stop_button,
        height = 3,
        width = 3,
        bg='darkred',
        activebackground='red',
        fg='white'
    )
    button2state.pack(side='top', ipadx=10, padx=10, pady=15)
    
    #button1 - Rev
    button3 = IntVar()
    button3state = Button(Ledmotor_screen,
        text="Reverse",
        command=reverse_button,
        height = 3,
        width = 3,
        bg='darkgreen',
        activebackground='green',
        fg='white'
    )
    button3state.pack(side='top', ipadx=10, padx=10, pady=15)

    #Quit button
    tkButtonQuit = Button(
        Ledmotor_screen,
        text="Quit",
        command=quit_button,
        height = 3,
        width = 5,
        bg='black',
        activebackground='grey',
        fg='white'
    )
    tkButtonQuit.pack(side='top', ipadx=10, padx=10, pady=15)

val1 = 0
index = []


def readserial():
    global val1
    ser_bytes = ser.readline()
    ser_bytes = ser_bytes.decode("utf-8")
    print(ser_bytes.rstrip())
    val1 = ser_bytes
    index.append(val1)
    
    if len(index) == 1:
        display1 = Label(Ledmotor_screen,text=index[0]).place(x=60,y=400)

    elif len(index) == 2:
        #display1 = tk.Label(tkTop,text=index[0]).place(x=10,y=10)
        display2 = Label(Ledmotor_screen,text=index[1]).place(x=50,y=430)
        index.clear()
    

    time.sleep(0.5)

 
def quit_button():
    ser.write(bytes('L', 'UTF-8'))
    Ledmotor_screen.destroy()
 
def on_button():
    varLabel.set("Motor forward, LED ON ")
    ser.write(bytes('H', 'UTF-8'))
 
def stop_button():
    varLabel.set("Motor off, LED OFF")
    ser.write(bytes('L', 'UTF-8'))

def reverse_button():
    varLabel.set("Motor Reverse, LED ON")
    ser.write(bytes('R', 'UTF-8'))
   
# def red_alert():
#     b = ser.readline.decode.rstrip()         # read a byte string
#     flt = float(b)        # convert string to float
#     print(flt)
#     if flt == 'L':
#       print("warning")
 
val1 = 0

index = []

def readserial():
    global val1
    ser_bytes = ser.readline()
    ser_bytes = ser_bytes.decode("utf-8")
    print(ser_bytes.rstrip())
    val1 = ser_bytes
    index.append(val1)
    
    if len(index) == 1:
        display1 = Label(Ledmotor_screen,text=index[0]).place(x=60,y=400)

    elif len(index) == 2:
        #display1 = tk.Label(tkTop,text=index[0]).place(x=10,y=10)
        display2 = Label(Ledmotor_screen,text=index[1]).place(x=50,y=430)

    if len(index) == 2:
        #print("Done")
        index.clear()
    
    time.sleep(0.5)


 
# Designing Main(first) window
 
def main_account_screen():
    global main_screen
    main_screen = Tk()
    main_screen.geometry("300x250")
    main_screen.title("Account Login")
    Label(text="Select Your Choice", bg="blue", width="300", height="2", font=("Calibri", 13)).pack()
    Label(text="").pack()
    Button(text="Login", height="2", width="30", command = login).pack()
    Label(text="").pack()
    Button(text="Register", height="2", width="30", command=register).pack()
    main_screen.mainloop()
 
 
 
# if __name__ == "__main__": 
main_account_screen()


