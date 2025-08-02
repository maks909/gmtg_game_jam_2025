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

import random

if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    os.chdir(sys._MEIPASS)

TEX_RED_BUTTON_NORMAL = arcade.load_texture("images/button/normal.png")
TEX_RED_BUTTON_HOVER = arcade.load_texture("images/button/hovered.png")
TEX_RED_BUTTON_PRESS = arcade.load_texture("images/button/pressed.png")

try:
    arcade.load_font("fonts/8bitoperator.ttf")  # Replace with your pixel font filename
    PIXEL_FONT_NAME = "8bitoperator"
except:
    PIXEL_FONT_NAME = "Courier New"  # Fallback to monospace


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
        super().__init__()

        self.center_x=300
        self.center_y=330
        self.scale=5
        
        self.run_left_animation = create_animation("images/player/", "run_left", 4, 80)
        self.run_right_animation = create_animation("images/player/", "run_right", 4, 80)

        self.stand_left_animation = create_animation("images/player/", "run_left", 1, 80)
        self.stand_right_animation = create_animation("images/player/", "run_right", 1, 80)

        self.animation = self.stand_left_animation
        
        self.jump_sound = arcade.load_sound("sounds/jump.mp3")
        self.run_sound = arcade.load_sound("sounds/running.mp3")
        self.run_sound_player = None

    def play_run_sound(self):
        if not self.run_sound_player or not self.run_sound_player.playing:
            self.run_sound_player = self.run_sound.play(volume=0.5, pan=random.randint(-10, 10)/10)

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
        elif self.behavior_type == "angry":
            self.center_x=arcade.get_display_size()[0]/2
            self.y_direction = 1
            self.center_y = 800
            self.animation=self.angry_animation
            self.scale = 20

    def update(self, delta_time: float):
        super().update() # The base Sprite.update doesn't need delta_time

        if self.behavior_type == "hovering" or self.behavior_type == "angry":
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
        super().__init__(background_color=arcade.color.GRAY_ASPARAGUS)
        self.display_size = arcade.get_display_size()
        self.sprite_list = arcade.SpriteList()
        self.player = Player()
        self.player.center_x = 20
        self.player.animation = self.player.run_right_animation
        self.sprite_list.append(self.player)
        self.sprite_list.append(Boss("hovering"))

        self.wall = arcade.Sprite("images/platform/platform.png", 7.5, self.display_size[0]/2, 120)
        self.wall_list = arcade.SpriteList(use_spatial_hash=True)
        self.wall_list.append(self.wall)

        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player, walls=self.wall_list)

        self.jump_count = 0

    def on_draw(self):
        self.clear()
        self.sprite_list.draw(pixelated=True)
        self.wall_list.draw(pixelated=True)
    
    def on_update(self, delta_time):
        self.sprite_list.update(delta_time)
        self.sprite_list.update_animation(delta_time)
        self.player.scale = 6
        self.physics_engine.update() 
        if self.player.center_x <=500:
            self.player.play_run_sound()
            self.player.center_x += 3
        elif self.player.center_x >= 500 and self.player.center_x <= 520 and self.jump_count<4:
            if self.physics_engine.can_jump():
                self.player.change_y = 10
                self.jump_count += 1
                self.player.jump_sound.play()
        else:
            self.window.show_view(StartDialogueView())

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            self.window.show_view(PauseGUIView(self))

class StartDialogueView(arcade.View):
    def __init__(self):
        super().__init__(background_color=arcade.color.GRAY_ASPARAGUS)
        self.sprite_list = arcade.SpriteList()
        self.display_size = arcade.get_display_size()
        self.sprite_list.append(Boss("angry"))
        self.sprite_list.append(Player())
        self.sprite_list.append(arcade.Sprite("images/platform/platform.png", 7.5, self.display_size[0]/2, 120))
        self.sprite_list[1].center_x = 520
        self.sprite_list[1].scale = 6
        self.sprite_list[1].animation = self.sprite_list[1].stand_right_animation

        self.dialogue = ["Uhh, uhh... No one should bother me when I am sleeping!!",
            "Or you will face my full power!!!",
            "I can create a time loop and you will stay here forever...",
            "... Unless you know math well...", 
            "So have fun >:)"]
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
            x=80,
            y=120,
            color=arcade.color.WHITE,
            font_size=18,
            width=self.display_size[0] - 80,
            multiline=True, 
            font_name=PIXEL_FONT_NAME
        )
        arcade.draw_text(
            "Press Enter to continue",
            x=80,
            y=40,
            color=arcade.color.WHITE,
            font_size=18,
            width=self.display_size[0] - 80,
            multiline=True,
            font_name=PIXEL_FONT_NAME
        )


    def on_update(self, delta_time):
        self.sprite_list.update(delta_time)
        self.sprite_list.update_animation(delta_time)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            self.window.show_view(PauseGUIView(self))
        if key == arcade.key.ENTER:
            if self.current_line_index < len(self.dialogue) - 1:
                self.current_line_index += 1
            else:
                self.window.show_view(PlatformerView())

class PlatformerView(arcade.View):
    def __init__(self):
        super().__init__(background_color=arcade.color.GRAY_ASPARAGUS)
        self.sprite_list = arcade.SpriteList()
        self.player = Player()
        self.sprite_list.append(self.player)
        self.display_size = arcade.get_display_size()
        self.wall_list = arcade.SpriteList(use_spatial_hash=True)
        self.wall_list.append(arcade.Sprite("images/platform/platform.png", 7.5, self.display_size[0]/2, 120))
        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player, self.wall_list)
        self.sprite_list.append(Boss("hovering"))

    def on_draw(self):
        self.clear()
        self.sprite_list.draw(pixelated=True)
        self.wall_list.draw(pixelated=True)
    
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
        if key == arcade.key.UP:
            if self.physics_engine.can_jump():
                self.player.change_y = 10
                self.player.jump_sound.play()
    
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