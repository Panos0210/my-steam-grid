import os, sys, urllib.request, zipfile, shutil
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QObject
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QTextEdit, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox

repo = 'https://github.com/Panos0210/my-steam-grid/archive/refs/heads/main.zip'
output = 'grid.zip'

class Worker(QObject):
    progress = pyqtSignal(str)
    finished = pyqtSignal()

    def __init__(self, userdata_path):
        super().__init__()
        self.userdata_path = userdata_path

    def run(self):
        try:
            self.progress.emit("Downloading Grid...")
            urllib.request.urlretrieve(repo, output)

            self.progress.emit('Extracting Grid...')
            with zipfile.ZipFile(output, 'r') as zip_ref:
                zip_ref.extractall("extracted_repo")

            config_folder_path = os.path.join("extracted_repo", "my-steam-grid-main", "config")
            if not os.path.exists(config_folder_path):
                self.progress.emit("Error: 'config' folder not found in the extracted ZIP!")
                return

            found_any = False
            for folder_name in os.listdir(self.userdata_path):
                folder_path = os.path.join(self.userdata_path, folder_name)
                if os.path.isdir(folder_path) and folder_name.isdigit():
                    found_any = True
                    dest_path = os.path.join(folder_path, "config")
                    shutil.copytree(config_folder_path, dest_path, dirs_exist_ok=True)
                    self.progress.emit(f"Copied 'config' folder to: {dest_path}")
            
            if not found_any:
                self.progress.emit(f"Warning: No user ID folders found in '{self.userdata_path}'")

            shutil.rmtree("extracted_repo")
            os.remove(output)
            self.progress.emit("\nAll done!")

        except Exception as e:
            self.progress.emit(f"\nAN ERROR OCCURRED: {e}")
        finally:
            self.finished.emit()

app = QApplication([])
path_win = None

def userdata_textbox_win():
    global path_win
    path_win = QWidget()
    path_win.setWindowTitle('Setting up the userdata path...')
    path_layout = QVBoxLayout()
    
    path_label = QLabel('Now you have to select the Steam/userdata folder directory on your pc\n'
                        r'(Default Steam userdata folder directory on your system is: C:\Program Files(x86)\Steam\Userdata)')
    path_label.setWordWrap(True)
    
    path_input = QLineEdit(r"C:\Program Files (x86)\Steam\userdata")
    start_button = QPushButton('Start')

    log_box = QTextEdit()
    log_box.setReadOnly(True)
    log_box.setPlaceholderText("Progress will be shown here...")

    path_layout.addWidget(path_label)
    path_layout.addWidget(path_input)
    path_layout.addWidget(start_button)
    path_layout.addWidget(log_box)

    path_win.setLayout(path_layout)
    path_win.resize(500, 400)
    
    def on_start_click():
        start_button.hide()
        user_path = path_input.text()
        log_box.clear()
        
        path_win.thread = QThread()
        path_win.worker = Worker(user_path)
        path_win.worker.moveToThread(path_win.thread)
        
        path_win.thread.started.connect(path_win.worker.run)
        path_win.worker.finished.connect(path_win.thread.quit)
        path_win.worker.finished.connect(path_win.worker.deleteLater)
        path_win.thread.finished.connect(path_win.thread.deleteLater)
        path_win.worker.progress.connect(log_box.append)
        
        def on_finish():
            start_button.setText("Close")
            start_button.clicked.disconnect()
            start_button.clicked.connect(app.quit)
            start_button.show()

        path_win.worker.finished.connect(on_finish)
        
        path_win.thread.start()
        
    start_button.clicked.connect(on_start_click)
    path_win.show()

def on_proceed_click():
    welcome.close()
    userdata_textbox_win()

def on_cancel_click():
    app.quit()

welcome = QWidget()
welcome.setWindowTitle('Download Steam Grid...')
welcome_layout = QVBoxLayout()
prompt = QLabel('This will install a clean Steam grid for your apps and games in your steam library.')
button = QPushButton('Proceed')
cbutton = QPushButton('Cancel')
welcome_layout.addWidget(prompt)
welcome_layout.addWidget(button)
welcome_layout.addWidget(cbutton)
button.clicked.connect(on_proceed_click)
cbutton.clicked.connect(on_cancel_click)
welcome.setLayout(welcome_layout)
welcome.show()

sys.exit(app.exec_())

