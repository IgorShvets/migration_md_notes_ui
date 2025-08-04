import os
import re
#import widgets
from PySide6.QtWidgets import QWidget
from PySide6.QtWidgets import QTableWidget
from PySide6.QtWidgets import QPushButton
from PySide6.QtWidgets import QTableWidgetItem
from PySide6.QtWidgets import QMessageBox
#import layouts
from PySide6.QtWidgets import QVBoxLayout
from PySide6.QtWidgets import QHBoxLayout

class NoteWindow(QWidget):
    def __init__(self, note_path: str, attach_folder_name: str, joplin_folder_path: str):
        super().__init__()

        self.note_name: str = os.path.basename(os.path.normpath(note_path))

        #set window properties
        self.setWindowTitle(self.note_name)
        self.setGeometry(100, 100, 700, 500)
        self.setMinimumSize(700, 500)

        #create table
        self.note_table: QTableWidget = QTableWidget()
        self.note_table.setColumnCount(4)
        self.note_table.setHorizontalHeaderLabels(["md description", "file name", "size", "type"])
        self.note_table.setRowHeight(0, 15)
        #create button
        self.btn_save: QPushButton = QPushButton("Save note")
        self.btn_show_in_explorer: QPushButton = QPushButton("Show in explorer")
        self.btn_cancel: QPushButton = QPushButton("Cancel")

        #create main layout
        self.main_layout: QVBoxLayout = QVBoxLayout()
        self.table_layout: QHBoxLayout = QHBoxLayout()
        self.button_layout: QHBoxLayout = QHBoxLayout()

        #set main layout
        self.setLayout(self.main_layout)
        #set table layout
        self.main_layout.addLayout(self.table_layout)
        self.table_layout.setContentsMargins(2, 2, 2, 2)
        self.table_layout.addWidget(self.note_table)
        #set button layout
        self.button_layout.setContentsMargins(2, 2, 2, 2)
        self.main_layout.addLayout(self.button_layout)
        self.button_layout.addWidget(self.btn_save)
        self.button_layout.addWidget(self.btn_show_in_explorer)
        self.button_layout.addWidget(self.btn_cancel)

        #connect buttons to functions
        self.btn_cancel.clicked.connect(self.close_window)

        #fill table
        self.fill_table(note_path, attach_folder_name, joplin_folder_path)

    def close_window(self):
        """
        Close window
        Args: None
        Returns: None
        """
        self.close()

        
    def fill_table(self, note_path: str, attach_folder_name: str, joplin_folder_path: str):
        """
        Fill table with note
        Args: note_path - full note path
        Returns: None
        """
        try:
            with open(note_path, "r", encoding="utf-8") as file:
                note_content: str = file.read()
            
            matches = re.findall(r'(!?)\[(.*?)\]\((.*?)\)', note_content)
            
            for is_image, text, path in matches:
                print(f"{'Image' if is_image else 'Link'}: [{text}] -> ({path})")
                
                # add new row
                row_position = self.note_table.rowCount()
                self.note_table.insertRow(row_position)
                
                # fill all columns
                self.note_table.setItem(row_position, 0, QTableWidgetItem(text))  # md description
                self.note_table.setItem(row_position, 1, QTableWidgetItem(path))  # file name
                
                #get attach file name
                attach_file_name: str = os.path.basename(os.path.normpath(path))
                #get full attach file path
                attach_file_path: str = os.path.join(joplin_folder_path, attach_folder_name, attach_file_name)
                # get file size
                if os.path.exists(attach_file_path):
                    file_size = os.path.getsize(attach_file_path)
                    size_text = self.format_size(file_size)
                else:
                    size_text = "N/A"
                
                self.note_table.setItem(row_position, 2, QTableWidgetItem(size_text))  # size
                self.note_table.setItem(row_position, 3, QTableWidgetItem("Image" if is_image else "Link"))  # type
            
            # update columns width
            self.note_table.resizeColumnsToContents()
            
        except Exception as e:
            QMessageBox.warning(self, "Warning", "Error fill table with note: " + str(e))
            raise e

    def format_size(self,bytes_size: int) -> str:
        """
        Format size
        Args: bytes_size - size in bytes
        Returns: formatted size
        """
        for unit in ['bytes', 'KB', 'MB', 'GB', 'TB']:
            if bytes_size < 1024:
                return f"{bytes_size:.2f} {unit}"
            bytes_size /= 1024
        return f"{bytes_size:.2f} PB"


        


