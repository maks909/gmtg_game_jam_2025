from panda3d.core import *
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.actor.Actor import Actor
from panda3d.core import KeyboardButton

class PongGame(ShowBase):
    def __init__(self):
        super().__init__()

        self.disableMouse()

        # Set up the camera
        self.camera.setPos(0, -20, 0)
        self.camera.lookAt(0, 0, 0)

        # Create left paddle
        self.left_paddle = self.loader.loadModel("models/box")
        self.left_paddle.setScale(0.2, 0.2, 1.5)
        self.left_paddle.setPos(-6, 0, 0)
        self.left_paddle.reparentTo(self.render)

        # Create right paddle
        self.right_paddle = self.loader.loadModel("models/box")
        self.right_paddle.setScale(0.2, 0.2, 1.5)
        self.right_paddle.setPos(6, 0, 0)
        self.right_paddle.reparentTo(self.render)

        # Create ball
        self.ball = self.loader.loadModel("models/smiley")
        self.ball.setScale(0.4)
        self.ball.setPos(0, 0, 0)
        self.ball.reparentTo(self.render)

        self.ball_velocity = [0.1, 0.1]

        # Movement states
        self.keys = {"w": False, "s": False, "arrow_up": False, "arrow_down": False}

        self.accept("w", self.set_key, ["w", True])
        self.accept("w-up", self.set_key, ["w", False])
        self.accept("s", self.set_key, ["s", True])
        self.accept("s-up", self.set_key, ["s", False])
        self.accept("arrow_up", self.set_key, ["arrow_up", True])
        self.accept("arrow_up-up", self.set_key, ["arrow_up", False])
        self.accept("arrow_down", self.set_key, ["arrow_down", True])
        self.accept("arrow_down-up", self.set_key, ["arrow_down", False])

        # Add update task
        self.taskMgr.add(self.update, "update")

    def set_key(self, key, value):
        self.keys[key] = value

    def update(self, task):
        # Move paddles
        if self.keys["w"]:
            self.left_paddle.setZ(self.left_paddle.getZ() + 0.2)
        if self.keys["s"]:
            self.left_paddle.setZ(self.left_paddle.getZ() - 0.2)
        if self.keys["arrow_up"]:
            self.right_paddle.setZ(self.right_paddle.getZ() + 0.2)
        if self.keys["arrow_down"]:
            self.right_paddle.setZ(self.right_paddle.getZ() - 0.2)

        # Move ball
        pos = self.ball.getPos()
        vx, vz = self.ball_velocity
        new_x = pos.getX() + vx
        new_z = pos.getZ() + vz
        self.ball.setPos(new_x, 0, new_z)

        # Bounce off top and bottom walls
        if new_z > 4.5 or new_z < -4.5:
            self.ball_velocity[1] *= -1

        # Bounce off paddles
        if self.check_collision(self.ball, self.left_paddle) and vx < 0:
            self.ball_velocity[0] *= -1
        if self.check_collision(self.ball, self.right_paddle) and vx > 0:
            self.ball_velocity[0] *= -1

        # Reset if ball goes off screen
        if abs(new_x) > 8:
            self.ball.setPos(0, 0, 0)
            self.ball_velocity = [0.1, 0.1]

        return Task.cont

    def check_collision(self, ball, paddle):
        ball_pos = ball.getPos()
        paddle_pos = paddle.getPos()
        return (
            abs(ball_pos.getX() - paddle_pos.getX()) < 0.5 and
            abs(ball_pos.getZ() - paddle_pos.getZ()) < 1.5
        )

game = PongGame()
game.run()
