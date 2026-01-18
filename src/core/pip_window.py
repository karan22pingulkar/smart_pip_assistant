from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel
from PyQt6.QtCore import Qt, QPoint, QUrl
from PyQt6.QtWebEngineWidgets import QWebEngineView


class PipWindow(QMainWindow):
    """
    A Zen-Browser style Picture-in-Picture player for your college project.
    Extracts ONLY the video element with dedicated Top-Bar buttons for resizing.
    """

    def __init__(self, config_manager):
        super().__init__()
        self.config_manager = config_manager
        self.settings = self.config_manager.load_settings()
        self.drag_start_position = QPoint()

        self.init_ui()
        self.setup_layout()

    def init_ui(self):
        """Sets top-level window flags and initial dimensions."""
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.SubWindow
        )

        # Defaulting to standard 16:9 widescreen player size (640x360) + 32px top bar
        self.setGeometry(
            self.settings.get("x_position", 100),
            self.settings.get("y_position", 100),
            self.settings.get("width", 640),
            self.settings.get("height", 392)
        )
        self.setWindowOpacity(self.settings.get("opacity", 0.98))

    def setup_layout(self):
        """Constructs the frame layout hierarchy with high-visibility controls."""
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # 1. Top Bar Control Panel
        self.top_bar = QWidget(self.central_widget)
        self.top_bar.setFixedHeight(32)
        self.top_bar.setStyleSheet(
            "background-color: #1A1A1A; border-bottom: 1px solid #2A2A2A;")

        self.top_layout = QHBoxLayout(self.top_bar)
        self.top_layout.setContentsMargins(12, 0, 12, 0)
        self.top_layout.setSpacing(8)

        self.title_label = QLabel("📺 Pure Video PiP Mode", self.top_bar)
        self.title_label.setStyleSheet(
            "font-size: 11px; font-weight: bold; color: #FFFFFF;")
        self.top_layout.addWidget(self.title_label)

        self.top_layout.addStretch()

        # BUTTON A: Enlarge Window (Scale Up)
        self.enlarge_btn = QPushButton("＋", self.top_bar)
        self.enlarge_btn.setFixedSize(24, 22)
        self.enlarge_btn.setToolTip("Enlarge Window Size")
        self.enlarge_btn.setStyleSheet(
            "background: #3A3A3A; color: #FFFFFF; border: none; font-weight: bold; font-size: 14px; border-radius: 4px;"
            "QPushButton:hover { background: #555555; }"
        )
        self.enlarge_btn.clicked.connect(lambda: self.scale_window(50))
        self.top_layout.addWidget(self.enlarge_btn)

        # BUTTON B: Shrink Window (Scale Down)
        self.shrink_btn = QPushButton("－", self.top_bar)
        self.shrink_btn.setFixedSize(24, 22)
        self.shrink_btn.setToolTip("Shrink Window Size")
        self.shrink_btn.setStyleSheet(
            "background: #3A3A3A; color: #FFFFFF; border: none; font-weight: bold; font-size: 14px; border-radius: 4px;"
            "QPushButton:hover { background: #555555; }"
        )
        self.shrink_btn.clicked.connect(lambda: self.scale_window(-50))
        self.top_layout.addWidget(self.shrink_btn)

        # BUTTON C: Close Application
        self.close_btn = QPushButton("✕", self.top_bar)
        self.close_btn.setFixedSize(24, 22)
        self.close_btn.setStyleSheet(
            "background: #D32F2F; color: #FFFFFF; border: none; font-weight: bold; font-size: 12px; border-radius: 4px;"
            "QPushButton:hover { background: #F44336; }"
        )
        self.close_btn.clicked.connect(self.close_application)
        self.top_layout.addWidget(self.close_btn)

        self.main_layout.addWidget(self.top_bar)

        # 2. Chromium Web View Window Segment
        self.browser = QWebEngineView(self.central_widget)
        self.main_layout.addWidget(self.browser, stretch=1)

        # --- ZEN EXTRACTOR: Inject custom DOM styling when a video page loads ---
        self.browser.loadFinished.connect(self.isolate_html5_video)

    def scale_window(self, delta_width: int):
        """Calculates and applies an active widescreen proportional 16:9 resize modifier."""
        geom = self.geometry()
        new_w = geom.width() + delta_width
        new_h = int((new_w - 32) * (9 / 16)) + 32

        if 320 <= new_w <= 1280:
            self.resize(new_w, new_h)

    def isolate_html5_video(self):
        """Strips away page wrappers to target just the raw video container element."""
        js_injection = """
        (function() {
            let videoContainer = document.querySelector('.html5-video-player') || 
                                 document.querySelector('video') || 
                                 document.querySelector('#player');
                                 
            if (videoContainer) {
                document.body.style.overflow = 'hidden';
                for (let child of document.body.children) {
                    child.style.display = 'none';
                }
                document.body.appendChild(videoContainer);
                videoContainer.style.display = 'block';
                videoContainer.style.position = 'fixed';
                videoContainer.style.top = '0';
                videoContainer.style.left = '0';
                videoContainer.style.width = '100%';
                videoContainer.style.height = '100%';
                videoContainer.style.zIndex = '999999';
            }
        })();
        """
        self.browser.page().runJavaScript(js_injection)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton and event.position().y() <= self.top_bar.height():
            self.drag_start_position = event.globalPosition().toPoint() - \
                self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton and not self.drag_start_position.isNull():
            self.move(event.globalPosition().toPoint() -
                      self.drag_start_position)
            event.accept()

    def mouseReleaseEvent(self, event):
        self.drag_start_position = QPoint()

    def load_url(self, url: str):
        self.browser.setUrl(QUrl(url))

    def close_application(self):
        geom = self.geometry()
        self.settings["x_position"] = geom.x()
        self.settings["y_position"] = geom.y()
        self.settings["width"] = geom.width()
        self.settings["height"] = geom.height()
        self.config_manager.save_settings(self.settings)
        self.close()
