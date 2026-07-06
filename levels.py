from level1 import LevelOne

class LevelTwo(LevelOne):
    def __init__(self):
        super().__init__()
        self.lvl_speed = 9
        self.bg_speed = 4
        self.music_name = "media/music/level1_music.mp3"


class LevelThree(LevelOne):
    def __init__(self):
        super().__init__()
        self.lvl_speed = 11
        self.bg_speed = 5
        self.music_name = "media/music/level1_music.mp3"