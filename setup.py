from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.clock import Clock
from kivy.metrics import dp
import os
from kivy.utils import get_color_from_hex

# Define the modern UI styling using Kivy Language
Builder.load_string('''
#:import utils kivy.utils

<ModernButton@Button>:
    background_normal: ''
    background_color: utils.get_color_from_hex('#2196F3')
    color: 1, 1, 1, 1
    size_hint: (None, None)
    size: (dp(200), dp(50))
    font_size: '18sp'
    canvas.before:
        Color:
            rgba: utils.get_color_from_hex('#1976D2') if self.state == 'down' else self.background_color
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [dp(25)]

<UploadScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: dp(20)
        spacing: dp(20)

        Widget:
            size_hint_y: 0.2

        Label:
            text: 'Upload Your Image'
            font_size: '24sp'
            size_hint_y: None
            height: dp(50)
            color: utils.get_color_from_hex('#333333')

        BoxLayout:
            orientation: 'vertical'
            size_hint_y: None
            height: dp(200)
            canvas.before:
                Color:
                    rgba: utils.get_color_from_hex('#E3F2FD')
                RoundedRectangle:
                    pos: self.pos
                    size: self.size
                    radius: [dp(15)]
                Line:
                    rounded_rectangle: [self.x, self.y, self.width, self.height, dp(15)]
                    dash_offset: dp(5)
                    dash_length: dp(10)
                    width: dp(2)

            Label:
                text: root.upload_status
                color: utils.get_color_from_hex('#666666')
                font_size: '16sp'

            Image:
                source: 'data/icons/upload.png' if root.upload_icon else ''
                size_hint: None, None
                size: dp(64), dp(64)
                pos_hint: {'center_x': 0.5}

        ModernButton:
            text: 'Select File'
            pos_hint: {'center_x': 0.5}
            on_release: root.select_file()

        Widget:
            size_hint_y: 0.2

<DisplayScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: dp(20)
        spacing: dp(20)

        BoxLayout:
            size_hint_y: None
            height: dp(50)
            spacing: dp(10)

            ModernButton:
                text: 'Back'
                size: (dp(100), dp(40))
                on_release: root.go_back()

            Widget:
                size_hint_x: 0.7

            ModernButton:
                text: 'Share'
                size: (dp(100), dp(40))
                on_release: root.share_image()

        Image:
            id: display_image
            source: root.image_source
            allow_stretch: True
            keep_ratio: True

        BoxLayout:
            size_hint_y: None
            height: dp(50)
            spacing: dp(10)

            ModernButton:
                text: 'Edit'
                on_release: root.edit_image()
                pos_hint: {'center_x': 0.5}
''')


class UploadScreen(Screen):
    upload_status = StringProperty('Drag and drop your image here\nor click Select File')
    upload_icon = StringProperty('True')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.bind(on_dropfile=self._on_file_drop)

        # Create 'data/icons' directory if it doesn't exist
        if not os.path.exists('data/icons'):
            os.makedirs('data/icons')

        # Here you would normally have your upload icon
        # For this example, we'll just use text

    def _on_file_drop(self, window, file_path):
        """Handle dropped files"""
        file_path = file_path.decode('utf-8')
        if self._validate_file(file_path):
            self._process_file(file_path)
            return True
        return False

    def select_file(self):
        """Handle file selection button press"""
        # In a real app, you'd use plyer or other file chooser
        # For this example, we'll simulate a file selection
        self._simulate_file_selected()

    def _simulate_file_selected(self):
        """Simulate file selection for demonstration"""
        self.upload_status = 'Processing...'
        self.upload_icon = 'False'
        Clock.schedule_once(lambda dt: self._process_file('simulated_path.jpg'), 1)

    def _validate_file(self, file_path):
        """Validate the file type"""
        valid_extensions = ['.jpg', '.jpeg', '.png', '.gif']
        return any(file_path.lower().endswith(ext) for ext in valid_extensions)

    def _process_file(self, file_path):
        """Process the uploaded file"""
        # In a real app, you'd process the actual file
        # For demo, we'll just transition to display screen
        self.manager.transition = SlideTransition(direction='left')
        display_screen = self.manager.get_screen('display')
        display_screen.image_source = file_path
        self.manager.current = 'display'

        # Reset upload screen state
        Clock.schedule_once(lambda dt: self._reset_state(), 1)

    def _reset_state(self):
        """Reset the upload screen state"""
        self.upload_status = 'Drag and drop your image here\nor click Select File'
        self.upload_icon = 'True'


class DisplayScreen(Screen):
    image_source = StringProperty('')

    def go_back(self):
        """Return to upload screen"""
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = 'upload'

    def share_image(self):
        """Share the image"""
        # Implement sharing functionality
        pass

    def edit_image(self):
        """Edit the image"""
        # Implement editing functionality
        pass


class ImageUploadApp(App):
    def build(self):
        # Create the screen manager
        sm = ScreenManager(transition=SlideTransition())

        # Add screens
        sm.add_widget(UploadScreen(name='upload'))
        sm.add_widget(DisplayScreen(name='display'))

        # Set window properties
        Window.size = (400, 600)
        Window.clearcolor = get_color_from_hex('#FFFFFF')

        return sm


if __name__ == '__main__':
    ImageUploadApp().run()