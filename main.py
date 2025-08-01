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

TEX_RED_BUTTON_NORMAL = arcade.load_texture("images/button/normal.png")
TEX_RED_BUTTON_HOVER = arcade.load_texture("images/button/hovered.png")
TEX_RED_BUTTON_PRESS = arcade.load_texture("images/button/pressed.png")

class StartGUIView(arcade.View):
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

        play_button = box.add(
            UITextureButton(
                text="Play",
                texture=TEX_RED_BUTTON_NORMAL,
                texture_hovered=TEX_RED_BUTTON_HOVER,
                texture_pressed=TEX_RED_BUTTON_PRESS,
                scale=0.2
            )
        )
        exit_button = box.add(
            UITextureButton(
                text="Exit Game",
                texture=TEX_RED_BUTTON_NORMAL,
                texture_hovered=TEX_RED_BUTTON_HOVER,
                texture_pressed=TEX_RED_BUTTON_PRESS,
                scale=0.2
            )
        )
        # add a button to start th game
        @play_button.event("on_click")
        def on_click(event):
            self.window.show_view(StartCutSceneView())

        # add a button to switch to exit the game
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

class PauseGUIView(arcade.View):
    def __init__(self, backview):
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
                scale=0.2
            )
        )
        exit_button = box.add(
            UITextureButton(
                text="Exit Game",
                texture=TEX_RED_BUTTON_NORMAL,
                texture_hovered=TEX_RED_BUTTON_HOVER,
                texture_pressed=TEX_RED_BUTTON_PRESS,
                scale=0.2
            )
        )

        # add a button to resume
        @resume_button.event("on_click")
        def on_click(event):
            self.window.show_view(backview)

        # add butoon to exit
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

def create_animation(path, image_name, frame_count, frame_duration, number = True):
        textures = []
        for i in range(1, frame_count+1):
            if number:    
                filename = f"{path}{image_name}{i}.png"
            else:
                filename = f"{path}{image_name}.png"
            textures.append(arcade.load_texture(filename))
        frames = []
        for texture in textures:
            frames.append(arcade.TextureKeyframe(texture, duration=frame_duration))
        return arcade.TextureAnimation(frames)
class Player(arcade.TextureAnimationSprite):
    def __init__(self):
        super().__init__(center_x=300, center_y=300)

        self.center_x=300
        self.center_y=300
        self.scale=5
        
        self.run_left_animation = create_animation("images/player/", "run_left", 4, 80)
        self.run_right_animation = create_animation("images/player/", "run_right", 4, 80)

        self.stand_left_animation = create_animation("images/player/", "run_left", 1, 80)
        self.stand_right_animation = create_animation("images/player/", "run_right", 1, 80)

        self.animation = self.stand_left_animation

class Boss(arcade.TextureAnimationSprite):
    def __init__(self, behavior_type: str):
        super().__init__()

        self.injured_animation = create_animation("images/boss/", "injured", 2, 500)
        self.sleeping_animation = create_animation("images/boss/", "sleeping", 7, 500)
        self.angry_animation = create_animation("images/boss/", "angry", 2, 500)
        self.normal_animation = create_animation("images/boss/", "normal", 1, 500, False)
        self.dead_animation = create_animation("images/boss/", "dead", 1, 500, False)
        self.behavior_type = behavior_type
        if self.behavior_type == "hovering":
            self.center_x=arcade.get_display_size()[0]/2
            self.y_direction = 1
            self.center_y = 800
            self.animation=self.sleeping_animation
            self.scale = 20

    def update(self, delta_time: float):
        super().update() # The base Sprite.update doesn't need delta_time

        if self.behavior_type == "hovering":
            self.hover(delta_time)
    
    def hover(self, delta_time: float):
        if self.center_y <= 680:
            self.y_direction = 1
        elif self.center_y >=730:
            self.y_direction = -1
        self.center_y += self.y_direction*delta_time*30


class StartCutSceneView(arcade.View):
    def __init__(self):
        super().__init__(background_color=arcade.color.GRAY_ASPARAGUS)
        self.sprite_list = arcade.SpriteList()
        self.sprite_list.append(Boss("hovering"))

        self.display_size = arcade.get_display_size()

        self.dialogue = ["Hello, adventurer! I'm glad you stopped by.",
            "This village is in peril. A fearsome dragon has been spotted in the mountains.",
            "Will you be the hero we need?",
            "Please, find the dragon and save us all!"]
        self.current_line_index = 0
        
        self.dialogue_box = arcade.shape_list.create_rectangle_filled(
            center_x=self.display_size[0] / 2,
            center_y=100,
            width=self.display_size[0] - 40,
            height=150,
            color=(0, 0, 0, 180) # Black with transparency
        )
    def on_draw(self):
        """Draw the dialogue box and the current line of text."""
        self.clear()
        self.sprite_list.draw(pixelated=True)
        # Now, draw the dialogue box on top
        self.dialogue_box.draw()

        current_line = self.dialogue[self.current_line_index]
        arcade.draw_text(
            current_line,
            x=40,
            y=150,
            color=arcade.color.WHITE,
            font_size=18,
            width=self.display_size[0] - 80,
            multiline=True, 
        )

    def on_update(self, delta_time):
        self.sprite_list.update(delta_time)
        self.sprite_list.update_animation(delta_time)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            self.window.show_view(PauseGUIView(self))
        if key == arcade.key.ENTER:
            self.current_line_index += 1

class PlatformerView(arcade.View):
    def __init__(self):
        super().__init__(background_color=arcade.color.GRAY_ASPARAGUS)
        self.sprite_list = arcade.SpriteList()
        self.player = Player()
        self.sprite_list.append(self.player)
        self.physics_engine = arcade.PhysicsEngineSimple(self.player)
        self.sprite_list.append(Boss("show-right"))

    def on_draw(self):
        self.clear()
        self.sprite_list.draw(pixelated=True)
    
    def on_update(self, delta_time):
        # Pass delta_time to the sprite list's update method
        self.sprite_list.update(delta_time)
        
        # The update_animation method also benefits from delta_time
        self.sprite_list.update_animation(delta_time)
        self.physics_engine.update()
    
    def on_key_press(self, key, modifiers):
        if key == arcade.key.LEFT:
            self.player.animation = self.player.run_left_animation
            self.player.change_x = -10
        elif key == arcade.key.RIGHT:
            self.player.animation = self.player.run_right_animation
            self.player.change_x = 10
        elif key == arcade.key.ESCAPE:
            self.window.show_view(PauseGUIView(PlatformerView()))
    
    def on_key_release(self, key, modifiers):
        if key == arcade.key.LEFT:
            self.player.change_x = 0
            self.player.animation = self.player.stand_left_animation
        elif key == arcade.key.RIGHT:
            self.player.change_x = 0
            self.player.animation = self.player.stand_right_animation
    
    def on_show_view(self) -> None:
        pass

    def on_hide_view(self) -> None:
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