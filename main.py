import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

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
        notebook.append_page(page, Gtk.Label(ip.get_text()))
        win.show_all()


#layout of the chatting area        
def chat_area():
            vb = Gtk.VBox()
            hb = Gtk.HBox()
            tv = vb.pack_start(Gtk.TextView(),expand=True,fill=True,padding=0)
            btn = Gtk.Button()

            snd_image = Gtk.Image()
            snd_image.set_from_file("./send_white.svg")
            btn.add(snd_image)
            
            ety = Gtk.Entry()
            hb.pack_start(ety, expand = True, fill = True, padding = 0)
            hb.pack_start(btn, expand = False, fill = True, padding = 0)
            vb.pack_start(hb, expand = False, fill = True, padding = 6)
            return vb


#Getting the UI Components
builder = Gtk.Builder()
builder.add_from_file("UI.glade")
win = builder.get_object("window1")
name = builder.get_object("name")
password = builder.get_object("pass")
password.set_visibility(False)
ip = builder.get_object("ip")
output = builder.get_object("output")

builder.connect_signals(Handler())
win.show_all()
Gtk.main()

