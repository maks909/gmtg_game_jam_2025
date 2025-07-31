import arcade
from arcade.gui import (
    UIManager,
    UITextureButton,
    UIAnchorLayout,
    UIView,
    UIBoxLayout
)
import sys
import os

if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    os.chdir(sys._MEIPASS)

TEX_RED_BUTTON_NORMAL = arcade.load_texture(":resources:gui_basic_assets/button/red_normal.png")
TEX_RED_BUTTON_HOVER = arcade.load_texture(":resources:gui_basic_assets/button/red_hover.png")
TEX_RED_BUTTON_PRESS = arcade.load_texture(":resources:gui_basic_assets/button/red_press.png")

class StartGUIView(arcade.View):
    def __init__(self):
        super().__init__(background_color=arcade.color.GRAY_ASPARAGUS)
        
        self.ui = UIManager()

        anchor = self.ui.add(UIAnchorLayout())

        button = anchor.add(
            UITextureButton(
                text="Play",
                texture=TEX_RED_BUTTON_NORMAL,
                texture_hovered=TEX_RED_BUTTON_HOVER,
                texture_pressed=TEX_RED_BUTTON_PRESS,
            )
        )
        # add a button to switch to the blue view
        @button.event("on_click")
        def on_click(event):
            self.window.show_view(PlatformerView())

    def on_show_view(self) -> None:
        self.ui.enable()

    def on_hide_view(self) -> None:
        self.ui.disable()

    def on_draw(self):
        # Clear the screen
        self.clear(color=arcade.uicolor.GREEN_EMERALD)

        # Add draw commands that should be below the UI
        # ...

        self.ui.draw()

        # Add draw commands that should be on top of the UI (uncommon)
        # ...



class PauseGUIView(arcade.View):
    def __init__(self):
        super().__init__(background_color=arcade.color.GRAY_ASPARAGUS)

        self.ui = UIManager()

        anchor = self.ui.add(UIAnchorLayout())
        
        box = anchor.add(
            UIBoxLayout(
                vertical=True,
                space_between=20,  # space between buttons in pixels
                align="center"
            )
        )

        resume_button = box.add(
            UITextureButton(
                text="Resume",
                texture=TEX_RED_BUTTON_NORMAL,
                texture_hovered=TEX_RED_BUTTON_HOVER,
                texture_pressed=TEX_RED_BUTTON_PRESS,
            )
        )
        exit_button = box.add(
            UITextureButton(
                text="Exit Game",
                texture=TEX_RED_BUTTON_NORMAL,
                texture_hovered=TEX_RED_BUTTON_HOVER,
                texture_pressed=TEX_RED_BUTTON_PRESS,
            )
        )

        # add a button to resume
        @resume_button.event("on_click")
        def on_click(event):
            self.window.show_view(PlatformerView())

        @exit_button.event("on_click")
        def on_click(event):
            arcade.exit()

    def on_show_view(self) -> None:
        self.ui.enable()

    def on_hide_view(self) -> None:
        self.ui.disable()

    def on_draw(self):
        # Clear the screen
        self.clear(color=arcade.uicolor.GREEN_EMERALD)

        # Add draw commands that should be below the UI
        # ...

        self.ui.draw()

        # Add draw commands that should be on top of the UI (uncommon)

class MathView(arcade.View):
    pass

class PlatformerView(arcade.View):
    def __init__(self):
        super().__init__(background_color=arcade.color.GRAY_ASPARAGUS)
    
    def on_draw(self):
        self.clear()
    
    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            self.window.show_view(PauseGUIView())

class Player(arcade.TextureAnimationSprite):
    pass

def main():
    """ Main function """
    # Create a window class. This is what actually shows up on screen
    screen = arcade.get_display_size()
    window = arcade.Window(title="The Learning Loop")
    window.set_size(screen[0], screen[1])
    window.set_fullscreen()

    # Show the view on screen
    window.show_view(StartGUIView())

    # Start the arcade game loop
    arcade.run()

main()