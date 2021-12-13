from PyQt5 import QtGui
from apiRef import getcoords, myapiref, refresh, write_cache, getlocation, refresh, singleapiref
import sys, os
from PyQt5 import QtCore
import datetime
import time
from PyQt5.QtCore import QDate, QTime, Qt, QSize, center
from PyQt5.QtWidgets import QSplashScreen,QCheckBox, QPushButton, QScrollArea ,QGridLayout,QFormLayout, QLineEdit, QStackedWidget, QWidget, QComboBox, QApplication, QMainWindow, QLabel, QVBoxLayout, QHBoxLayout, QFormLayout, QMessageBox
from PyQt5.QtGui import QImage, QIcon, QPixmap, QFont
from PIL import Image
import glob
from PIL.ImageQt import ImageQt
import requests
from io import BytesIO

class weather():
    def __init__(self):
        self.weatherapp = QApplication(sys.argv)
        self.central_widget = QWidget()
        self.main_window = QWidget()
        self.Stack = QStackedWidget()
        self.Stack.addWidget(self.central_widget)
        self.Stack.addWidget(self.main_window)
        self.layout = QGridLayout()
        self.layout1 = QFormLayout()
        self.ctemp = 0
        self.darkmode = 1
        self.tempstate = 1
        self.Info = []
        self.t = []
        self.Info.append("Current Location")
        self.path = sys.path[0]

    def mainwindow(self):
        temp = QWidget()
        templayout = QHBoxLayout()
        if self.window.isHidden() == True:
            self.window.show()
        l1 = QLabel("Enter City's Name") 
        l1.setFont(QFont('Times', 12))  #font size
        l1.setStyleSheet('background-color: rgba(255,255,255,0);')
        self.textbox = QLineEdit()
        self.textbox.setFont(QFont('Times', 15))
        self.textbox.setStyleSheet('background-color: rgba(255,255,255,50);')
        self.cbox = QComboBox()
        self.cbox.addItems(self.State)
        self.cbox.setFont(QFont('Times', 10))
        self.cbox.setStyleSheet('background-color: rgba(255,255,255,200);')
        templayout.addWidget(l1)
        templayout.addWidget(self.textbox)
        temp.setLayout(templayout)
        temp.setStyleSheet('background-color: rgba(255,255,255,175);')
        self.layout1.addRow(self.cbox)
        self.layout1.addRow(temp)


        b1 = QPushButton("Submit")
        b1.setFont(QFont('Times', 12))
        b1.setStyleSheet("background-color : rgba(60,100,240,200); \
                        color: black; \
                        border-style: outset;\
                        border-width: 2px; \
                        border-radius: 15px; \
                        border-color: black;\
                        padding: 4px") #changed the color of the submit button so its more visible 
        b2 = QPushButton("Cancel")
        b2.setFont(QFont('Times', 12))
        b2.setStyleSheet("background-color : rgba(240,70,35,200); \
                        color: black; \
                        border-style: outset;\
                        border-width: 2px; \
                        border-radius: 15px; \
                        border-color: black;\
                        padding: 4px") #changed the color of the cancel button so its more visible 
        b1.clicked.connect(self.Check_current)
        self.textbox.returnPressed.connect(lambda:self.Check_current)
        b2.clicked.connect(lambda: self.Stack.setCurrentIndex(0))
        self.layout1.addRow(b1, b2)

        self.layout1.setSpacing(20) #adds spacing between the QPushbuttons and the Textbook/label
        self.main_window.setLayout(self.layout1)

        if self.darkmode:
            self.main_window.setStyleSheet('background-color: rgba(50,50,50,255);')
        else:
            self.main_window.setStyleSheet('background-color: none;')  #changes background and font color for search new city window

    def weather_window(self):
        self.Info['Location'][0] = refresh(self.Info['Location'][0])
        self.splash.hide()
        if self.window.isHidden() == True:
            self.window.show()
        self.cb = QComboBox()
        temp = QWidget()
        templayout = QHBoxLayout()
        # l = []
        # for x in self.Info['Location']:
        #     l.append(x['City'])
        self.cb.addItems(self.t)
        self.cb.setFont(QFont('Times', 10))
        self.cb.setStyleSheet('background-color: rgba(255,255,255,225);')
        tc = QPushButton("Farenheight to Celsius")
        tc.setStyleSheet('background-color: rgba(255,255,255,200);')
        dm = QPushButton("Dark/Light Mode")
        dm.setStyleSheet('background-color: rgba(255,255,255,200);')
        tc.setFont(QFont('Times', 10))
        tc.clicked.connect(lambda:self.switchtempval())
        dm.clicked.connect(lambda:self.switchdarkmode())
        tc.move(400,0)
        templayout.addWidget(tc)
        templayout.addWidget(dm)
        temp.setLayout(templayout)
        self.layout.addWidget(temp)
        self.layout.addWidget(self.cb)
        weatherw = QWidget()
        weatherlayout = QHBoxLayout()

        Icon = self.Info["Location"][0]["current"]["weather"][0]["icon"]
        weather = self.Info["Location"][0]["current"]["weather"][0]["main"]
        #print(Icon)
        index = self.image_name.index(Icon)
        #print(index)
        pixmap = QPixmap(self.image_list[index]).scaled(QSize(150,150), Qt.KeepAspectRatio)
        
        label = QLabel()
        label.setText("    Current Weather is {} ".format(weather))
        label.setFont(QFont('Times', 18))
        label.setStyleSheet("background-color: rgba(211,211,211,0);")
        
        label.setAlignment(QtCore.Qt.AlignCenter)
        label1 = QLabel()
        label1.setPixmap(pixmap)
        label1.setStyleSheet("background-color: rgba(211,211,211,0);")
        weatherlayout.addWidget(label)
        weatherlayout.addWidget(label1)
        weatherw.setLayout(weatherlayout)
        weatherw.setStyleSheet("background-color: rgba(211,211,211,175);")
        self.layout.addWidget(weatherw)

        # text = self.Info['Location']
        # for x in self.Info['Location']:
        #     if x['City'] == cityin:
        #         location = x
        location = self.Info['Location'][0]
        
        text = getlocation(location)
        temperature = int(location['current']['temp'])
        self.cb.activated[str].connect(lambda: self.change_city(0))  
        #prints the current date and time
        now = QDate.currentDate().toString("MM-dd-yy")
        time = QTime.currentTime().toString("hh:mm AP")

        label1 = QLabel(" {} \n Date: {} \n Time : {}".format(text,now,time))
        label1.setFont(QFont('Times', 20))
        label1.setAlignment(QtCore.Qt.AlignCenter)
    
        label1.setStyleSheet("background-color: navy; \
                            color : rgba(255,255,255,200); \
                            margin: 1px; \
                            padding: 10px; \
                            border-style: solid; \
                            border-radius: 9px; \
                            border-width: 8px; \
                            border-color: rgba(0,0,0,255);")

        label1.setMargin(0)
        label1.setContentsMargins(0,0,0,0)
        
        #toolBar added
        self.layout.addWidget(label1)

        if(self.tempstate):
            temp = QLabel("Temperature : {} °F".format(round(temperature)))
        else:
            temp = QLabel("Temperature : {} °C".format(round((temperature - 32) * 5/9)))

        temp.setAlignment(QtCore.Qt.AlignCenter)
        temp.setStyleSheet("background-color: brown; \
                            color : rgba(255,255,255,200); \
                            margin: 1px; \
                            padding: 10px; \
                            border-style: solid; \
                            border-radius: 9px; \
                            border-width: 8px; \
                            border-color: rgba(0,0,0,255);")
        temp.setFont(QFont('Times', 15))
        temp.setMargin(0)
        temp.setContentsMargins(0,0,0,0)

        self.layout.addWidget(temp)
        
     

        layout3 = QGridLayout()
        layout5 = QGridLayout()
        layout4 = QVBoxLayout()
        scroll = QScrollArea()             # Scroll Area which contains the widgets, set as the centralWidget  
        scrollwidget = QWidget()
        #Scroll Area Properties
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setWidgetResizable(True)
        hourlyInfo = location['hourly']
        degree = u"\u00b0"
        #print(self.hwdata[0][0])
        #print(self.hwdata[1])
        i = 1
        blank = QLabel('    ')
        blank2 = QLabel('      ')
        texth = QLabel('Hourly:')
        texth.setStyleSheet("background-color: rgba(211,211,211,0);")
        texth.setFont(QFont('Times', 12, QFont.Bold))
        textd = QLabel('Daily:')
        textd.setStyleSheet("background-color: rgba(211,211,211,0);")
        textd.setFont(QFont('Times', 12, QFont.Bold))
        layout3.addWidget(texth)
        i = 1
        for x in range(1,15):
            if(self.tempstate):
                hourlyInfo[x]['temp'] = round(hourlyInfo[x]['temp'])
                hourlyInfo[x]['temp'] = str(hourlyInfo[x]['temp']) + degree + "F"
            else:
                 hourlyInfo[x]['temp'] = round((hourlyInfo[x]['temp'] - 32) * 5 / 9)
                 hourlyInfo[x]['temp'] = str(hourlyInfo[x]['temp']) + degree + "C"
            Icon = hourlyInfo[x]["weather"][0]["icon"]
            index = self.image_name.index(Icon)
            hourlyCheck = hourlyInfo[x]
            time = str(datetime.datetime.fromtimestamp(hourlyCheck['dt']).strftime('%c')).split()[3]
            time = int(time.split(':')[0])
            if time == 12:
                time = str(time) + 'pm'
            elif time == 0:
                time = str(12) + 'am'
            elif time > 12:
                time -= 12
                time = str(time) + ' pm'
            else:
                time = str(time) + ' am'
            #print(time)
            # hourlyCheck[0] = time
            j = 0


            # fill in hours for hourly  
            #print (time)
            if time == "0 am":
                time = "12 am"
            if time == "0 pm":
                time = "12 pm"
            timelabel = QLabel(str(time))
            # for y in timelabel:
            #     print(y)
            timelabel.setFont(QFont('Times', 10)) 
            timelabel.setAlignment(QtCore.Qt.AlignCenter)
            timelabel.setStyleSheet("background-color: rgba(211,211,211,0);")
            layout3.addWidget(timelabel, j+1, i*2)
            layout3.addWidget(blank, j+1, i*2+1)
            # i += 1

            # fill in temperatures for hourly
            temperaturelabel = QLabel(str(hourlyCheck['temp']))
            temperaturelabel.setFont(QFont('Times', 10))
            temperaturelabel.setStyleSheet("background-color: rgba(211,211,211,0);")
            temperaturelabel.setAlignment(QtCore.Qt.AlignCenter)
            layout3.addWidget(temperaturelabel, j+2, i*2)
            layout3.addWidget(blank, j+2, i*2+1)
            # i += 1

            #fill in conditions for hourly
            pixmap = QPixmap(self.image_list[index])
            condlabel = QLabel()
            condlabel.setPixmap(pixmap)            
            condlabel.setAlignment(QtCore.Qt.AlignCenter)
            condlabel.setStyleSheet("background-color: rgba(211,211,211,0);")
            layout3.addWidget(condlabel, j+3, i*2)
            layout3.addWidget(blank, j+2, i*2+1)

            i += 1
        layout5.addWidget(textd)


        # fill in daily forecast
        weeklyInfo = location['weekly']
        t = 1
        for x in range(0,8):
            #print(hourlyCheck)
            if(self.tempstate):
                weeklyInfo[x]['temp']['day'] = round(weeklyInfo[x]['temp']['day'])#* 9/5 + 32
                weeklyInfo[x]['temp']['day'] = str(weeklyInfo[x]['temp']['day']) + degree + "F"
            else:
                 weeklyInfo[x]['temp']['day'] = round((weeklyInfo[x]['temp']['day'] - 32) * 5 / 9)
                 weeklyInfo[x]['temp']['day'] = str(weeklyInfo[x]['temp']['day']) + degree + "C"
            Icon = weeklyInfo[x]["weather"][0]["icon"]
            #print(Icon)
            index = self.image_name.index(Icon)
            #print(index)
            # else:
            #     weeklyInfo[x]['temp']['day'] = str(weeklyInfo[x]['temp']['day']) + degree + "C"
            weeklyCheck = weeklyInfo[x]
            temp = str(weeklyCheck['temp']['day'])
            #print(temp)
            # temp = (temp[0])
            
            weeklyCheck[0] = temp
            j = 0

            # get day of week for weekly forecast
            time = str(datetime.datetime.fromtimestamp(weeklyCheck['dt']).strftime('%c')).split()[0]
            #print (time)
            timelabel = QLabel(time)
            # for y in timelabel:
            #     print(y)
            timelabel.setFont(QFont('Times', 10)) 
            timelabel.setAlignment(QtCore.Qt.AlignCenter)
            timelabel.setStyleSheet("background-color: rgba(211,211,211,0);")
            layout5.addWidget(timelabel, j+1, t)
            layout5.addWidget(blank2, j+1, t+1)
            # t += 1

            # get temp for weekly forecast
            temperature = weeklyCheck['temp']['day']
            temperaturelabel = QLabel(str(temperature))
            temperaturelabel.setFont(QFont('Times', 10))
            temperaturelabel.setStyleSheet("background-color: rgba(211,211,211,0);")
            temperaturelabel.setAlignment(QtCore.Qt.AlignCenter)
            layout5.addWidget(temperaturelabel, j+2, t)
            layout5.addWidget(blank2, j+2, t+1)
            # t += 1

            # get weather conditions for weekly forecast
            conditionslabel = QLabel()
            pixmap = QPixmap(self.image_list[index])
            conditionslabel.setPixmap(pixmap)  
            conditionslabel.setAlignment(QtCore.Qt.AlignCenter)
            conditionslabel.setStyleSheet("background-color: rgba(211,211,211,0);")
            layout5.addWidget(conditionslabel, j+3, t)
            layout5.addWidget(blank2, j+3, t+1)
            t += 1
        layout4.addLayout(layout3)
        layout4.addLayout(layout5)
        scrollwidget.setLayout(layout4)
        scroll.setWidget(scrollwidget)
        scroll.setAttribute(Qt.WA_StyledBackground, True)
        scroll.setStyleSheet('background-color: rgba(211,211,211,175);')
        self.layout.addWidget(scroll)

        b1 = QPushButton("Search New City")
        b1.setFont(QFont('Times', 12))
        self.layout.addWidget(b1)
        # status bar
        b1.setStyleSheet('background-color: rgba(255,255,255,200);')
        b1.clicked.connect(lambda: self.change_window(1))

        b2 = QPushButton()
        b2.setIcon(QtGui.QIcon(os.path.join(self.path+("/Images/"), 'refresh.png')))   
        self.layout.addWidget(b2)
        # status bar
        b2.setStyleSheet('background-color: rgba(255,255,255,200);')
        b2.clicked.connect(lambda: self.change_window(0))

        b3 = QPushButton()
        b3.setIcon(QtGui.QIcon(os.path.join(self.path+("/Images/"), 'close.png')))   
        self.layout.addWidget(b3)
        # status bar
        b3.setStyleSheet('background-color: rgba(255,255,255,200);')
        b3.clicked.connect(lambda: self.closeEvent(0))

        b4 = QPushButton("Report an Issue")
        b4.clicked.connect(self.report)
        b4.setFont(QFont('Times', 12))
        b4.setStyleSheet('background-color: rgba(255,255,255,200);')
        self.layout.addWidget(b4)

        # status bar
        self.central_widget.setLayout(self.layout)
        if self.darkmode:
            self.central_widget.setStyleSheet('background-color: rgba(50,50,50,255);')
        else:
            self.central_widget.setStyleSheet('background-color: none;')

    def loading(self):
        index = self.image_name.index("Loading")
        pixmap = QPixmap(self.image_list[index]).scaled(QSize(self.width/2.7, self.height/1.4), Qt.KeepAspectRatio)
        self.splash = QSplashScreen(pixmap)
        self.splash.showMessage("Loading modules", Qt.AlignBottom | Qt.AlignLeft)
        self.splash.show()

    def Check_current(self):
        word = self.textbox.text().lower()
        if word == "current":
            self.add_current("Current Location")
            write_cache(self.Info)
            self.get_data()
            self.t.insert(0, self.t.pop(self.t.index(self.Info[0][0])))
            self.change_window(0)
        else:
            word = word + ", " + self.cbox.currentText()
            self.City = word
            self.newcity()
        # word = self.textbox.text().lower()
        # #print(word)
        # if word == "current":
        #     if("Current Location" in self.t):
        #         self.change_city("Current Location")
        #     else:
        #         self.t.insert(0, "Current Location")
        #         self.change_city("Current Location")
        # else:
        #     word = word + ", " + self.cbox.currentText()
        #     self.City = word
        #     #print(self.city)
        #     self.newcity()

    def locations_saved(self, data, state):
        #print('\n\n\n')
        data['Location'].append(getcoords("Current Location"))
        #print(data)
        #print('\n\n\n')
        if data != False:
            self.Info = data
            for x in data['Location']:
                self.t.append(x['City'])
            
            # self.t = [data['Location'][i][str(i+1)]["Name"] for i in range(len(data['Location']))]
            # self.get_current()
        else:
            self.t = []
        self.State = []
        self.city = []
        for i in state:
            self.State.append(i)
            for j in state[i]:
                self.city.append(j)

        #print(self.Abb)

        # for i in range(len(data['Location'])):
        #     self.t.append(data['Location'][i][str(i+1)]["Name"])
    def load_images(self):
        self.image_list = []
        self.image_name = []
        for x in glob.glob((os.path.join(self.path+("/Images/*.png")))):
            self.image_list.append(x)
        image_name = os.listdir((os.path.join(self.path+("/Images/"))))
        #print(image_name)
        for x in range(len(image_name)):
            temp = str(image_name[x])
            temp = temp.split(".")
            self.image_name.append(temp[0])
        #print(self.image_name)

    def newcity(self):
        #word = self.spell.correction(self.textbox.text())
        word = self.City
        if word in self.t: # if the city is already added
            self.change_city(word)
            #print("test1")
        elif self.textbox.text() in self.city:
            self.add_current(word)
            #print("test")
            write_cache(self.Info)
            self.get_data()
            self.t.insert(0, word)
            self.change_window(0)
        self.Info, out = singleapiref(self.Info, word)
        if not out:
            self.textbox.clear()
            alert = QMessageBox()
            alert.setWindowTitle("City not found!")
            alert.setText("Please try again.")
            alert.setIcon(QMessageBox.Warning)
            alert.exec_()
            self.window.show()
        else:
            self.t.insert(0, word)
            write_cache(self.Info)
            self.get_data()
            # self.t.insert(0, self.Info[0][0])
            self.change_window(0)

    def change_city(self, data):
        if(data != 0):
            index = self.t.index(data)
        else:
            index = self.cb.currentIndex()
        # self.hwdata[0].insert(0, self.hwdata[0].pop(index))
        
        # self.hwdata[1].insert(0, self.hwdata[1].pop(index))

        # self.t.insert(0, self.t.pop(index))
        # self.Info.insert(0, self.Info.pop(index))
        # #print(self.Info)
        temp = self.Info['Location'][index]
        self.Info['Location'][index] = self.Info['Location'][0]
        self.Info['Location'][0] = temp
        # self.Info['Location'][0] = refresh(self.Info['Location'][0])
        self.swapt(index)
        self.change_window(0)
        
    def get_data(self):
        self.splash.repaint()

    def change_temp(self, state):
        if state == QtCore.Qt.Checked:
            self.ctemp = 0
            self.tempstate = 1
        else:
            self.ctemp = 1
            self.tempstate = 0
        self.change_window(0)
        
        # print(state)
    def get_current(self):
        self.Info = myapiref(self.t)

    def add_current(self, city):
        city = myapiref(city)
        if(city in self.Info):
            index = self.Info.index(city)
            self.Info.insert(0,self.Info.pop(index))
        else:
            self.Info.insert(0, city)
        #self.Info.insert(0, self.Info.pop(city))

    def change_window(self, index):
        self.Stack.setCurrentIndex(index)
        layout_list = [self.layout, self.layout1]
        for i in reversed(range(layout_list[index].count())):
            layout_list[index].itemAt(i).widget().setParent(None)
        window_list = [self.weather_window, self.mainwindow]
        f = window_list[index]
        f()

    def get_screensize(self):
        screen = QApplication.primaryScreen()
        size = screen.size()
        self.width = size.width()
        self.height = size.height()

    def create_window(self):
        self.get_screensize()
        self.window = QMainWindow()        
        self.window.setGeometry(self.width/3.75, self.height/9, self.width/2.2, self.height/1.3)
        self.window.setWindowTitle("Weather App")
        self.window.setCentralWidget(self.Stack)
        super().__init__()

    def closeEvent(self, event):
        # write_cache(self.Info)
        if(event == 0):
            sys.exit(self.weatherapp.exit())
        
    def swapt(self, x):
        temp = self.t[x]
        self.t[x] = self.t[0]
        self.t[0] = temp

    def switchtempval(self):

        if self.tempstate:
            self.tempstate = 0
            self.change_window(0)
        else:
            self.tempstate = 1
            self.change_window(0)

    def switchdarkmode(self):

        if self.darkmode:
            self.darkmode = 0
            self.change_window(0)
        else:
            self.darkmode = 1
            self.change_window(0)

    def report(self):
        ##report an issue window
        window2 = QMainWindow()
        window2.setGeometry(1000,1000,1000,1000)
        window2.setWindowTitle("Report an Issue")
        window2.setStyleSheet("background-color : navy; color : rgba(255,255,255,200)")

        central_widget = QWidget()
        layout = QFormLayout()
        window2.setCentralWidget(central_widget)
        central_widget.setLayout(layout)

        self.label = QLabel()
        pixmap = QPixmap(os.path.join(self.path+("/Images/"),'image.png')).scaled(QSize(75,75), Qt.KeepAspectRatio)
        self.label.setPixmap(pixmap)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(self.label)

        label = QLabel("Help improve the Weather app by describing the current conditions at your location")
        label.setFont(QFont('Times', 20))
        layout.addWidget(label)

        label1 = QLabel("Overall Conditions")
        label1.setFont(QFont('Times', 18))
        layout.addWidget(label1)

        tc = QCheckBox("     Clear")
        tc.setFont(QFont('Times', 14))
        tc.move(400,0)
        layout.addWidget(tc)

        tc = QCheckBox("     Clouds")
        tc.setFont(QFont('Times', 14))
        tc.move(400,0)
        layout.addWidget(tc)

        tc = QCheckBox("     Rain")
        tc.setFont(QFont('Times', 14))
        tc.move(400,0)
        layout.addWidget(tc)

        tc = QCheckBox("     Sleet")
        tc.setFont(QFont('Times', 14))
        tc.move(400,0)
        layout.addWidget(tc)

        tc = QCheckBox("     Snow")
        tc.setFont(QFont('Times', 14))
        tc.move(400,0)
        layout.addWidget(tc)

        tc = QCheckBox("     It's warmer")
        tc.setFont(QFont('Times', 14))
        tc.move(400,0)
        layout.addWidget(tc)

        tc = QCheckBox("     Seems accurate")
        tc.setFont(QFont('Times', 14))
        tc.move(400,0)
        layout.addWidget(tc)  

        tc = QCheckBox("     It's colder")
        tc.setFont(QFont('Times', 14))
        tc.move(400,0)
        layout.addWidget(tc)      

        label5 = QLabel("Other Conditions")
        label.setFont(QFont('Times', 18))
        layout.addWidget(label5)

        tc = QCheckBox("     Fog")
        tc.setFont(QFont('Times', 14))
        tc.move(400,0)
        layout.addWidget(tc)   

        tc = QCheckBox("     Hail")
        tc.setFont(QFont('Times', 14))
        tc.move(400,0)
        layout.addWidget(tc)   

        tc = QCheckBox("     Smoke")
        tc.setFont(QFont('Times', 14))
        tc.move(400,0)
        layout.addWidget(tc)  

        tc = QCheckBox("     Lightning")
        tc.setFont(QFont('Times', 14))
        tc.move(400,0)
        layout.addWidget(tc)    

        b1 = QPushButton("Submit")
        central_widget.setLayout(layout)
        b1.setStyleSheet("background-color : rgba(255,255,255,200); color: black")
        b1.clicked.connect(lambda: window2.hide())
        
        b2 = QPushButton("Close")
        central_widget.setLayout(layout)
        b2.setStyleSheet("background-color : rgba(255,255,255,200); color: black") 
        b2.clicked.connect(lambda: window2.hide())
        
        layout.addRow(b1,b2)
        layout.setSpacing(20)

        window2.show()