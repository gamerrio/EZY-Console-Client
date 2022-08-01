import gi


gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class Handler:
    def onDestroy(self, *args):
        Gtk.main_quit()

    def onButtonPressed(self, button):
        print("Hello World!")


builder = Gtk.Builder()
builder.add_from_file("UI.glade")
win = builder.get_object("window1")
builder.connect_signals(Handler())
win.show_all()
Gtk.main()

