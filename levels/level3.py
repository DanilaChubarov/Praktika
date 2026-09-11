from base_level import BaseLevel

class LevelThree(BaseLevel):
    def __init__(self):
        super().__init__(level_num=3, lvl_speed=11, bg_speed=5, finish_line=25000)
