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

