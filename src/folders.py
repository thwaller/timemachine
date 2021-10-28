import configparser
import sys
import os

from pathlib import Path
from PyQt5.uic import loadUi
from PyQt5.QtCore import QSize    
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import * 
from PyQt5.QtGui import *

home_user = str(Path.home())
get_home_folders = os.listdir(home_user)
src_user_config = "src/user.ini"
src_ui_folders = "src/folders.ui"
src_restore_icon = "src/icons/restore_48.png"

#dst_user_config = home_user+"/.local/share/timemachine/src/user.ini"
#dst_ui_folders = home_user+"/.local/share/timemachine/src/folders.ui"

#CONFIGPARSER
config = configparser.ConfigParser()
config.read(src_user_config)

class Folders(QMainWindow):
    def __init__(self):
        super(Folders, self).__init__()
        loadUi(src_ui_folders,self)
        self.button_folders_cancel.clicked.connect(self.on_button_folders_cancel_clicked)
        self.button_folders_done.clicked.connect(self.on_button_folders_done_clicked)
        
        #ADD BUTTONS AND IMAGES FOR EACH HD
        vertical = 15
        for self.folders in get_home_folders:
            if not self.folders.startswith('.'):
                other_folder_checkbox = QCheckBox(self.folders, self.folder_frame)
                other_folder_checkbox.setFixedSize(310, 22)
                other_folder_checkbox.move(120 ,vertical)
                vertical = vertical = + 60
                text = other_folder_checkbox.text()
                other_folder_checkbox.show()
                other_folder_checkbox.clicked.connect(lambda ch, text=text : self.on_desktop_checkbox_clicked(text))
                print(self.folders)
                
        #----Read user.config(backup folders choose)----#
        reader_desktop_folder = config['FOLDER']['desktop']        
        if reader_desktop_folder == "true":
            self.desktop_checkbox.setChecked(True)

        reader_documents_folder = config['FOLDER']['documents']        
        if reader_documents_folder == "true":
            self.documents_checkbox.setChecked(True)

        reader_downloads_folder = config['FOLDER']['downloads']        
        if reader_downloads_folder == "true":
            self.downloads_checkbox.setChecked(True)

        reader_music_folder = config['FOLDER']['music']        
        if reader_music_folder == "true":
            self.music_checkbox.setChecked(True)

        reader_pictures_folder = config['FOLDER']['pictures']        
        if reader_pictures_folder == "true":
            self.pictures_checkbox.setChecked(True)

        reader_videos_folder = config['FOLDER']['videos']        
        if reader_videos_folder == "true":
            self.videos_checkbox.setChecked(True)

    def on_desktop_checkbox_clicked(self):
        if self.desktop_checkbox.isChecked():
            cfgfile = open(src_user_config, 'w')
            config.set('FOLDER', 'desktop', 'true')
            config.write(cfgfile)
            cfgfile.close() 
            print("Desktop")
        else:
        #----Remove (.desktop) if user wants to----#
            cfgfile = open(src_user_config, 'w')
            config.set('FOLDER', 'desktop', 'false')
            config.write(cfgfile)
            cfgfile.close() 

    def on_documents_checkbox_clicked(self):
        if self.documents_checkbox.isChecked():
            cfgfile = open(src_user_config, 'w')
            config.set('FOLDER', 'documents', 'true')
            config.write(cfgfile)
            cfgfile.close() 
            print("Documents")
        else:
        #----Remove (.desktop) if user wants to----#
            cfgfile = open(src_user_config, 'w')
            config.set('FOLDER', 'documents', 'false')
            config.write(cfgfile)
            cfgfile.close() 

    def on_downloads_checkbox_clicked(self):
        if self.downloads_checkbox.isChecked():
            cfgfile = open(src_user_config, 'w')
            config.set('FOLDER', 'downloads', 'true')
            config.write(cfgfile)
            cfgfile.close() 
            print("Downloads")
        else:
        #----Remove (.desktop) if user wants to----#
            cfgfile = open(src_user_config, 'w')
            config.set('FOLDER', 'downloads', 'false')
            config.write(cfgfile)
            cfgfile.close() 

    def on_music_checkbox_clicked(self):
        if self.music_checkbox.isChecked():
            cfgfile = open(src_user_config, 'w')
            config.set('FOLDER', 'music', 'true')
            config.write(cfgfile)
            cfgfile.close() 
            print("Music")
        else:
        #----Remove (.desktop) if user wants to----#
            cfgfile = open(src_user_config, 'w')
            config.set('FOLDER', 'music', 'false')
            config.write(cfgfile)
            cfgfile.close() 

    def on_pictures_checkbox_clicked(self):
        if self.pictures_checkbox.isChecked():
            cfgfile = open(src_user_config, 'w')
            config.set('FOLDER', 'pictures', 'true')
            config.write(cfgfile)
            cfgfile.close() 
            print("Picture")
        else:
        #----Remove (.desktop) if user wants to----#
            cfgfile = open(src_user_config, 'w')
            config.set('FOLDER', 'pictures', 'false')
            config.write(cfgfile)
            cfgfile.close() 

    def on_videos_checkbox_clicked(self):
        if self.videos_checkbox.isChecked():
            cfgfile = open(src_user_config, 'w')
            config.set('FOLDER', 'videos', 'true')
            config.write(cfgfile)
            cfgfile.close() 
            print("Videos")
        else:
        #----Remove (.desktop) if user wants to----#
            cfgfile = open(src_user_config, 'w')
            config.set('FOLDER', 'videos', 'false')
            config.write(cfgfile)
            cfgfile.close() 

    def on_button_folders_cancel_clicked(self, button):
        exit()

    def on_button_folders_done_clicked(self, button):
        exit()

# main
app = QApplication(sys.argv)
main_screen = Folders()
widget = QtWidgets.QStackedWidget()
appIcon = QIcon(src_restore_icon)
widget.setWindowIcon(appIcon)
widget.addWidget(main_screen)
widget.setFixedHeight(405)
widget.setFixedWidth(445)
widget.setWindowTitle("Folders")
widget.show()
sys.exit(app.exec_())


