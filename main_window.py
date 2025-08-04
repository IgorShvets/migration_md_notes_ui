import os
import re
#import widgets
from PySide6.QtWidgets import QMainWindow
from PySide6.QtWidgets import QTableWidget
from PySide6.QtWidgets import QTableWidgetItem
from PySide6.QtWidgets import QPushButton
from PySide6.QtWidgets import QWidget
from PySide6.QtWidgets import QLineEdit
from PySide6.QtWidgets import QMessageBox
#import layouts
from PySide6.QtWidgets import QVBoxLayout
from PySide6.QtWidgets import QHBoxLayout
#import dialogs
from PySide6.QtWidgets import QProgressDialog
from PySide6.QtCore import Qt
#import other modules
from note_windows import NoteWindow
from main_window_logic import MainWindowLogic

class MainWindow(QMainWindow):
    def __init__(self, window_title: str, window_width: int, window_height: int):
        super().__init__()

        #set window title and size
        self.setWindowTitle(window_title)
        self.setGeometry(100, 100, window_width, window_height)
        self.setMinimumSize(window_width, window_height)
        #self.setMaximumSize(window_width, window_height)
        #self.setFixedSize(window_width, window_height)

        #create main window logic class instance
        self.window_logic: MainWindowLogic = MainWindowLogic(self)

        #create main menu buttons
        self.btn_open_notes_folder_dialog: QPushButton = QPushButton("Open Notes Folder Dialog")
        self.btn_open_save_folder_dialog: QPushButton = QPushButton("Open Save Folder Dialog")
        self.btn_attach_notes_folder: QPushButton = QPushButton("Attachments Notes Folder")
        self.btn_scan_notes_folder: QPushButton = QPushButton("Scan Notes Folder")

        #create main menu text fields
        self.txt_notes_folder_path: QLineEdit = QLineEdit()
        self.txt_notes_folder_path.setPlaceholderText("Root folder of md notes")
        self.txt_save_folder_path: QLineEdit = QLineEdit()
        self.txt_save_folder_path.setPlaceholderText("Folder to save migrated notes")
        self.txt_attach_notes_folder: QLineEdit = QLineEdit()
        self.txt_attach_notes_folder.setPlaceholderText("Name of folder with attachments (images and other files)")
        

        #create main menu table
        self.table_notes: QTableWidget = QTableWidget()
        #set table columns
        self.table_notes.setColumnCount(3)
        self.table_notes.setHorizontalHeaderLabels(["Note Name", "Note Path", "Attach Count"])
        self.table_notes.setRowHeight(0, 20)
        self.table_notes.setColumnWidth(0, 500)
        self.table_notes.setColumnWidth(1, 250)
        self.table_notes.setColumnWidth(2, 100)


        #create central widget
        self.central_widget: QWidget = QWidget()
        self.setCentralWidget(self.central_widget)

        #create layouts
        self.main_layout: QVBoxLayout = QVBoxLayout()
        self.layout_menu_notes: QHBoxLayout = QHBoxLayout()
        self.layout_menu_save: QHBoxLayout = QHBoxLayout()
        self.layout_menu_attach: QHBoxLayout = QHBoxLayout()
        self.layout_menu_scan: QHBoxLayout = QHBoxLayout()
        self.layout_table: QVBoxLayout = QVBoxLayout()
        #set options for layouts
        self.layout_menu_notes.setContentsMargins(2, 2, 2, 2)
        self.layout_menu_save.setContentsMargins(2, 2, 2, 2)
        self.layout_menu_attach.setContentsMargins(2, 2, 2, 2)
        self.layout_menu_scan.setContentsMargins(2, 2, 2, 2)
        self.layout_table.setContentsMargins(2, 2, 2, 2)

        #set main layout
        self.central_widget.setLayout(self.main_layout)
        #set main window layouts
        self.main_layout.addLayout(self.layout_menu_notes)
        self.main_layout.addLayout(self.layout_menu_save)
        self.main_layout.addLayout(self.layout_menu_attach)
        self.main_layout.addLayout(self.layout_menu_scan)
        self.main_layout.addLayout(self.layout_table)

        #add main menu buttons to main menu layout
        self.layout_menu_notes.addWidget(self.txt_notes_folder_path)
        self.layout_menu_notes.addWidget(self.btn_open_notes_folder_dialog)
        self.layout_menu_save.addWidget(self.txt_save_folder_path)
        self.layout_menu_save.addWidget(self.btn_open_save_folder_dialog)
        self.layout_menu_attach.addWidget(self.txt_attach_notes_folder)
        self.layout_menu_attach.addWidget(self.btn_attach_notes_folder)
        self.layout_menu_scan.addWidget(self.btn_scan_notes_folder)
        self.layout_table.addWidget(self.table_notes)

        #progress dialog 
        self.progress_dialog: QProgressDialog = QProgressDialog()
        self.progress_dialog.setWindowModality(Qt.ApplicationModal)
        self.progress_dialog.setCancelButton(None)

        #connect buttons to functions
        self.btn_open_notes_folder_dialog.clicked.connect(self.window_logic.open_notes_folder_dialog)
        self.txt_notes_folder_path.textChanged.connect(self.window_logic.auto_fill_save_folder_path)
        self.txt_notes_folder_path.textChanged.connect(self.window_logic.auto_fill_attach_folder_path)
        self.btn_open_save_folder_dialog.clicked.connect(self.window_logic.open_save_folder_dialog)
        self.btn_attach_notes_folder.clicked.connect(self.window_logic.attach_joplin_folder_dialog)
        self.btn_scan_notes_folder.clicked.connect(self.window_logic.start_check_joplin_folder)
        #connect table to functions
        self.table_notes.itemDoubleClicked.connect(self.table_item_double_clicked)
   
    #create function get markdown attach from .md file
    def get_markdown_attach_from_md_file(self, md_file_path: str)-> list[str]:
        """
        Get markdown attach from .md file
        Args: md_file_path - full md file path
        Returns: list[str] - attach list
        """
        try:
            with open(md_file_path, "r", encoding="utf-8") as file:
                md_content: str = file.read()
                #get all attach from md content
                attach_list: list[str] = re.findall(r"!\[.*?\]\((.*?)\)", md_content)
                return attach_list
        except Exception as e:
            QMessageBox.warning(self, "Warning", "Error get markdown attach from md file: " + str(e))
            raise e

    #create function table item double clicked
    def table_item_double_clicked(self, item: QTableWidgetItem):
        try:
            #get item row
            item_row: int = item.row()
            #get note name
            note_name: str = self.table_notes.item(item_row, 0).text()
            #get note path
            note_path: str = self.table_notes.item(item_row, 1).text()
            #open note window
            self.note_window: NoteWindow = NoteWindow(note_path, self.txt_attach_notes_folder.text(), self.txt_notes_folder_path.text())
            self.note_window.show()
        except Exception as e:
            QMessageBox.warning(self, "Warning", "Error table item double clicked: " + str(e))
            raise e