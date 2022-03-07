from setup import *

config = configparser.ConfigParser()
config.read(src_user_config)


class UI(QWidget):
    def __init__(self):
        super().__init__()
        # self.setWindowTitle(app_name)
        # self.setFixedSize(1000, 600)
        # self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
        # self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.showFullScreen()

        # getResolution = QtWidgets.QDesktopWidget().screenGeometry(0)
        # self.screen_x = getResolution.width()  # Screen resolution x
        # self.screen_y = getResolution.height()  # Screen resolution y
        # self.screen_center = getResolution.center()

        ################################################################################
        ## Variables
        ################################################################################
        self.filesToRestore = []
        self.filesToRestoreWithSpace = []

        self.copyCmd = "rsync -avruzh"
        self.count = 0
        self.countTime = 0

        ################################################################################
        ## Read ini
        ################################################################################
        self.getHDName = config['EXTERNAL']['name']
        self.getExternalLocation = config['EXTERNAL']['hd']

        ################################################################################
        ## Read restore settings
        ################################################################################
        with open(src_restore_settings, 'r') as self.reader:
            self.reader = self.reader.readline()
            self.reader = self.reader.replace(':', '').strip()
            print(f"Search files from : {self.reader}")

        self.widgets()

    def widgets(self):
        ################################################################################
        ## Base layouts
        ################################################################################
        self.baseVLayout = QVBoxLayout()
        self.baseVLayout.setAlignment(QtCore.Qt.AlignVCenter)
        self.baseVLayout.setContentsMargins(20, 20, 20, 20)

        self.baseHLayout = QHBoxLayout()
        self.baseHLayout.setAlignment(QtCore.Qt.AlignHCenter)
        self.baseHLayout.setSpacing(20)

        self.buttonHLayout = QHBoxLayout()
        self.buttonHLayout.setSpacing(20)
        self.buttonHLayout.setContentsMargins(20, 20, 20, 20)

        self.updownVLayout = QVBoxLayout()
        self.updownVLayout.setContentsMargins(0, 0, 0, 0)

        self.timeVLayout = QVBoxLayout()
        self.timeVLayout.setAlignment(QtCore.Qt.AlignVCenter)
        self.timeVLayout.setSpacing(20)
        self.timeVLayout.setContentsMargins(20, 0, 20, 0)

        ################################################################################
        ## ScrollArea
        ################################################################################
        scrollWidget = QWidget()
        scrollWidget.setStyleSheet("""
            background-color: rgb(24, 25, 26);
        """)

        scroll = QScrollArea()
        scroll.setFixedSize(1000, 600)
        # scroll.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        # scroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet(
            "QScrollBar::handle"
                "{"
                    "background : rgb(58, 59, 60);"
                "}"
            "QScrollBar::handle::pressed"
                "{"
                    "background : rgb(68, 69, 70);"
                "}"
            )
        scroll.setWidget(scrollWidget)

        ################################################################################
        ## Files vertical layout
        ################################################################################
        self.filesGridLayout = QGridLayout(scrollWidget) # scrollWidget
        self.filesGridLayout.setAlignment(QtCore.Qt.AlignHCenter)
        self.filesGridLayout.setContentsMargins(20, 20, 20, 20)
        self.filesGridLayout.setSpacing(20)

        ################################################################################
        ## Cancel button
        ################################################################################
        self.cancelButton = QPushButton()
        self.cancelButton.setText("Cancel")
        self.cancelButton.setFont(QFont(font4, 14))
        self.cancelButton.setFixedSize(120, 34)
        self.cancelButton.setEnabled(True)
        self.cancelButton.clicked.connect(lambda x: exit())
        self.cancelButton.setStyleSheet(
            "QPushButton"
                "{"
                    "background-color: rgb(58, 59, 60);"
                    "border: 0px;"
                    "border-radius: 5px;"
                "}"
            "QPushButton::hover"
                "{"
                    "background-color: rgb(68, 69, 70);"
                "}"
        )

        ################################################################################
        ## Restore button
        ################################################################################
        self.restoreButton = QPushButton()
        self.restoreButton.setText("Restore")
        self.restoreButton.setFont(QFont(font4, 14))
        self.restoreButton.setFixedSize(120, 34)
        self.restoreButton.setEnabled(False)
        self.restoreButton.setStyleSheet(
            "QPushButton"
                "{"
                    "background-color: rgb(58, 59, 60);"
                    "border: 0px;"
                    "border-radius: 5px;"
                "}"
            "QPushButton::hover"
                "{"
                    "background-color: rgb(68, 69, 70);"
                "}"
        )

        ################################################################################
        ## Up button
        ################################################################################
        self.upButton = QPushButton()
        self.upButton.setText("Up")
        self.upButton.setFont(QFont(font4, 12))
        self.upButton.setFixedSize(50, 50)
        self.upButton.clicked.connect(lambda x: self.get_date(True))
        self.upButton.setStyleSheet(
            "QPushButton"
                "{"
                    "background-color: rgb(58, 59, 60);"
                    "border: 0px;"
                    "border-radius: 5px;"
                "}"
            "QPushButton::hover"
                "{"
                    "background-color: rgb(68, 69, 70);"
                "}"
            )

        ################################################################################
        ## Down button
        ################################################################################
        self.downButton = QPushButton()
        self.downButton.setText("Down")
        self.downButton.setFont(QFont(font4, 12))
        self.downButton.setFixedSize(50, 50)
        self.downButton.clicked.connect(lambda x: self.get_date(False))
        self.downButton.setStyleSheet(
            "QPushButton"
                "{"
                    "background-color: rgb(58, 59, 60);"
                    "border: 0px;"
                    "border-radius: 5px;"
                "}"
            "QPushButton::hover"
                "{"
                    "background-color: rgb(68, 69, 70);"
                "}"
            )

        ################################################################################
        ## Label date
        ################################################################################
        self.labelDate = QLabel()
        self.labelDate.setFont(QFont(font2, 12))

        ################################################################################
        ## Current lcoation
        ################################################################################
        self.currentLocation = QLabel()
        self.currentLocation.setText(self.reader)
        self.currentLocation.setFont(QFont(font2, 28))

        ################################################################################
        ## Add widgets and Layouts
        ################################################################################
        # ButtonLayout
        self.updownVLayout.addStretch()
        self.updownVLayout.addWidget(self.upButton, 0, QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeft)
        self.updownVLayout.addWidget(self.labelDate, 0, QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeft)
        self.updownVLayout.addWidget(self.downButton, 0, QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeft)
        self.updownVLayout.addStretch()

        # ButtonHLayout
        self.buttonHLayout.addWidget(self.cancelButton, 0, QtCore.Qt.AlignVCenter | QtCore.Qt.AlignRight)
        self.buttonHLayout.addWidget(self.restoreButton, 0, QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeft)

        # BaseVLayout
        self.baseVLayout.addWidget(self.currentLocation, 0, QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft)
        self.baseVLayout.addStretch()
        self.baseVLayout.addLayout(self.baseHLayout, 0)
        self.baseVLayout.addLayout(self.buttonHLayout, 0)
        self.baseVLayout.addStretch()

        # BaseHLayout
        self.baseHLayout.addStretch(2)
        self.baseHLayout.addWidget(scroll, 0)
        self.baseHLayout.addLayout(self.updownVLayout, 1)
        self.baseHLayout.addLayout(self.timeVLayout, 1)

        self.setLayout(self.baseVLayout)

        self.get_date(None)

    def get_date(self, direction):
        ################################################################################
        ## Get available dates inside TMB
        ################################################################################
        try:
            self.dateFolders = []
            for output in os.listdir(f"{self.getExternalLocation}/TMB/"):
                self.dateFolders.append(output)
                self.dateFolders.sort(reverse= True, key=lambda date: datetime.strptime(date, "%d-%m-%y"))

        except FileNotFoundError:
            print("External not detected.")
            not_available_notification()
            exit()

        ################################################################################
        ## Dates up or down
        ################################################################################
        print("Date available: ", self.dateFolders)
        if direction == None:
            self.count = 0

        elif not direction:
            self.count += 1

        else:
            self.count -= 1

        getDate = self.dateFolders[self.count]
        ################################################################################
        ## Set current folder date
        ################################################################################
        self.labelDate.setText(getDate)

        self.get_time(getDate)

    def get_time(self, getDate):
        self.index = self.dateFolders.index(getDate)

        ################################################################################
        ## Disable up
        ################################################################################
        if self.index == 0:
            self.upButton.setEnabled(False)

        else:
            self.upButton.setEnabled(True)

        ################################################################################
        ## Disable down
        ################################################################################
        if (self.index + 1) == len(self.dateFolders):
            self.downButton.setEnabled(False)

        else:
            self.downButton.setEnabled(True)

        ################################################################################
        ## Remove items
        ################################################################################
        for i in range(self.timeVLayout.count()):
            item = self.timeVLayout.itemAt(i)
            widget = item.widget()
            widget.deleteLater()
            i -=1

        ################################################################################
        ## Get available times inside TMB
        ################################################################################
        timeFolders = []
        for getTime in os.listdir(f"{self.getExternalLocation}/TMB/{getDate}/"):
            timeFolders.append(getTime)

            ################################################################################
            ## Time button
            ################################################################################
            getTime = getTime.replace("-", ":")   # Change - to :
            self.timeButton = QPushButton()
            self.timeButton.setText(getTime)
            getTime = getTime.replace(":", "-")   # Change back : to -
            self.timeButton.setFont(QFont(font2, 12))
            self.timeButton.setFixedSize(100, 34)
            self.timeButton.setCheckable(True)
            self.timeButton.setAutoExclusive(True)
            self.timeButton.clicked.connect(lambda x, getTime=getTime: self.show_on_screen(getDate, getTime))
            self.timeButton.setStyleSheet(
                "QPushButton"
                    "{"
                        "background-color: rgb(58, 59, 60);"
                        "border-radius: 5px;"
                    "}"
                "QPushButton::hover"
                    "{"
                        "background-color: rgb(68, 69, 70);"
                    "}"
                "QPushButton::checked"
                    "{"
                        "background-color: rgb(24, 25, 26);"
                        "border: 1px solid white;"
                    "}"
                )
            self.countTime += 1

            ################################################################################
            ## Set current folder date
            ################################################################################
            self.timeVLayout.addWidget(self.timeButton, 1, QtCore.Qt.AlignRight)

        print("Time available: ", timeFolders)
        self.timeButton.setChecked(True)    # Auto selected that lastest one

        self.show_on_screen(getDate, getTime)

    def show_on_screen(self, getDate, getTime):
        ################################################################################
        ## Remove items
        ################################################################################
        for i in range(self.filesGridLayout.count()):
            item = self.filesGridLayout.itemAt(i)
            widget = item.widget()
            widget.deleteLater()
            i -=1

        ################################################################################
        ## Show available files
        ################################################################################
        try:
            count = 0
            vert = 0
            for output in os.listdir(f"{self.getExternalLocation}/TMB/{getDate}/{getTime}/{self.reader}"):
                if "." in output and not output.startswith("."):
                    print("Files: ", output)

                    self.buttonFiles =  QPushButton(self)
                    self.buttonFiles.setCheckable(True)
                    self.buttonFiles.setFixedSize(150, 150)
                    scaledHTML = 'width:"100%" height="250"'
                    self.buttonFiles.setToolTip(f"<img src={self.getExternalLocation}/TMB/{getDate}/{getTime}/{self.reader}/{output} {scaledHTML}/>")
                    self.buttonFiles.setStyleSheet(
                        "QPushButton"
                            "{"
                                "background-color: rgb(36, 37, 38);"
                                "border-top: 2px solid rgb(58, 59, 60);"
                                "border-radius: 5px;"
                            "}"
                        "QPushButton::hover"
                            "{"
                                "background-color: rgb(58, 59, 60);"
                            "}"
                        "QPushButton::checked"
                            "{"
                                "background-color: rgb(24, 25, 26);"
                                "border: 1px solid white;"
                            "}"
                    )
                    self.buttonFiles.clicked.connect(lambda x, output=output: self.add_to_restore(output, getDate, getTime))

                    ################################################################################
                    ## Preview
                    ################################################################################
                    # image = QLabel(self.buttonFiles)
                    # pixmap = QPixmap(f"{self.getExternalLocation}/TMB/{getDate}/{getTime}/{self.reader}/{output}")
                    # pixmap = pixmap.scaled(128, 128, QtCore.Qt.KeepAspectRatio)
                    # image.setPixmap(pixmap)

                    # Output preview
                    image = QLabel(self.buttonFiles)
                    scaledHTML = 'width:"100%" height="60"'
                    image.setText(f"<img  src={self.getExternalLocation}/TMB/{getDate}/{getTime}/{self.reader}/{output} {scaledHTML}/>")
                    image.move(20, 20)

                    ################################################################################
                    ## Text
                    ################################################################################
                    text = QLabel(self.buttonFiles)
                    text.setText(output.capitalize())
                    text.setFont(QFont(font2, 10))
                    text.move(20, 120)
                    text.setStyleSheet("""
                        color: white;
                        border: 0px;
                        background-color: transparent;
                                        """)

                    ################################################################################
                    ## Add layout and widgets
                    ################################################################################
                    self.filesGridLayout.addWidget(self.buttonFiles, vert, count)

                    count += 1
                    if count == 5:
                        count = 0
                        vert += 1

        except FileNotFoundError:
            print("Source files not found inside TMB.")

    def add_to_restore(self, output, getDate, getTime):
        ################################################################################
        ## Check for spaces inside output and sort them
        ################################################################################
        if not " " in output:
            if not output in self.filesToRestore:  # Check if output is already inside list
                self.filesToRestore.append(output)  # Add output to the list files to restore

            else:
                self.filesToRestore.remove(output) # Remove item if already in list

        else:
            if not output in self.filesToRestoreWithSpace:  # Check if output is already inside list
                self.filesToRestoreWithSpace.append(output)  # Add output to the list files to restore

            else:
                self.filesToRestoreWithSpace.remove(output) # Remove item if already in list

        print("")
        print("No spaces list   : ", self.filesToRestore)
        print("with spaces list : ", self.filesToRestoreWithSpace)

        ################################################################################
        ## Enable/Disable buttons
        ################################################################################
        if len(self.filesToRestore) or len(self.filesToRestoreWithSpace) >= 1:  # If something inside list
            self.restoreButton.setEnabled(True)
            self.upButton.setEnabled(False)
            self.downButton.setEnabled(False)

            for i in range(self.timeVLayout.count()):   # Hide times
                item = self.timeVLayout.itemAt(i)
                widget = item.widget()
                widget.hide()
                i -=1
        else:
            self.restoreButton.setEnabled(False)
            for i in range(self.timeVLayout.count()):   # Show times
                item = self.timeVLayout.itemAt(i)
                widget = item.widget()
                widget.show()
                i -=1

            if self.index != 0:     # If is not last/top date
                self.upButton.setEnabled(True)

            if not (self.index + 1) == len(self.dateFolders):   # If is not last/bottom date
                self.downButton.setEnabled(True)

        ################################################################################
        ## Connection restore button
        ################################################################################
        self.restoreButton.clicked.connect(lambda x: self.start_restore(getDate, getTime))

    def start_restore(self, getDate, getTime):
        config = configparser.ConfigParser()
        config.read(src_user_config)

        ################################################################################
        ## Restore files without spaces
        ################################################################################
        try:
            count = 0
            for _ in self.filesToRestore:
                sub.run(f"{self.copyCmd} {self.getExternalLocation}/TMB/{getDate}/{getTime}/{self.reader}/{self.filesToRestore[count]} {home_user}/{self.reader}/ &", shell=True)
                count += 1

            ################################################################################
            ## Restore files with spaces
            ################################################################################
            count = 0
            for _ in self.filesToRestoreWithSpace:
                sub.run(f'{self.copyCmd} {self.getExternalLocation}/TMB/{getDate}/{getTime}/{self.reader}/"{self.filesToRestoreWithSpace[count]}" {home_user}/{self.reader}/ &', shell=True)
                count += 1

        except:
            failed_restore()  # Notification
            exit()

        been_restored()  # Notification
        exit()

    def keyPressEvent(self, event):
        if event.key():  # == Qt.Key_Esc
            exit()


app = QApplication(sys.argv)
tic = time.time()

main = UI()
main.show()

toc = time.time()
print(f'Time Machine {(toc-tic):.4f} seconds')
app.exit(app.exec())