from base_level import BaseLevel

class LevelOne(BaseLevel):
    def __init__(self):
        super().__init__(level_num=1, lvl_speed=7, bg_speed=3, finish_line=22000)
        