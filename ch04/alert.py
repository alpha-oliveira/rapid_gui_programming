import sys
import time
####### changed the following ######
### but SIGNAL not used
# from PyQt4.QtCore import (QTime, QTimer, Qt, SIGNAL)
#from PyQt4.QtGui import (QApplication, QLabel)

from PyQt5.QtCore import QTime, QTimer, Qt
from PyQt5.QtWidgets import QApplication, QLabel

app = QApplication(sys.argv)

try:
    due = QTime.currentTime()
    message = "Alert!"
    if len(sys.argv) < 2:
        raise ValueError
    hours, mins = sys.argv[1].split(":")
    due = QTime(int(hours), int(mins))
    if not due.isValid():
        raise ValueError
    if len(sys.argv) > 2:
        message = " ".join(sys.argv[2:])
except ValueError:
    message = "Usage: alert.pyw HH:MM [optional message]" # 24hr clock

while QTime.currentTime() < due:
    time.sleep(20) # 20 seconds

label = QLabel("<font color=red size=72><b>{0}</b></font>"
               .format(message))
label.setWindowFlags(Qt.SplashScreen)
label.show()
QTimer.singleShot(60000, app.quit) # 1 minute
app.exec_()
