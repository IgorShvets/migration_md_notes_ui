#import main window
from main_window import MainWindow
from PySide6.QtWidgets import QApplication
import qdarkstyle

#init app
app: QApplication = QApplication([])
#set dark theme
app.setStyleSheet(qdarkstyle.load_stylesheet())
#init main window
main_window: MainWindow = MainWindow("Migrage From Joplin", 900, 600)
main_window.show()
app.exec()
