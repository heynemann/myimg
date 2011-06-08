#!/usr/bin/python
# -*- coding: utf-8 -*-

import gtk
import appindicator

def menuitem_response(w, buf):
    print buf

if __name__ == "__main__":
    ind = appindicator.Indicator ("example-simple-client",
                              "indicator-messages",
                              appindicator.CATEGORY_APPLICATION_STATUS)
    ind.set_status (appindicator.STATUS_ACTIVE)
    ind.set_attention_icon ("indicator-messages-new")

    # create a menu
    menu = gtk.Menu()

    # create some 
    for i in range(3):
        buf = "Test-undermenu - %d" % i

    menu_items = gtk.MenuItem(buf)

    menu.append(menu_items)

    # this is where you would connect your menu item up with a function:

    # menu_items.connect("activate", menuitem_response, buf)

    # show the items
    menu_items.show()

    ind.set_menu(menu)

    gtk.main()


#def main():
    ## create a new Status Icon
    #staticon = gtk.StatusIcon()
    #staticon.set_from_file("/home/heynemann/Desktop/dropbox.png")
    #staticon.set_blinking(True)
    #staticon.set_visible(True)

    ## invoking the main()
    #gtk.main()

#if __name__ == '__main__':
    #main()
