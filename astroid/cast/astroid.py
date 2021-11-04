from genie.cast.actor import Actor

class Astroid(Actor):
    def __init__(self, path: str,
                width: int = 0, 
                height: int = 0, 
                
                x: float = 0, 
                y: float = 0, 
                
                vx: float = 0, 
                vy: float = 0, 
                
                rotation: float = 0, 
                rotation_vel: float = 0,
                
                points: int = 0,
                max_hp: int = 0):

        super().__init__(path, 
                        width=width, 
                        height=height, 
                        
                        x=x, 
                        y=y, 
                        
                        vx=vx, 
                        vy=vy, 
                        
                        rotation=rotation, 
                        rotation_vel=rotation_vel)
        self._points = points
        self._max_hp = max_hp
        self._current_hp = max_hp

    def set_points(self, points):
        self._points = points
    
    def get_point(self):
        return self._points

    def set_hp(self, hp):
        self._current_hp = hp
    
    def get_hp(self):
        return self._current_hp
    
    def set_max_hp(self, hp):
        self._max_hp = hp
    
    def get_max_hp(self):
        return self._max_hp
    
    def get_hp_percent(self):
        return self._current_hp / self._max_hp

    def take_damage(self, damage):
        self._current_hp -= damage