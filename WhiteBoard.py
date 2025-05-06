from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.widget import Widget
from kivy.graphics import Color, Line, Rectangle
from alert import email_alert, send_to, phone_providers

class DrawInput(Widget):
    """Whiteboard for drawing custom churro shapes."""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.draw_area = (0, 0, 0, 0)  # Will be set in on_size
        self.bind(size=self.update_draw_area, pos=self.update_draw_area)

    def update_draw_area(self, *args):
        # Define a centered 200x200 draw area inside the widget
        margin = 20
        x = self.x + margin
        y = self.y + (self.height - 200) / 2  # vertically center
        w = self.width - 2 * margin
        h = 200
        self.draw_area = (x, y, w, h)

        # Draw the box
        self.canvas.before.clear()
        with self.canvas.before:
            Color(1, 1, 1, 0.3)
            Rectangle(pos=(x, y), size=(w, h))

    def on_touch_down(self, touch):
        if self._in_draw_area(touch.x, touch.y):
            with self.canvas:
                Color(1, 0, 0, 1)
                touch.ud["line"] = Line(points=(touch.x, touch.y))

    def on_touch_move(self, touch):
        if "line" in touch.ud and self._in_draw_area(touch.x, touch.y):
            touch.ud["line"].points += (touch.x, touch.y)

    def _in_draw_area(self, x, y):
        dx, dy, dw, dh = self.draw_area
        return dx <= x <= dx + dw and dy <= y <= dy + dh

    def clear_canvas(self):
        self.canvas.clear()
        self.update_draw_area()

class ChurroControlScreen(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', padding=40, spacing=20, **kwargs)

        with self.canvas.before:
            Color(0, 0, 0.5, 2)
            self.rect = Rectangle(size=self.size, pos=self.pos)

        self.bind(size=self.update_rect, pos=self.update_rect)

        self.selected_shape = 'Round'

        self.add_widget(Label(text='ChurroBot Control', font_size=40, color=(1, 1, 1, 1)))  # White Text

        self.add_widget(Label(text='Select Churro Shape:', font_size=20, color=(1, 1, 1, 1)))  # White Text
        shape_grid = GridLayout(cols=2, spacing=10, size_hint_y=None, height=150)

        self.shape_buttons = {}
        for shape in ['Round', 'Star', 'Heart', 'Custom']:
            btn = ToggleButton(text=shape, group='shapes', background_color=(0.2, 0.6, 1, 1))  # Light Blue Buttons
            btn.bind(on_press=self.set_selected_shape)
            shape_grid.add_widget(btn)
            self.shape_buttons[shape] = btn

        self.add_widget(shape_grid)

        self.add_widget(Label(text="Draw Your Custom Churro:", font_size=20, color=(1, 1, 1, 1)))  # White Text
        self.draw_input = DrawInput(size_hint_y=None, height=300)
        self.add_widget(self.draw_input)

        self.clear_button = Button(text="Clear Drawing", size_hint=(1, 0.2), background_color=(1, 0.3, 0.3, 1))  # Red
        self.clear_button.bind(on_press=lambda instance: self.draw_input.clear_canvas())
        self.add_widget(self.clear_button)

        # Email input
        self.add_widget(Label(text='Enter Email (if preferred):', font_size=20, color=(1, 1, 1, 1)))
        self.email_input = TextInput(hint_text='e.g., someone@example.com', multiline=False, size_hint_y=None, height=40)
        self.add_widget(self.email_input)

        # Phone number input
        self.add_widget(Label(text='Or Phone Number (10 digits):', font_size=20, color=(1, 1, 1, 1)))
        self.phone_input = TextInput(hint_text='e.g., 1234567890', multiline=False, size_hint_y=None, height=40)
        self.add_widget(self.phone_input)

        # Provider input
        self.add_widget(Label(text='And Phone Carrier (if SMS):', font_size=20, color=(1, 1, 1, 1)))
        self.provider_input = TextInput(hint_text='e.g., Verizon', multiline=False, size_hint_y=None, height=40)
        self.add_widget(self.provider_input)


        self.start_button = Button(text='Start', font_size=20, size_hint=(1, 0.3),
                                   background_color=(0, 1, 0, 1))  # Green
        self.start_button.bind(on_press=self.start_churro_making)
        self.add_widget(self.start_button)

        self.status_label = Label(text='Status: Idle', font_size=20, color=(1, 1, 1, 1))  # White Text
        self.add_widget(self.status_label)

    def update_rect(self, *args):
        """Updates background when window resizes."""
        self.rect.size = self.size
        self.rect.pos = self.pos

    def set_selected_shape(self, instance):
        """Stores selected churro shape."""
        self.selected_shape = instance.text

    def start_churro_making(self, instance):
        """Updates status label when making a churro."""
        phone = self.phone_input.text.strip()
        provider = self.provider_input.text.strip()
        email = self.email_input.text.strip()

        message = "A new churro drawing has been submitted!"

        if email:
            recipient = send_to(email=email)
        elif phone and provider:
            if len(phone) != 10 or not phone.isdigit():
                self.status_label.text = "Error: Phone number must be 10 digits."
                return
            if provider not in phone_providers:
                self.status_label.text = "Error: Invalid carrier name."
                return
            recipient = send_to(number=phone, provider=provider)
        else:
            self.status_label.text = "Error: Provide phone+carrier OR an email."
            return
        self.status_label.text = "Your churro is being made..."

        try:
            email_alert("Churro Drawing Submitted!", message, recipient)
            self.status_label.text = "Success! Notification sent."

            # Clear input fields and drawing
            self.phone_input.text = ""
            self.provider_input.text = ""
            self.email_input.text = ""
            self.draw_input.clear_canvas()
        except Exception as e:
            print("Email failed:", e)
            self.status_label.text = "Error: Failed to send notification."

        self.status_label.text = f'Your {self.selected_shape} churro is being made...'


class ChurroMakerApp(App):
    def build(self):
        return ChurroControlScreen()


if __name__ == '__main__':
    ChurroMakerApp().run()
