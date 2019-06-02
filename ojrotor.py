# coding: utf-8
 
from Tkinter import * 
import tkMessageBox
import socket
import sys
import time
import os
import threading
import math
import configparser

rotor_offset=0
old_rotor=999
new_rotor=997
direction=""
direction2=""
refresh=3
rotor=998

def rot(rotor):
        if (rotor>=360):rotor=rotor-360
        if (rotor<0):rotor=rotor+360
	return rotor

def lecture():
	global old_rotor,rotor,new_rotor
        sock.sendall("p")
	data = sock.recv(4096)
	if (data.find("RPRT")>-1):return
	rotor=int(float(data.split("\n")[0]))
	rotor=int(rot(rotor+rotor_offset))
	global refresh,refreshc
	if (rotor<>old_rotor):
		refreshc=0
		refresh=1
		rotord=rot(80-rotor)
		rotorf=20
                text1.config(text =str(rotor)+"°")
		global direction
		canvas.delete(direction)
		direction=canvas.create_arc(26, 26, 173, 173,start=rotord, extent=rotorf,fill="green",style="pieslice",width=0)
		old_rotor=rotor
	        fenetre.update()
	if (new_rotor==rotor):
		text2.config(text="")
		refresh=3
	refreshc=refreshc+1
	time.sleep(refresh/5)
        time.sleep(refresh/5)
        time.sleep(refresh/5)
        time.sleep(refresh/5)
        time.sleep(refresh/5)


def getorigin(eventorigin):
	global rotor_offset
	x0 = eventorigin.x
	y0 = eventorigin.y
	myradians = math.atan2(100-y0, 100-x0)
	mydegrees = int(rot(math.degrees(myradians)-90))
#	print(mydegrees)
	if (rotor<>mydegrees):
		global sock
		global new_rotor
		new_rotor=mydegrees
		sock.sendall("P "+str(int(rot(mydegrees-rotor_offset)))+" 0\n")
		text2.config(text=str(mydegrees)+"°")
		mydegrees =rot(89-mydegrees)
		global direction2
		canvas.delete(direction2)
		direction2=canvas.create_arc(26, 26, 173, 173,start=mydegrees, extent=2,fill="red",style="pieslice",width=0)

def start_new_thread():
#	global refreshc,refresh ,old_rotor,rotor,thread,thread_stop
	global refresh,refreshc
	if (refreshc>3):
		refresh=3
                refreshc=0
#	thread_stop= threading.Event()
	thread = threading.Thread(target=lecture())
	thread.start()
#	time.sleep(0.05)

def quit():
	global fenetre
#,thread_stop
#	thread_stop.set()
        config = configparser.ConfigParser()
        config.read(os.path.dirname(os.path.abspath(__file__))+"/ojrotor.cfg")
        read=list(config.items('DEFAULT'))
	configw = configparser.ConfigParser()
        for k,v in read:
		if (k.find("window_")== -1):
			configw.set('DEFAULT', k,v)
#	print(fenetre.winfo_screenwidth())
	configw.set('DEFAULT', 'window_x',str(fenetre.winfo_width()))
        configw.set('DEFAULT', 'window_y', str(fenetre.winfo_height()-40))
	print(list(configw.items('DEFAULT')))
        with open(os.path.dirname(os.path.abspath(__file__))+"/ojrotor.cfg", 'w') as configfile:
               configw.write(configfile)
	fenetre.quit()
	fenetre.destroy()
	sys.exit()

config = configparser.ConfigParser()
config.read(os.path.dirname(os.path.abspath(__file__))+"/ojrotor.cfg")
rotor_offset=float(config.get("DEFAULT","rotor_offset") )
rotctl_serveur=config.get("DEFAULT","rotctl_serveur")
rotctl_port=int(config.get("DEFAULT","rotctl_port"))
old_rotor=999
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = (rotctl_serveur,rotctl_port)
sock.connect(server_address)
fenetre = Tk()
fenetre.resizable(0, 0) 
fenetre.geometry("210x220+"+config.get("DEFAULT","window_x")+"+"+config.get("DEFAULT","window_y"))
fenetre.config(bg="white")
fenetre.title("FG8OJ Rotator")
fenetre.protocol("WM_DELETE_WINDOW", quit)

path = os.path.abspath(__file__)
photo = PhotoImage(file=os.path.dirname(path)+"/boussole.png")
canvas = Canvas(fenetre,width=200, height=200,bd=0, highlightthickness=0, relief='ridge')
canvas.config(bg='white')
canvas.create_image(0, 0, anchor=NW, image=photo)
canvas.bind("<Button-1>",getorigin)
canvas.pack(pady=10)
canvast1 = Canvas(fenetre,width=20, height=20,bd=0, highlightthickness=0, relief='ridge')
canvast1.place(x=0, y=0)
text1 = Label(canvast1, bg="white",fg="green",font=("Helvetica", 15),text="360°",justify="center")
text1.pack()
canvast2 = Canvas(fenetre,width=20, height=20,bd=0, highlightthickness=0, relief='ridge')
canvast2.place(x=210, y=0,anchor=NE)
text2 = Label(canvast2, bg="white",fg="red",font=("Helvetica", 15),text="",justify="right")
text2.pack()
fenetre.update()

refreshc=0
while True:
	fenetre.update()
        start_new_thread()
	time.sleep(0.1)
sock.close()


mainloop()
