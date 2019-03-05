#!/usr/bin/env python3

"""

Copyright (C) CheesecakeCG Interactive Media

This file is part of M!nk Link.

M!nk Link is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

M!nk Blink is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with M!nk Blink.  If not, see <http://www.gnu.org/licenses/>.

Author: Christopher D. - "CheesecakeCG" - cheesecakecgcontact@gmail.com

"""

import os
import sys
import gi
import validators
gi.require_version('Gtk', '3.0')
gi.require_version('WebKit2', '4.0')
gi.require_version('Soup', '2.4')
from gi.repository import Gtk, Soup, WebKit2
import sqlite3

class Gui:

        def on_window_destroy(self, object, data=None):
                print("quit with cancel")
                Gtk.main_quit()
                quit()
        def on_webview_load_changed(self, object, data=None):
                self.uri_input.set_text(self.webview.get_uri())
                if not self.webview.get_title() is None:
                        self.window.set_title(self.webview.get_title() + " | mink link")
                else:
                        self.window.set_title("loading... | mink link")
        
        def on_forward_btn_clicked(self, object, data=None):
                print("Going Forward")
                self.webview.go_forward()
        def on_back_btn_clicked(self, object, data=None):
                print("Going Back")
                self.webview.go_back()
        def on_reload_btn_clicked(self, object, data=None):
                print("Reloading Page!")
                self.webview.reload()
        def on_uri_input_activate(self, object, data=None):
                uri = self.uri_input.get_text()
                if not validators.url(uri):
                    if (any(sub in uri for sub  in [".com", ".net", ".io", ".org", ".xyz", ".co", ".gov", ".ca"])):
                        uri = "https://" + uri
                    else: 
                        uri = "https://www.google.com/search?q=" + uri
                print("Loading Page: ", uri)
                self.webview.load_uri(uri)
        def policy_decision_requested(view, frame, request, mimetype, policy_decision):
                if mimetype != 'text/html':
                        policy_decision.download()
                        return True
        def download_requested(view, download):
                name = download.get_suggested_filename()
                path = os.path.join(
                        GLib.get_user_special_dir(GLib.UserDirectory.DIRECTORY_DOWNLOAD),
                        name
                )
                urlretrieve(download.get_uri(), path)  # urllib.request.urlretrieve
                return False
        def on_webview_create(self, object, data=None):
                print(data)
        
                
# This is our init part where we connect the signals
        def __init__(self):
                
                self.wdm = WebKit2.WebsiteDataManager()
                self.context = WebKit2.WebContext.new_with_website_data_manager(self.wdm)
                self.context.get_cookie_manager().set_persistent_storage("~/.config/minklink/cookies", False)
                
                self.webview = WebKit2.WebView()
                tmp = WebKit2.Settings()
                #tmp = None
                
                
                self.gladefile = os.path.join(os.path.abspath(os.path.dirname(__file__)),"gui/main.glade") # store the file name
                self.builder = Gtk.Builder() # create an instance of the gtk.Builder
                self.builder.add_from_file(self.gladefile) # add the xml file to the Builder

                self.builder.connect_signals(self)
                
                self.header = self.builder.get_object("header")
                self.reload_btn = self.builder.get_object("reload_btn")
                self.forward_btn = self.builder.get_object("forward_btn")
                self.back_btn = self.builder.get_object("back_btn")
                self.webview = self.builder.get_object("webview")
                self.uri_input = self.builder.get_object("uri_input")
                self.window = self.builder.get_object("window") # This gets the 'note_window' object
                
                
                #self.wdm.base_cache_directory = "~/.config/minklink/cache"
                #self.wdm.base_data_directory = "~/.config/minklink/data"
                #self.wdm.disk_cache_directory = "~/.cache/minklink"
                #self.webview.get_context().set_process_model(WebKit2.ProcessModel.MULTIPLE_SECONDARY_PROCESSES)
                self.webview.get_context().get_cookie_manager().set_persistent_storage("/home/chrisd/.config/minklink/cookiesq", WebKit2.CookiePersistentStorage(1))
                
                self.webview.load_uri("https://google.com")
                
                self.window.show() # this shows the 'note_window' object
                
                

if __name__ == "__main__":
    main = Gui() # create an instance of our class
    Gtk.main() # run the darn thing
