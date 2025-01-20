class ConveyorBelt:
    def __init__(self, env):
        self.env = env
        self.running = False
        self.speed = 1.0

    def start(self):
        self.running = True
        return "Conveyor belt started"

    def stop(self):
        self.running = False
        return "Conveyor belt stopped"

    def adjust_speed(self, speed):
        self.speed = speed
        return f"Conveyor belt speed adjusted to {speed}"