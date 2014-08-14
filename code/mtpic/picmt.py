#!/usr/bin/env python
#v2
import sys
import os

import pygtk
#pygtk.require('2.0')
import gtk

from subprocess import call

vargs={"cur":0}

def movefile(srcfile,tardir):
	try:
		excmd = call(["mv",srcfile, tardir])
		if excmd < 0:
                    print >>sys.stderr, "#Move " + srcfile + \
				" failed,as killed by signal:", -excmd
	except OSError,e:
		print >>sys.stderr,"#Move " + srcfile + "  failed:",e

def setwallp(imgf):
	try:
		os.system("cp "+imgf+" /tmp/picmtwapp.jpg")
		os.system("gsettings set org.gnome.desktop.background picture-uri "+"file:///tmp/picmtwapp.jpg")
	except OSError,e:
		print >>sys.stderr,"#Set wallpaper failed:",e


class PyApp(gtk.Window):
	def showImg(self,imgfile,gtkImg,back=None):
		try:
			pixbuf = gtk.gdk.pixbuf_new_from_file(imgfile)
			pwith = pixbuf.get_width()
			pheight = pixbuf.get_height()
			while pwith >1000 or pheight > 850:
				pheight = int(pheight * 0.99)
				pwith = int(pwith *0.99)
			pixbuf = pixbuf.scale_simple(pwith, pheight,gtk.gdk.INTERP_BILINEAR)
                        #self.resize(pixbuf.get_width(),pixbuf.get_height())
                        gtkImg.set_from_pixbuf(pixbuf)
                        self.set_title(str(vargs["cur"]) + " : " + imgfile)
		except Exception, e:
			print e.message
                        self.set_title(str(vargs["cur"]) + "Open: ["+imgfile+"] failed")

	def on_shiftImage(self, widget, data,gtkImg,flist,trashdir):
                newcur=vargs["cur"]
		try:
			mouse_pressed=data.button
			if mouse_pressed == 3: #rightclick
                            movefile(flist[newcur],trashdir)
                            #print "#Movefile",flist[newcur],trashdir
                        newcur+=1
		except AttributeError:
			key_pressed=data.keyval
			if key_pressed == 65535 or key_pressed == 97: #a / del pressed to del a file
                            movefile(flist[newcur],trashdir)
                            newcur+=1
			elif key_pressed == 65361 and newcur >0: #left <- pressed
                            newcur-=1
			elif key_pressed == 112:
                            setwallp(flist[newcur])
                        else:
                            newcur+=1
		finally:
                        self.showImg(flist[newcur],gtkImg)
			vargs["cur"]=newcur
                        print "#Viewed:",vargs["cur"]

	def __init__(self,flist,trashdir):
		super(PyApp, self).__init__()

		self.set_title("PicMT")
		self.set_size_request(1400,800)
		self.modify_bg(gtk.STATE_NORMAL, gtk.gdk.Color(2550, 2550, 2550))
		self.set_position(gtk.WIN_POS_CENTER)
		self.add_events(gtk.gdk.KEY_PRESS_MASK |
			gtk.gdk.POINTER_MOTION_MASK |
			gtk.gdk.BUTTON_PRESS_MASK |
			gtk.gdk.SCROLL_MASK)

                gtkImg = gtk.Image()
		self.connect("button_press_event", self.on_shiftImage, gtkImg,
				flist,trashdir)
		self.connect("key_press_event", self.on_shiftImage, gtkImg,
				flist,trashdir)
		self.connect("destroy", gtk.main_quit)

                fix = gtk.Fixed()
                fix.put(gtkImg,0, 0)
                self.add(fix)
		self.showImg(flist[vargs["cur"]],gtkImg)
                print "#Viewed:",vargs["cur"]
		self.show_all()


if __name__ == "__main__":
	print '''
	Usage:
	Set wallpaper : p
	back : <--
	Quickmove: a, del , [rightClick]
		'''
	picfiles=[]
	print "*Reading files list..."
        filelist = open(sys.argv[1],'r')
        for line in filelist.readlines():
            picfiles.append(line[:-1])

	print "*Read in ",len(picfiles)," files!!!"

	trashdir="/data/xarc/imgs/test/"
	try:
		if sys.argv[2] >0: vargs["cur"]=int(sys.argv[2])
	except Exception:
		vargs["cur"]=0
	myapp = PyApp(picfiles,trashdir)
	gtk.main()



