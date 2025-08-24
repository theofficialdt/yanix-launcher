#!/usr/bin/python3
import os
import subprocess
import webbrowser
import shutil
import time
import threading
import requests
import zipfile
import sys
import socket
import json
import tempfile

from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QFileDialog, QVBoxLayout,
    QWidget, QLabel, QMessageBox, QComboBox, QDialog, QHBoxLayout,
    QSplashScreen, QProgressDialog, QLineEdit, QCheckBox
)
from PyQt5.QtGui import QFont, QPalette, QLinearGradient, QColor, QBrush, QIcon, QPainter, QPixmap
from PyQt5.QtCore import Qt, QUrl, QRect, QTimer, QCoreApplication, QObject, pyqtSignal, QThread

try:
    from pypresence import Presence
    presence_enabled = True
except ImportError:
    presence_enabled = False

CLIENT_ID = '1383809366460989490'
USER_AGENT = 'YanixLauncher/1.0.2'

YANIX_PATH = os.path.expanduser("~/.local/share/yanix-launcher")
DATA_DOWNLOAD_URL = "https://nikoyandere.github.io/data.zip"
TEMP_ZIP_PATH = os.path.join(YANIX_PATH, "data.zip")
LATEST_VERSION_URL = "https://gitea.com/YanixLauncher/Yanix-Launcher-Gitea/raw/branch/main/yanix-launcher.py"

CONFIG_PATH = os.path.join(YANIX_PATH, "data/game_path.txt")
LANG_PATH = os.path.join(YANIX_PATH, "data/multilang.txt")
ICON_PATH = os.path.join(YANIX_PATH, "data/Yanix-Launcher.png")
WINEPREFIX_PATH = os.path.join(YANIX_PATH, "data/wineprefix_path.txt")
THEME_PATH = os.path.join(YANIX_PATH, "data/theme.txt")
CUSTOM_THEMES_DIR = os.path.join(YANIX_PATH, "themes")
ADVANCED_CONFIG_PATH = os.path.join(YANIX_PATH, "advanced_config.json")
ADVANCED_FLAG_PATH = os.path.join(YANIX_PATH, "advanced_mode.flag")

YAN_SIM_DOWNLOAD_URL = "https://yanderesimulator.com/dl/latest.zip"
YAN_SIM_INSTALL_PATH = os.path.join(YANIX_PATH, "game")
YAN_SIM_EXE_NAME = "YandereSimulator.exe"
YAN_SIM_NATIVE_EXE_PATH = os.path.join(YAN_SIM_INSTALL_PATH, YAN_SIM_EXE_NAME)

os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
os.makedirs(CUSTOM_THEMES_DIR, exist_ok=True)

LANGUAGES = {
    "en": {"welcome": "Welcome to Yanix Launcher", "loading": "Loading", "play": "Play", "github": "GitHub", "settings": "Settings", "download": "Download Game", "select_language": "Select Language", "select_exe": "Select .exe for WINE", "support": "Support", "discord": "Discord", "lang_changed": "Language changed!", "exit": "Exit", "missing_path": "Uh oh, try extract in home folder", "winetricks": "Winetricks", "no_internet": "No internet connection. Please check your network and try again.", "downloading_data": "Downloading Data File....", "extracting_data": "Extracting Files....", "download_failed": "Failed to download data.", "extract_failed": "Failed to extract data.", "download_success": "Data downloaded and extracted successfully!", "wineprefix": "Manage Wineprefix", "wineprefix_selected": "Wineprefix path saved successfully.", "wineprefix_error": "Could not save Wineprefix path.", "select_theme": "Select Theme", "theme_changed": "Theme changed!", "load_custom_theme": "Load Custom Theme", "delete_game": "Delete Game", "delete_game_confirm": "Are you sure you want to delete the game? This action cannot be undone.", "game_deleted_success": "Game deleted successfully!", "game_not_found": "Game not found at the installed path.", "check_updates": "Check for Updates", "update_outdated": "Your launcher is outdated. The application will now be updated and restarted.", "update_developer": "You are running a developer build.", "update_uptodate": "Your launcher is up to date.", "update_error": "Could not check for updates.", "connecting": "Connecting...", "cancel": "Cancel", "canceled": "Canceled", "apply": "Apply", "success_title": "Success", "info_title": "Info", "error_title": "Error", "theme_error_title": "Error Loading Theme", "theme_load_error": "Failed to load custom theme from {filepath}: {e}", "theme_save_error": "Could not save theme setting: {e}", "lang_ai_warning": "This language is 100% AI and may have malfunctions.", "lang_save_error": "Could not save language setting: {e}", "game_path_invalid": "The saved game path is invalid. Please select the .exe file for WINE again.", "game_path_undefined": "Game executable path not defined. Please select the .exe file for WINE or download Yandere Simulator.", "wine_missing": "WINE is not installed or not in your system's PATH.", "game_launch_fail": "An error occurred while launching the game: {e}", "select_exe_window_title": "Select Game Executable", "exe_file_filter": "EXE Files (*.exe)", "exe_save_success": "Executable path saved successfully.", "exe_save_fail": "Could not save executable path: {e}", "no_internet_title": "No Internet", "game_installed": "Yandere Simulator is already installed.", "download_game_window_title": "Download Game", "download_game_prompt": "Do you want to download Yandere Simulator?\nThis may take a while.", "download_progress_window_title": "Download Progress", "downloading_label": "Downloading... {downloaded} / {total} ({percentage}%)", "downloading_label_no_total": "Downloading... {downloaded}", "download_canceled": "Download canceled.", "extraction_canceled": "Extraction canceled.", "extracting_label": "Extracting files...", "extraction_progress_window_title": "Extraction Progress", "game_download_success": "Yandere Simulator downloaded and extracted successfully!", "game_delete_fail": "Failed to delete game: {e}", "winetricks_missing": "Winetricks is not installed or not in your PATH.", "winetricks_launch_fail": "Failed to launch Winetricks: {e}", "update_restart_prompt": "The application will now restart to apply the update.", "update_error_window_title": "Update Error", "update_fail": "Failed to apply update: {e}", "unexpected_error": "An unexpected error occurred: {e}", "extracting_label_progress": "Extracting files... ({current}/{total})", "advanced_settings_applied": "Advanced settings saved. Some changes require a restart."}
}

THEMES = {
    "yanix-default": {
        "background_color_start": "#ff4da6",
        "background_color_end": "#6666ff",
        "button_bg_color": "white",
        "button_text_color": "black",
        "button_hover_bg_color": "#f0f0f0",
        "label_text_color": "white",
        "border_color": "#ccc"
    },
    "dark": {
        "background_color_start": "#333333",
        "background_color_end": "#1a1a1a",
        "button_bg_color": "#555555",
        "button_text_color": "white",
        "button_hover_bg_color": "#777777",
        "label_text_color": "white",
        "border_color": "#666666"
    },
    "light": {
        "background_color_start": "#f0f0f0",
        "background_color_end": "#ffffff",
        "button_bg_color": "#e0e0e0",
        "button_text_color": "black",
        "button_hover_bg_color": "#cccccc",
        "label_text_color": "black",
        "border_color": "#aaaaaa"
    },
    "ocean-blue": {
        "background_color_start": "#007bff",
        "background_color_end": "#0056b3",
        "button_bg_color": "#6c757d",
        "button_text_color": "white",
        "button_hover_bg_color": "#5a6268",
        "label_text_color": "white",
        "border_color": "#495057"
    },
    "forest-green": {
        "background_color_start": "#28a745",
        "background_color_end": "#1e7e34",
        "button_bg_color": "#ffc107",
        "button_text_color": "black",
        "button_hover_bg_color": "#e0a800",
        "label_text_color": "white",
        "border_color": "#d39e00"
    }
}

def load_advanced_config():
    defaults = {
        "QT6FRAMEWORK": False,
        "BLOGLINK": "https://yanix-launcher.blogspot.com",
        "DISCORD_RPC": True
    }
    if not os.path.exists(ADVANCED_CONFIG_PATH):
        return defaults
    try:
        with open(ADVANCED_CONFIG_PATH, 'r') as f:
            config = json.load(f)
            defaults.update(config)
            return defaults
    except (json.JSONDecodeError, IOError):
        return defaults

def save_advanced_config(data):
    try:
        with open(ADVANCED_CONFIG_PATH, 'w') as f:
            json.dump(data, f, indent=4)
    except IOError:
        pass

def load_custom_theme(filepath, lang_data):
    try:
        with open(filepath, 'r') as f:
            theme_data = json.load(f)
        required_keys = ["background_color_start", "background_color_end",
                         "button_bg_color", "button_text_color",
                         "button_hover_bg_color", "label_text_color", "border_color"]
        if not all(key in theme_data for key in required_keys):
            raise ValueError("Invalid .yltheme file: missing required keys.")
        return theme_data
    except (FileNotFoundError, json.JSONDecodeError, ValueError) as e:
        QMessageBox.critical(None, lang_data["theme_error_title"], lang_data["theme_load_error"].format(filepath=filepath, e=e))
        return None

def get_language():
    try:
        if os.path.exists(LANG_PATH):
            with open(LANG_PATH, "r") as f:
                return f.read().strip()
    except IOError:
        pass
    return "en"

def get_theme():
    try:
        if os.path.exists(THEME_PATH):
            with open(THEME_PATH, "r") as f:
                theme_setting = f.read().strip()
                if theme_setting.endswith(".yltheme") and os.path.exists(theme_setting):
                    return theme_setting
                elif theme_setting in THEMES:
                    return theme_setting
    except IOError:
        pass
    return "yanix-default"

def get_wineprefix_path():
    try:
        if os.path.exists(WINEPREFIX_PATH):
            with open(WINEPREFIX_PATH, "r") as f:
                return f.read().strip()
    except IOError:
        pass
    return None

def check_internet_connection():
    try:
        socket.create_connection(("nikoyandere.github.io", 80), timeout=0.1)
        return True
    except OSError:
        return False

class DownloadSignals(QObject):
    update_splash = pyqtSignal(str, str)
    download_complete = pyqtSignal()
    download_failed = pyqtSignal(str)
    extraction_progress = pyqtSignal(int, int)
    extraction_complete = pyqtSignal()
    extraction_failed = pyqtSignal(str)

class UpdateCheckerSignals(QObject):
    update_status = pyqtSignal(str)
    update_found = pyqtSignal(str)

class YanixSplashScreen(QSplashScreen):
    def __init__(self, current_lang_data):
        super().__init__()
        self.current_lang = current_lang_data
        self.setFixedSize(600, 300)
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.message = ""
        self.progress_text = ""

        self.update_splash_content(self.current_lang["downloading_data"])

    def paintEvent(self, event):
        painter = QPainter(self)
        rect = self.rect()

        gradient = QLinearGradient(0, 0, 0, rect.height())
        gradient.setColorAt(0, QColor(THEMES["yanix-default"]["background_color_start"]))
        gradient.setColorAt(1, QColor(THEMES["yanix-default"]["background_color_end"]))
        painter.fillRect(rect, gradient)

        painter.setPen(QColor(0, 0, 0))
        painter.drawRect(rect.adjusted(20, 20, -20, -20))

        text_rect = QRect(rect.width() // 2 - 200, rect.height() // 2 - 50, 400, 100)

        font_title = QFont("Futura", 32, QFont.Bold)
        painter.setFont(font_title)
        painter.setPen(QColor(255, 255, 255))
        painter.drawText(text_rect, Qt.AlignCenter, "Yanix Launcher")

        font_message = QFont("Futura", 16)
        painter.setFont(font_message)
        painter.setPen(QColor(0, 0, 0))
        message_rect = QRect(rect.width() // 2 - 200, rect.height() // 2 + 10, 400, 50)
        painter.drawText(message_rect, Qt.AlignCenter, self.message)

        font_progress = QFont("Futura", 12)
        painter.setFont(font_progress)
        painter.setPen(QColor(0, 0, 0))
        progress_rect = QRect(rect.width() - 150, rect.height() - 50, 100, 30)
        painter.drawText(progress_rect, Qt.AlignRight | Qt.AlignBottom, self.progress_text)

    def update_splash_content(self, message, progress=""):
        self.message = message
        self.progress_text = progress
        self.repaint()

class DataDownloader(QObject):
    def __init__(self, current_lang_data, signals):
        super().__init__()
        self.current_lang_data = current_lang_data
        self.signals = signals

    def run(self):
        target_data_folder = os.path.join(YANIX_PATH, "data")

        if os.path.exists(target_data_folder) and os.listdir(target_data_folder):
            self.signals.download_complete.emit()
            return

        if not check_internet_connection():
            if os.path.exists(target_data_folder):
                self.signals.download_complete.emit()
                return
            else:
                self.signals.download_failed.emit(self.current_lang_data["no_internet"])
                return

        self.signals.update_splash.emit(self.current_lang_data["downloading_data"], "")
        try:
            headers = {'User-Agent': USER_AGENT}
            response = requests.get(DATA_DOWNLOAD_URL, stream=True, timeout=10, headers=headers)
            response.raise_for_status()

            total_size = int(response.headers.get('content-length', 0))
            downloaded_size = 0
            with open(TEMP_ZIP_PATH, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
                    downloaded_size += len(chunk)
                    self.signals.update_splash.emit(
                        self.current_lang_data["downloading_data"],
                        f"{downloaded_size / (1024 * 1024):.1f}MB / {total_size / (1024 * 1024):.1f}MB" if total_size > 0 else "..."
                    )

        except requests.exceptions.Timeout:
            self.signals.download_failed.emit(f"{self.current_lang_data['download_failed']} (Connection timeout).")
            if os.path.exists(TEMP_ZIP_PATH):
                os.remove(TEMP_ZIP_PATH)
            return
        except requests.exceptions.ConnectionError:
            self.signals.download_failed.emit(f"{self.current_lang_data['download_failed']} (Connection error. Check URL or internet connection).")
            if os.path.exists(TEMP_ZIP_PATH):
                os.remove(TEMP_ZIP_PATH)
            return
        except requests.exceptions.RequestException as e:
            self.signals.download_failed.emit(f"{self.current_lang_data['download_failed']} (Error: {e}).")
            if os.path.exists(TEMP_ZIP_PATH):
                os.remove(TEMP_ZIP_PATH)
            return
        except Exception as e:
            self.signals.download_failed.emit(f"{self.current_lang_data['download_failed']} (Unexpected error during download: {e}).")
            if os.path.exists(TEMP_ZIP_PATH):
                os.remove(TEMP_ZIP_PATH)
            return

        self.signals.update_splash.emit(self.current_lang_data["extracting_data"], "")
        try:
            os.makedirs(target_data_folder, exist_ok=True)
            with zipfile.ZipFile(TEMP_ZIP_PATH, 'r') as zip_ref:
                file_list = zip_ref.namelist()
                total_files = len(file_list)
                extracted_count = 0

                for file in file_list:
                    zip_ref.extract(file, target_data_folder)
                    extracted_count += 1
                    self.signals.extraction_progress.emit(extracted_count, total_files)

            self.signals.extraction_complete.emit()

        except zipfile.BadZipFile as e:
            self.signals.extraction_failed.emit(f"{self.current_lang_data['extract_failed']} (Corrupted or invalid ZIP file: {e}).")
            if os.path.exists(TEMP_ZIP_PATH):
                os.remove(TEMP_ZIP_PATH)
            shutil.rmtree(target_data_folder, ignore_errors=True)
            return
        except Exception as e:
            self.signals.extraction_failed.emit(f"{self.current_lang_data['extract_failed']} (Unexpected error during extraction: {e}).")
            if os.path.exists(TEMP_ZIP_PATH):
                os.remove(TEMP_ZIP_PATH)
            shutil.rmtree(target_data_folder, ignore_errors=True)
            return
        finally:
            if os.path.exists(TEMP_ZIP_PATH):
                os.remove(TEMP_ZIP_PATH)

class UpdateChecker(QObject):
    def __init__(self, current_version, lang_data, signals):
        super().__init__()
        self.current_version = current_version
        self.lang_data = lang_data
        self.signals = signals

    def parse_version_string(self, content):
        for line in content.splitlines():
            if 'USER_AGENT' in line:
                try:
                    version_str = line.split('/')[-1].strip().strip("'\"")
                    return tuple(map(int, version_str.split('.')))
                except (IndexError, ValueError):
                    return None
        return None

    def run(self):
        if not check_internet_connection():
            self.signals.update_status.emit(self.lang_data["no_internet"])
            return

        temp_file = None
        try:
            response = requests.get(LATEST_VERSION_URL, timeout=5)
            response.raise_for_status()
            latest_content = response.text

            with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.py') as tf:
                tf.write(latest_content)
            temp_file = tf.name

            latest_version_tuple = self.parse_version_string(latest_content)

            if latest_version_tuple is None:
                self.signals.update_status.emit(self.lang_data["update_error"])
                return

            current_version_tuple = tuple(map(int, self.current_version.split('.')))

            if latest_version_tuple > current_version_tuple:
                self.signals.update_found.emit(temp_file)
            else:
                if temp_file:
                    os.remove(temp_file)
                if latest_version_tuple < current_version_tuple:
                    self.signals.update_status.emit(self.lang_data["update_developer"])
                else:
                    self.signals.update_status.emit(self.lang_data["update_uptodate"])

        except requests.exceptions.RequestException:
            if temp_file and os.path.exists(temp_file):
                os.remove(temp_file)
            self.signals.update_status.emit(self.lang_data["update_error"])
        except Exception:
            if temp_file and os.path.exists(temp_file):
                os.remove(temp_file)
            self.signals.update_status.emit(self.lang_data["update_error"])


class SettingsDialog(QDialog):
    def __init__(self, lang_code, theme_name, lang_data, advanced_config, parent=None):
        super().__init__(parent)
        self.setWindowTitle(lang_data["settings"])
        self.setFixedSize(400, 250)
        self.advanced_config = advanced_config

        self.current_theme_name = theme_name

        layout = QVBoxLayout()

        lang_label = QLabel(lang_data["select_language"])
        layout.addWidget(lang_label)
        self.lang_selector = QComboBox()
        self.lang_selector.addItems(LANGUAGES.keys())
        self.lang_selector.setCurrentText(lang_code)
        layout.addWidget(self.lang_selector)

        theme_label = QLabel(lang_data["select_theme"])
        layout.addWidget(theme_label)
        self.theme_selector = QComboBox()
        self.update_theme_selector_items()
        self.theme_selector.setCurrentText(self.current_theme_name)
        layout.addWidget(self.theme_selector)

        self.load_custom_theme_button = QPushButton(lang_data["load_custom_theme"])
        self.load_custom_theme_button.clicked.connect(self.load_custom_theme_file)
        layout.addWidget(self.load_custom_theme_button)

        if os.path.exists(ADVANCED_FLAG_PATH):
            self.setup_advanced_settings(layout)
            self.setFixedSize(400, 450)

        self.apply_btn = QPushButton(lang_data["apply"])
        self.apply_btn.clicked.connect(self.apply_settings)
        layout.addWidget(self.apply_btn)

        self.setLayout(layout)
        self.apply_theme_to_settings_buttons()

    def setup_advanced_settings(self, layout):
        adv_label = QLabel("Advanced Settings")
        adv_label.setStyleSheet("font-weight: bold; margin-top: 10px;")
        layout.addWidget(adv_label)

        self.qt6_checkbox = QCheckBox("Enable PyQt6 Framework (Requires Restart)")
        self.qt6_checkbox.setChecked(self.advanced_config.get("QT6FRAMEWORK", False))
        layout.addWidget(self.qt6_checkbox)

        blog_link_label = QLabel("Blog Link URL")
        layout.addWidget(blog_link_label)
        self.blog_link_edit = QLineEdit()
        self.blog_link_edit.setText(self.advanced_config.get("BLOGLINK", ""))
        layout.addWidget(self.blog_link_edit)

        self.discord_rpc_checkbox = QCheckBox("Enable Discord Rich Presence")
        self.discord_rpc_checkbox.setChecked(self.advanced_config.get("DISCORD_RPC", True))
        layout.addWidget(self.discord_rpc_checkbox)

    def apply_theme_to_settings_buttons(self):
        theme = self.parent().get_current_theme_data()
        button_style = f"""
            QPushButton {{
                color: {theme["button_text_color"]};
                background-color: {theme["button_bg_color"]};
                padding: 8px;
                border-radius: 6px;
                border: 1px solid {theme["border_color"]};
            }}
            QPushButton:hover {{
                background-color: {theme["button_hover_bg_color"]};
            }}
        """
        self.apply_btn.setStyleSheet(button_style)
        self.load_custom_theme_button.setStyleSheet(button_style)

    def update_theme_selector_items(self):
        self.theme_selector.clear()
        self.theme_selector.addItems(THEMES.keys())
        custom_themes = [f for f in os.listdir(CUSTOM_THEMES_DIR) if f.endswith(".yltheme")]
        for theme_file in custom_themes:
            self.theme_selector.addItem(os.path.join(CUSTOM_THEMES_DIR, theme_file))

    def load_custom_theme_file(self):
        file, _ = QFileDialog.getOpenFileName(self, self.parent().lang["load_custom_theme"], CUSTOM_THEMES_DIR, "Yanix Theme Files (*.yltheme)")
        if file:
            theme_data = load_custom_theme(file, self.parent().lang)
            if theme_data:
                try:
                    with open(THEME_PATH, "w") as f:
                        f.write(file)
                    self.current_theme_name = file
                    self.update_theme_selector_items()
                    self.theme_selector.setCurrentText(file)
                    QMessageBox.information(self, self.parent().lang["success_title"], self.parent().lang["theme_changed"])
                    if self.parent():
                        self.parent().apply_theme(self.current_theme_name)
                        self.apply_theme_to_settings_buttons()
                except IOError as e:
                    QMessageBox.critical(self, self.parent().lang["error_title"], self.parent().lang["theme_save_error"].format(e=e))

    def apply_settings(self):
        new_lang = self.lang_selector.currentText()
        advanced_message = ""

        if hasattr(self, 'qt6_checkbox'):
            new_advanced_config = {
                "QT6FRAMEWORK": self.qt6_checkbox.isChecked(),
                "BLOGLINK": self.blog_link_edit.text(),
                "DISCORD_RPC": self.discord_rpc_checkbox.isChecked()
            }
            save_advanced_config(new_advanced_config)
            advanced_message = f'\n\n{self.parent().lang["advanced_settings_applied"]}'

        try:
            with open(LANG_PATH, "w") as f:
                f.write(new_lang)

            message = LANGUAGES[new_lang]["lang_changed"]
            if new_lang not in ["en", "pt", "ndk"]:
                message += f'\n\n{LANGUAGES[new_lang]["lang_ai_warning"]}'

            QMessageBox.information(self, LANGUAGES[new_lang]["info_title"], message + advanced_message)
        except IOError as e:
            QMessageBox.critical(self, self.parent().lang["error_title"], self.parent().lang["lang_save_error"].format(e=e))

        new_theme = self.theme_selector.currentText()
        try:
            with open(THEME_PATH, "w") as f:
                f.write(new_theme)
            if self.parent():
                self.parent().apply_theme(new_theme)
                self.apply_theme_to_settings_buttons()
                if not advanced_message:
                    QMessageBox.information(self, self.parent().lang["info_title"], self.parent().lang["theme_changed"])
        except IOError as e:
            QMessageBox.critical(self, self.parent().lang["error_title"], self.parent().lang["theme_save_error"].format(e=e))

        if self.parent():
            self.parent().retranslate_ui()

        self.accept()

class DownloadWorker(QObject):
    progress = pyqtSignal(int, str)
    finished = pyqtSignal()
    error = pyqtSignal(str, str)
    extraction_started = pyqtSignal(int)
    extraction_finished = pyqtSignal()

    def __init__(self, url, dest_path, install_path, lang_data):
        super().__init__()
        self.url = url
        self.dest_path = dest_path
        self.install_path = install_path
        self.lang = lang_data
        self._is_running = True

    def run(self):
        try:
            headers = {'User-Agent': USER_AGENT}
            response = requests.get(self.url, stream=True, timeout=30, headers=headers)
            response.raise_for_status()
            total_size = int(response.headers.get('content-length', 0))

            downloaded_size = 0
            with open(self.dest_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if not self._is_running:
                        raise InterruptedError(self.lang["download_canceled"])
                    f.write(chunk)
                    downloaded_size += len(chunk)
                    if total_size > 0:
                        progress_percentage = int((downloaded_size / total_size) * 100)
                        downloaded_mb = f"{downloaded_size / (1024*1024):.2f}MB"
                        total_mb = f"{total_size / (1024*1024):.2f}MB"
                        progress_text = self.lang["downloading_label"].format(downloaded=downloaded_mb, total=total_mb, percentage=progress_percentage)
                        self.progress.emit(progress_percentage, progress_text)
                    else:
                        downloaded_mb = f"{downloaded_size / (1024*1024):.2f}MB"
                        progress_text = self.lang["downloading_label_no_total"].format(downloaded=downloaded_mb)
                        self.progress.emit(0, progress_text)

            os.makedirs(self.install_path, exist_ok=True)
            with zipfile.ZipFile(self.dest_path, 'r') as zip_ref:
                self.extraction_started.emit(0)
                zip_ref.extractall(self.install_path)

            source_dir = self.install_path
            extracted_items = os.listdir(self.install_path)
            if len(extracted_items) == 1:
                potential_subfolder = os.path.join(self.install_path, extracted_items[0])
                if os.path.isdir(potential_subfolder):
                    source_dir = potential_subfolder

            if source_dir != self.install_path:
                for item_name in list(os.listdir(source_dir)):
                    source_item_path = os.path.join(source_dir, item_name)
                    destination_item_path = os.path.join(self.install_path, item_name)
                    shutil.move(source_item_path, destination_item_path)
                os.rmdir(source_dir)

            self.extraction_finished.emit()

        except InterruptedError as e:
            self.error.emit("canceled", str(e))
        except requests.exceptions.RequestException as e:
            self.error.emit("download_failed", str(e))
        except zipfile.BadZipFile as e:
            self.error.emit("extract_failed", str(e))
        except Exception as e:
            self.error.emit("error_title", self.lang["unexpected_error"].format(e=e))
        finally:
            if os.path.exists(self.dest_path):
                os.remove(self.dest_path)
            self.finished.emit()

    def stop(self):
        self._is_running = False

class YanixLauncher(QMainWindow):
    game_finished = pyqtSignal()
    update_checker_signals = UpdateCheckerSignals()

    def __init__(self):
        super().__init__()
        self.advanced_config = load_advanced_config()
        self.lang_code = get_language()
        self.current_theme_name = get_theme()
        self.lang = LANGUAGES.get(self.lang_code, LANGUAGES["en"])
        self.wineprefix = get_wineprefix_path()
        self.current_launcher_version = USER_AGENT.split('/')[-1]

        self.setWindowTitle("Yanix Launcher")
        self.setFixedSize(1100, 600)

        if os.path.exists(ICON_PATH):
            self.setWindowIcon(QIcon(ICON_PATH))

        self.rpc = None
        self.start_time = int(time.time())
        if presence_enabled and self.advanced_config.get("DISCORD_RPC", True):
            self.init_rpc()

        self.setup_ui()
        self.retranslate_ui()
        self.apply_theme(self.current_theme_name)
        self.game_finished.connect(self._on_game_finished)
        self.update_checker_signals.update_status.connect(self._on_update_check_result)
        self.update_checker_signals.update_found.connect(self._on_update_found)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_F6 and event.modifiers() == Qt.ShiftModifier:
            if not os.path.exists(ADVANCED_FLAG_PATH):
                with open(ADVANCED_FLAG_PATH, "w") as f:
                    f.write("enabled")
                QMessageBox.information(self, "Advanced Mode", "Advanced mode will be enabled on next restart.")
            else:
                os.remove(ADVANCED_FLAG_PATH)
                QMessageBox.information(self, "Advanced Mode", "Advanced mode will be disabled on next restart.")
        else:
            super().keyPressEvent(event)

    def init_rpc(self):
        try:
            self.rpc = Presence(CLIENT_ID)
            self.rpc.connect()
            self.update_rpc(details="In the launcher", state="Browsing...")
        except Exception:
            self.rpc = None

    def update_rpc(self, details, state=None):
        if not self.rpc:
            return
        try:
            self.rpc.update(
                details=details,
                state=state,
                start=self.start_time,
                large_image="yanix_logo",
                large_text="Yanix Launcher"
            )
        except Exception:
            self.rpc.close()
            self.rpc = None

    def get_current_theme_data(self):
        if self.current_theme_name.endswith(".yltheme") and os.path.exists(self.current_theme_name):
            theme_data = load_custom_theme(self.current_theme_name, self.lang)
            if theme_data:
                return theme_data
        return THEMES.get(self.current_theme_name, THEMES["yanix-default"])

    def apply_theme(self, theme_name):
        self.current_theme_name = theme_name
        theme = self.get_current_theme_data()

        button_style = f"""
            QPushButton {{
                color: {theme["button_text_color"]};
                background-color: {theme["button_bg_color"]};
                padding: 8px;
                border-radius: 6px;
                border: 1px solid {theme["border_color"]};
            }}
            QPushButton:hover {{
                background-color: {theme["button_hover_bg_color"]};
            }}
        """
        for button in [self.play_button, self.settings_button, self.select_exe_button,
                       self.download_button, self.winetricks_button, self.wineprefix_button,
                       self.delete_game_button, self.check_updates_button,
                       self.support_button, self.discord_button]:
            button.setStyleSheet(button_style)

        self.version_label.setStyleSheet(f"color: {theme['label_text_color']}; margin-top: 20px;")

        blog_view_style = f"""
            QWebEngineView {{
                border: 2px solid {theme["border_color"]};
                border-radius: 8px;
            }}
        """
        self.blog_view.setStyleSheet(blog_view_style)

        palette = self.palette()
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0, QColor(theme["background_color_start"]))
        gradient.setColorAt(1, QColor(theme["background_color_end"]))
        palette.setBrush(QPalette.Window, QBrush(gradient))
        self.setPalette(palette)

    def _on_game_finished(self):
        self.show()
        self.update_rpc(details="In the launcher", state="Browsing...")

    def _wait_for_game_exit(self, process):
        process.wait()
        self.game_finished.emit()

    def launch_game(self):
        game_to_launch = None
        game_dir = None
        wine_needed = True

        if os.path.exists(CONFIG_PATH):
            with open(CONFIG_PATH) as f:
                wine_path = f.read().strip()
            if os.path.exists(wine_path):
                game_to_launch = ["wine", wine_path]
                game_dir = os.path.dirname(wine_path)
            else:
                QMessageBox.critical(self, self.lang["error_title"], self.lang["game_path_invalid"])
                return
        elif os.path.exists(YAN_SIM_NATIVE_EXE_PATH):
            game_to_launch = ["wine", YAN_SIM_NATIVE_EXE_PATH]
            game_dir = YAN_SIM_INSTALL_PATH
        else:
            QMessageBox.critical(self, self.lang["error_title"], self.lang["game_path_undefined"])
            return

        if game_to_launch:
            try:
                env = os.environ.copy()
                if wine_needed and self.wineprefix:
                    env["WINEPREFIX"] = self.wineprefix

                self.hide()
                process = subprocess.Popen(game_to_launch, cwd=game_dir, env=env)

                self.update_rpc(details="Playing Yandere Simulator", state="In-Game")
                monitor_thread = threading.Thread(
                    target=self._wait_for_game_exit,
                    args=(process,),
                    daemon=True
                )
                monitor_thread.start()

            except FileNotFoundError:
                QMessageBox.critical(self, self.lang["error_title"], self.lang["wine_missing"])
                self.show()
                self.update_rpc(details="In the launcher", state="Browsing...")
            except Exception as e:
                QMessageBox.critical(self, self.lang["error_title"], self.lang["game_launch_fail"].format(e=e))
                self.show()
                self.update_rpc(details="In the launcher", state="Browsing...")

    def select_exe(self):
        file, _ = QFileDialog.getOpenFileName(self, self.lang["select_exe_window_title"], "", self.lang["exe_file_filter"])
        if file:
            try:
                with open(CONFIG_PATH, "w") as f:
                    f.write(file)
                QMessageBox.information(self, self.lang["success_title"], self.lang["exe_save_success"])
            except IOError as e:
                QMessageBox.critical(self, self.lang["error_title"], self.lang["exe_save_fail"].format(e=e))

    def select_wineprefix(self):
        directory = QFileDialog.getExistingDirectory(self, self.lang["wineprefix"])
        if directory:
            try:
                with open(WINEPREFIX_PATH, "w") as f:
                    f.write(directory)
                self.wineprefix = directory
                QMessageBox.information(self, self.lang["success_title"], self.lang["wineprefix_selected"])
            except IOError as e:
                QMessageBox.critical(self, self.lang["error_title"], self.lang['wineprefix_error'].format(e=e))

    def download_game(self):
        if not check_internet_connection():
            QMessageBox.critical(self, self.lang["no_internet_title"], self.lang["no_internet"])
            return

        yan_sim_zip_path = os.path.join(YANIX_PATH, "yansim.zip")

        if os.path.exists(YAN_SIM_NATIVE_EXE_PATH):
            QMessageBox.information(self, self.lang["info_title"], self.lang["game_installed"])
            return

        reply = QMessageBox.question(self, self.lang["download_game_window_title"],
                                     self.lang["download_game_prompt"],
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.No:
            return

        self.progress_dialog = QProgressDialog(self.lang.get("connecting", "Connecting..."), self.lang.get("cancel", "Cancel"), 0, 100, self)
        self.progress_dialog.setWindowTitle(self.lang["download_progress_window_title"])
        self.progress_dialog.setWindowModality(Qt.WindowModal)
        self.progress_dialog.setFixedSize(self.progress_dialog.size())

        self.thread = QThread()
        self.worker = DownloadWorker(YAN_SIM_DOWNLOAD_URL, yan_sim_zip_path, YAN_SIM_INSTALL_PATH, self.lang)
        self.worker.moveToThread(self.thread)

        self.progress_dialog.canceled.connect(self.cancel_download)
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.worker.progress.connect(self.update_download_progress)
        self.worker.error.connect(self.on_download_error)

        self.worker.extraction_started.connect(self.start_extraction_progress)
        self.worker.extraction_finished.connect(self.on_extraction_finished)

        self.thread.start()
        self.progress_dialog.show()

    def cancel_download(self):
        if hasattr(self, 'worker'):
            self.worker.stop()
        if hasattr(self, 'progress_dialog') and self.progress_dialog.isVisible():
            self.progress_dialog.close()
        if hasattr(self, 'extract_dialog') and self.extract_dialog.isVisible():
            self.extract_dialog.close()

    def update_download_progress(self, percentage, text):
        self.progress_dialog.setValue(percentage)
        self.progress_dialog.setLabelText(text)

    def on_download_error(self, title_key, message):
        if title_key == "canceled":
            return

        if hasattr(self, 'progress_dialog'):
            self.progress_dialog.close()
        if hasattr(self, 'extract_dialog'):
            self.extract_dialog.close()

        title = self.lang.get(title_key, self.lang["error_title"])
        QMessageBox.critical(self, title, message)

    def start_extraction_progress(self, total_files):
        self.progress_dialog.close()
        self.extract_dialog = QProgressDialog(self.lang["extracting_label"], self.lang.get("cancel", "Cancel"), 0, total_files, self)
        self.extract_dialog.setWindowTitle(self.lang["extraction_progress_window_title"])
        self.extract_dialog.setWindowModality(Qt.WindowModal)
        self.extract_dialog.setFixedSize(self.extract_dialog.size())
        self.extract_dialog.canceled.connect(self.cancel_download)
        self.extract_dialog.show()

    def on_extraction_finished(self):
        if hasattr(self, 'extract_dialog'):
            self.extract_dialog.close()
        QMessageBox.information(self, self.lang["success_title"], self.lang["game_download_success"])

    def delete_game(self):
        if not os.path.exists(YAN_SIM_INSTALL_PATH):
            QMessageBox.information(self, self.lang["info_title"], self.lang["game_not_found"])
            return

        reply = QMessageBox.question(self, self.lang["delete_game"],
                                     self.lang["delete_game_confirm"],
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            try:
                shutil.rmtree(YAN_SIM_INSTALL_PATH)
                if os.path.exists(CONFIG_PATH):
                    with open(CONFIG_PATH, 'r') as f:
                        configured_path = f.read().strip()
                    if configured_path.startswith(YAN_SIM_INSTALL_PATH):
                        os.remove(CONFIG_PATH)
                QMessageBox.information(self, self.lang["success_title"], self.lang["game_deleted_success"])
            except Exception as e:
                QMessageBox.critical(self, self.lang["error_title"], self.lang["game_delete_fail"].format(e=e))


    def manage_winetricks(self):
        if not shutil.which("winetricks"):
            QMessageBox.critical(self, self.lang["error_title"], self.lang["winetricks_missing"])
        else:
            try:
                env = os.environ.copy()
                if self.wineprefix:
                    env["WINEPREFIX"] = self.wineprefix
                subprocess.Popen(["winetricks"], env=env)
            except Exception as e:
                QMessageBox.critical(self, self.lang["error_title"], self.lang["winetricks_launch_fail"].format(e=e))

    def check_for_updates(self):
        update_worker = UpdateChecker(self.current_launcher_version, self.lang, self.update_checker_signals)
        threading.Thread(target=update_worker.run, daemon=True).start()

    def _on_update_check_result(self, message):
        QMessageBox.information(self, self.lang["check_updates"], message)

    def _on_update_found(self, temp_file_path):
        reply = QMessageBox.question(self, self.lang["check_updates"],
                                     self.lang["update_outdated"],
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        if reply == QMessageBox.Yes:
            try:
                with open(temp_file_path, 'r') as f_new:
                    new_code = f_new.read()

                with open(os.path.abspath(__file__), 'w') as f_old:
                    f_old.write(new_code)

                os.remove(temp_file_path)

                QMessageBox.information(self, self.lang["check_updates"], self.lang["update_restart_prompt"])

                os.execv(sys.executable, ['python3'] + sys.argv)

            except Exception as e:
                QMessageBox.critical(self, self.lang["update_error_window_title"], self.lang["update_fail"].format(e=e))
                if os.path.exists(temp_file_path):
                    os.remove(temp_file_path)

    def open_settings(self):
        dlg = SettingsDialog(self.lang_code, self.current_theme_name, self.lang, self.advanced_config, self)
        dlg.exec_()
        self.advanced_config = load_advanced_config()
        self.blog_view.load(QUrl(self.advanced_config.get("BLOGLINK", "https://yanix-launcher.blogspot.com")))

    def closeEvent(self, event):
        if self.rpc:
            self.rpc.close()
        event.accept()

    def retranslate_ui(self):
        self.lang_code = get_language()
        self.lang = LANGUAGES.get(self.lang_code, LANGUAGES["en"])

        self.play_button.setText(self.lang["play"])
        self.settings_button.setText(self.lang["settings"])
        self.select_exe_button.setText(self.lang["select_exe"])
        self.download_button.setText(self.lang["download"])
        self.winetricks_button.setText(self.lang["winetricks"])
        self.wineprefix_button.setText(self.lang["wineprefix"])
        self.delete_game_button.setText(self.lang["delete_game"])
        self.check_updates_button.setText(self.lang["check_updates"])
        self.support_button.setText(self.lang["support"])
        self.discord_button.setText(self.lang["discord"])
        self.version_label.setText(f"{self.lang['welcome']} V {self.current_launcher_version}")

        self.apply_theme(self.current_theme_name)

    def setup_ui(self):
        main_layout = QHBoxLayout()
        self.left_layout = QVBoxLayout()
        self.left_layout.setAlignment(Qt.AlignTop)

        font = QFont("Futura", 16)
        version_font = QFont("Futura", 10)

        self.play_button = QPushButton()
        self.play_button.setFont(font)
        self.play_button.clicked.connect(self.launch_game)
        self.left_layout.addWidget(self.play_button)

        self.settings_button = QPushButton()
        self.settings_button.setFont(font)
        self.settings_button.clicked.connect(self.open_settings)
        self.left_layout.addWidget(self.settings_button)

        self.select_exe_button = QPushButton()
        self.select_exe_button.setFont(font)
        self.select_exe_button.clicked.connect(self.select_exe)
        self.left_layout.addWidget(self.select_exe_button)

        self.download_button = QPushButton()
        self.download_button.setFont(font)
        self.download_button.clicked.connect(self.download_game)
        self.left_layout.addWidget(self.download_button)

        self.winetricks_button = QPushButton()
        self.winetricks_button.setFont(font)
        self.winetricks_button.clicked.connect(self.manage_winetricks)
        self.left_layout.addWidget(self.winetricks_button)

        self.wineprefix_button = QPushButton()
        self.wineprefix_button.setFont(font)
        self.wineprefix_button.clicked.connect(self.select_wineprefix)
        self.left_layout.addWidget(self.wineprefix_button)

        self.delete_game_button = QPushButton()
        self.delete_game_button.setFont(font)
        self.delete_game_button.clicked.connect(self.delete_game)
        self.left_layout.addWidget(self.delete_game_button)

        self.check_updates_button = QPushButton()
        self.check_updates_button.setFont(font)
        self.check_updates_button.clicked.connect(self.check_for_updates)
        self.left_layout.addWidget(self.check_updates_button)

        self.support_button = QPushButton()
        self.support_button.setFont(font)
        self.support_button.clicked.connect(lambda: webbrowser.open("https://gitea.com/YanixLauncher/Yanix-Launcher-Gitea/issues"))
        self.left_layout.addWidget(self.support_button)

        self.discord_button = QPushButton()
        self.discord_button.setFont(font)
        self.discord_button.clicked.connect(lambda: webbrowser.open("https://discord.gg/7JC4FGn69U"))
        self.left_layout.addWidget(self.discord_button)

        self.version_label = QLabel()
        self.version_label.setFont(version_font)
        self.left_layout.addWidget(self.version_label)

        self.blog_view = QWebEngineView()
        self.blog_view.load(QUrl(self.advanced_config.get("BLOGLINK", "https://yanix-launcher.blogspot.com")))

        main_layout.addLayout(self.left_layout, 1)
        main_layout.addWidget(self.blog_view, 2)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)


if __name__ == "__main__":
    QCoreApplication.setAttribute(Qt.AA_ShareOpenGLContexts, True)
    app = QApplication(sys.argv)

    lang_code = get_language()
    current_lang_data = LANGUAGES.get(lang_code, LANGUAGES["en"])

    splash = YanixSplashScreen(current_lang_data)
    splash.show()

    signals = DownloadSignals()
    signals.update_splash.connect(splash.update_splash_content)
    signals.download_failed.connect(lambda msg: QMessageBox.critical(None, current_lang_data["download_failed"], msg))
    signals.extraction_progress.connect(lambda current, total: splash.update_splash_content(current_lang_data["extracting_data"], f"({current}/{total} files)"))
    signals.extraction_failed.connect(lambda msg: QMessageBox.critical(None, current_lang_data["extract_failed"], msg))

    downloader_thread = threading.Thread(target=DataDownloader(current_lang_data, signals).run, daemon=True)

    signals.download_complete.connect(lambda: splash.update_splash_content(current_lang_data["download_success"]))
    signals.extraction_complete.connect(lambda: splash.update_splash_content(current_lang_data["download_success"]))

    downloader_thread.start()

    while downloader_thread.is_alive():
        QApplication.processEvents()
        time.sleep(0.1)

    launcher = YanixLauncher()
    launcher.show()
    splash.finish(launcher)

    sys.exit(app.exec_())
