from re import T
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk ,Gdk,GLib,Gio

import os
import sys 
from subprocess import Popen, PIPE, STDOUT
import threading

#Handles the events like button presses
class Handler:
    def onDestroy(self, *args):
        Gtk.main_quit()

    def OnJoinPressed(self, button):
        startup_line = name.get_text() +" " + password.get_text()+" "+ip.get_text()
        textbuffer = output.get_buffer()
        textbuffer.set_text(startup_line,-1)
        notebook = builder.get_object("notebook")
        #opens the new tab with vb and adds it to the notebook
        page = chat_area()
        print(notebook)
        notebook.append_page(page, Gtk.Label(ip.get_text()))
        win.show_all()


#layout of the chatting area        
def chat_area():
            vb = Gtk.VBox()
            hb = Gtk.HBox()
            output = Gtk.TextView()
            sw = Gtk.ScrolledWindow()
            sw.add_with_viewport(output)
            tv = vb.pack_start(sw,expand=True,fill=True,padding=0)
            btn = Gtk.Button()

            snd_image = Gtk.Image()
            snd_image.set_from_file("./send_white.svg")
            btn.add(snd_image)
            
            ety = Gtk.Entry()
            ety.props.show_emoji_icon = True
            hb.pack_start(ety, expand = True, fill = True, padding = 0)
            hb.pack_start(btn, expand = False, fill = True, padding = 0)
            vb.pack_start(hb, expand = False, fill = True, padding = 6)

            #starts a new thread for taking the chat from a console window so it does not break GUI loop
            threading.Thread(target=chat, args=(output,btn,ety,)).start()
            create_notif()
            return vb


def chat(output,btn,ety):
    if not os.path.exists("./MinecraftClient.exe"):
        print("MinecraftClient.exe not found")
        return
    if password.get_text() == "":
        password_output = '-'
    else:
        password_output = password.get_text()
    p = Popen(['mono', 'MinecraftClient.exe',name.get_text(),password_output,ip.get_text(),'BasicIO'],
          stdout=PIPE, stderr=STDOUT,stdin=PIPE)
    def send_input(dummy,p,ety,*args):
        text=ety.get_text()+'\n'
        p.stdin.write(text.encode())
        p.stdin.flush()
        ety.set_text('')

    btn.connect("clicked",send_input,p,ety)
    ety.connect("activate",send_input,p,ety)
    with p.stdout:
        for line in iter(p.stdout.readline, b''):
            Gdk.threads_add_idle(GLib.PRIORITY_DEFAULT_IDLE,append_text, output,line.decode("utf-8")),

    p.wait()
    return p

#FIXME: this needs to be efficient and not take too much time 
#appends the text in Textview
def append_text(output,text):
    #removes color codes from the text
    def rm_color_code(text,text_buffer):
        while "§" in text:
            no = text.find("§")
            text = text.replace(text[no+1]," ")
            text.replace("§","")
        print(text)
        text_buffer.insert(end_iter,text)
    text_buffer = output.get_buffer()
    end_iter = text_buffer.get_end_iter()
    #schduler to do job whithout blocking the GUI loop
    threading.Thread(target=rm_color_code, args=(text,text_buffer)).start()

def create_notif():
    notif = Gio.Notification()
    notif.set_title("Opened a new tab")
    notif.set_body("you just opened a new tab")
    App.send_notification(None, notif)
    return notif



#Getting the UI Components
builder = Gtk.Builder()
builder.add_from_file("UI.glade")
win = builder.get_object("window1")
name = builder.get_object("name")
password = builder.get_object("pass")
password.set_visibility(False)
ip = builder.get_object("ip")
output = builder.get_object("output")
def create_window(*args):
    builder.connect_signals(Handler())
    win.show_all()
    Gtk.main()

App = Gtk.Application() 
App.connect("activate", create_window)

if __name__ == "__main__":
    App.run(sys.argv)
