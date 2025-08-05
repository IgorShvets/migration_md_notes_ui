from msvcrt import get_osfhandle
import os
#import PySide6 widgets
from PySide6.QtWidgets import QApplication, QFileDialog, QMessageBox
from PySide6.QtWidgets import QMainWindow
#
import time

#create function open folder dialog
class MainWindowLogic:
    def __init__(self, main_window: QMainWindow):
        self.main_window = main_window
        
        

    def get_path_from_folder_dialog(self)-> str:
        """
        Open folder dialog and return folder path
        Args: None
        Returns: str - folder path
        """
        try:
            folder_path: str = QFileDialog.getExistingDirectory(self.main_window, "Open Folder Dialog", "", QFileDialog.ShowDirsOnly)
            return folder_path
        except Exception as e:
            QMessageBox.warning(self.main_window, "Warning", "Error open folder dialog: " + str(e))
            raise e

    #create function open joplin folder dialog
    def open_notes_folder_dialog(self):
        """
        Open notes folder dialog and set text to txt_notes_folder_path
        Args: None
        Returns: None
        """
        try:
            folder_path: str = self.get_path_from_folder_dialog()
            if folder_path:
                folder_path = os.path.normpath(folder_path)
                self.main_window.txt_notes_folder_path.setText(folder_path)
                self.auto_fill_save_folder_path()
                self.auto_fill_attach_folder_path()
        except Exception as e:
            QMessageBox.warning(self.main_window, "Warning", "Error open notes folder dialog: " + str(e))
            raise e

    def auto_fill_save_folder_path(self):
        """
        Auto fill save folder path
        Args: None
        Returns: None
        """
        if self.main_window.txt_notes_folder_path.text():
            save_folder_path: str = self.main_window.txt_notes_folder_path.text() + "/MIGRATED_NOTES"
            self.main_window.txt_save_folder_path.setText(os.path.normpath(save_folder_path))

    def auto_fill_attach_folder_path(self):
        """
        Auto fill attach folder path
        Args: None
        Returns: None
        """
        if self.main_window.txt_notes_folder_path.text():
            #find folder with attachments
            folder_list: list[str] = self.get_folder_list_from_folder(self.main_window.txt_notes_folder_path.text())
            for folder in folder_list:
                try:
                    full_folder_path: str = os.path.join(self.main_window.txt_notes_folder_path.text(), folder)
                    file_list: list[str] = self.get_file_list_from_folder(full_folder_path)
                    #check if folder contains images and other files
                    if any(file.endswith((
                        '.png',
                        '.jpg',
                        '.jpeg', 
                        '.gif', 
                        '.bmp', 
                        '.webp',
                        '.mp4',
                        '.mp3',
                        '.pdf',
                        '.doc',
                        '.docx',
                        '.xls',
                        '.xlsx',
                        '.txt',
                        '.csv',
                        '.json',
                        '.xml',
                        '.yaml',
                        '.yml',
                        '.html'
                        )) for file in file_list):
                        self.main_window.txt_attach_notes_folder.setText(folder)
                        break
                except Exception as e:
                    QMessageBox.warning(self.main_window, "Warning", "Error search folder with attachments: " + str(e))
                    raise e
                        


    def get_folder_list_from_folder(self, folder_path: str)-> list[str]:
        """
        Get folder list from folder
        Args: folder_path - full folder path
        Returns: list[str] - folder list
        """
        
        try:
            folder_list: list[str] = []
            for root, dirs, _ in os.walk(folder_path):
                for dir in dirs:
                    folder_list.append(os.path.join(root, dir))
            time.sleep(2)
            return folder_list
        except Exception as e:
            QMessageBox.warning(self.main_window, "Warning", "Error get folder list from folder: " + str(e))
            raise e


    def get_file_list_from_folder(self, folder_path: str)-> list[str]:
        """
        Get file list from folder
        Args: folder_path - full folder path
        Returns: list[str] - file list
        """
        try:
            file_list: list[str] = []
            for file in os.listdir(folder_path):
                if os.path.isfile(os.path.join(folder_path, file)):
                    file_list.append(file)
            return file_list
        except Exception as e:
            QMessageBox.warning(self.main_window, "Warning", "Error get file list from folder: " + str(e))
            raise e

    def open_save_folder_dialog(self):
        """
        Open save folder dialog and set text to txt_save_folder_path
        Args: None
        Returns: None
        """
        try:
            folder_path: str = self.get_path_from_folder_dialog()
            if folder_path:
                self.main_window.txt_save_folder_path.setText(folder_path)
        except Exception as e:
            QMessageBox.warning(self.main_window, "Warning", "Error open save folder dialog: " + str(e))
            raise e

    def attach_joplin_folder_dialog(self):
        """
        Open attach joplin folder dialog and set text to txt_attach_joplin_folder
        Args: None
        Returns: None
        """
        try:
            folder_path: str = self.get_path_from_folder_dialog()
            if folder_path:
                folder_path = os.path.basename(os.path.normpath(folder_path))
                self.main_window.txt_attach_notes_folder.setText(folder_path)
        except Exception as e:
            QMessageBox.warning(self.main_window, "Warning", "Error open attach notes folder dialog: " + str(e))
            raise e

    def start_check_joplin_folder(self):
        """
        Start check joplin folder and fill table
        Args: None
        Returns: None
        """
        #check joplin folder path
        if not self.main_window.txt_notes_folder_path.text():
            QMessageBox.warning(self.main_window, "Warning", "Joplin folder path is not set")
            return
        #check save folder path
        if not self.main_window.txt_save_folder_path.text():
            QMessageBox.warning(self.main_window, "Warning", "Save folder path is not set")
            return
        #check attach joplin folder path
        if not self.main_window.txt_attach_notes_folder.text():
            QMessageBox.warning(self.main_window, "Warning", "Attach joplin folder path is not set")
            return
        #check attach joplin folder
        try:
            #get joplin folder path
            joplin_folder_path: str = self.main_window.txt_notes_folder_path.text()
            #get folder list from joplin folder
            folder_list: list[str] = self.get_folder_list_from_folder(joplin_folder_path)

            #get file list from joplin folder
            root_file_list: list[str] = self.get_file_list_from_folder(joplin_folder_path)
            #fill table with joplin notes from root folder
            self.fill_table_with_joplin_notes(joplin_folder_path, root_file_list)
            #fill table with joplin notes from sub folders (sub folders)
            for folder in folder_list:
                folder_file_list: list[str] = self.get_file_list_from_folder(os.path.join(joplin_folder_path, folder))
                self.fill_table_with_joplin_notes(os.path.join(joplin_folder_path, folder), folder_file_list)
        except Exception as e:
            QMessageBox.warning(self.main_window, "Warning", "Error start check joplin folder: " + str(e))
            raise e

    def fill_table_with_joplin_notes(self, joplin_folder_path: str, file_list: list[str]):
        """
        Fill table with joplin notes
        Args: joplin_folder_path - full joplin folder path or sub folder path
        file_list - list of files in folder
        Returns: None
        """
        #get markdown attach from md file
        try:
            for file in file_list:
                if file.endswith(".md"):
                    attach_list: list[str] = self.get_markdown_attach_from_md_file(os.path.join(joplin_folder_path, file))
                    #get attach count
                    attach_count: int = len(attach_list)
                    #add note to table
                    self.table_notes.insertRow(0)
                    self.main_window.table_notes.setItem(0, 0, self.main_window.QTableWidgetItem(file))
                    self.main_window.table_notes.setItem(0, 1, self.main_window.QTableWidgetItem(os.path.join(joplin_folder_path, file)))
                    self.main_window.table_notes.setItem(0, 2, self.main_window.QTableWidgetItem(str(attach_count)))
        except Exception as e:
            QMessageBox.warning(self, "Warning", "Error fill table with joplin notes: " + str(e))
            raise e