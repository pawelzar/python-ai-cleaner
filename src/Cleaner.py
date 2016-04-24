import Object


class Cleaner(Object):
    def can_move_under(self, furniture):
        return furniture.height_from_floor < self.height
