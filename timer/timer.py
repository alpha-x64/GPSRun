from kivy.app import App
from kivy.uix.label import Label
from kivy.animation import Animation
from kivy.properties import StringProperty, NumericProperty


class Countdown(Label):
    seconds = NumericProperty(60)  # seconds

    def start(self):
        Animation.cancel_all(self)  # stop any current animations
        self.anim = Animation(seconds=0, duration=self.seconds)
        def finish_callback(animation, incr_crude_clock):
            incr_crude_clock.text = "FINISHED"
        self.anim.bind(on_complete=finish_callback)
        self.anim.start(self)

class TimerApp(App):
    def build(self):
        countdown = Countdown()
        countdown.start()
        return countdown

if __name__ == "__main__":
    TimerApp().run()