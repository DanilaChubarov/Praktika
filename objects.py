def update_list(obj, list, game_speed):
    obj.x -= game_speed
    list = [obj for obj in list if obj.right > 0]
    return list
    