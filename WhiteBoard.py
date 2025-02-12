from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.widget import Widget
from kivy.graphics import Color, Line, Rectangle


class DrawInput(Widget):
    """Whiteboard for drawing custom churro shapes."""

    def on_touch_down(self, touch):
        with self.canvas:
            Color(1, 0, 0, 1)  # Red color
            touch.ud["line"] = Line(points=(touch.x, touch.y))  # Start drawing

    def on_touch_move(self, touch):
        touch.ud["line"].points += (touch.x, touch.y)  # Continue drawing

    def clear_canvas(self):
        """Clears the drawing board."""
        self.canvas.clear()


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
        self.draw_input = DrawInput()
        self.add_widget(self.draw_input)

        self.clear_button = Button(text="Clear Drawing", size_hint=(1, 0.2), background_color=(1, 0.3, 0.3, 1))  # Red
        self.clear_button.bind(on_press=lambda instance: self.draw_input.clear_canvas())
        self.add_widget(self.clear_button)

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
        self.status_label.text = f'Your {self.selected_shape} churro is being made...'


class ChurroMakerApp(App):
    def build(self):
        return ChurroControlScreen()


if __name__ == '__main__':
    ChurroMakerApp().run()
