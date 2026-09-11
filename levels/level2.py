from base_level import BaseLevel

class LevelTwo(BaseLevel):
    def __init__(self):
        super().__init__(level_num=2, lvl_speed=9, bg_speed=4, finish_line=33600)
