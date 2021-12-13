from PyQt5 import QtGui
import weatherapp, sys, os
from apiRef import read_cache, read_state
from PyQt5.QtWidgets import  QApplication


# class getLocation(QWidget):

#     def __init__(self):
#         super().__init__()

#         self.showDialog()
#         #self.menuBar()

#     def showDialog(self):
#         city = QInputDialog.getText(self, 'Location Check', 'Enter your location:')
#         name = city[0]
#         weather = weatherapp.weather(name)
#         weather.getInfo()
#         weather.create_window()
def swap(first, second):
    temp = first
    first = second
    second = temp
class Main():

    def window():
        app = QApplication(sys.argv)
        path = sys.path[0]
        app.setWindowIcon(QtGui.QIcon(os.path.join(path+("/Images/"),'Icon.png')))
        print(str(os.path.join(path+("/Images/"))))
        # ex = getLocation()
        weather = weatherapp.weather()
        weather.create_window()
        weather.load_images()
        weather.loading()
        data = read_cache()
        state = read_state()

        weather.locations_saved(data, state)
        if data != False:
            weather.get_data()
            for x in range(0, len(data['Location'])):
                if data['Location'][x]['City'] == 'Current Location':
                    temp = data['Location'][x]
                    data['Location'][x] = data['Location'][0]
                    data['Location'][0] = temp
                    weather.swapt(x)
                    break
            weather.weather_window()
        else:
            weather.change_window(1)
        
        app.exec_()
        
        weather.closeEvent(1)
    
if __name__ == '__main__':
    Main.window()
