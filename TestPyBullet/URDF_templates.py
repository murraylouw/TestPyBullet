from re import X


class Origin:
    def __init__(self, x, y, z, eulerX, eulerY, eulerZ):
        self.x = x
        self.y = y
        self.z = z
        self.eulerX = eulerX
        self.eulerY = eulerY
        self.eulerZ = eulerZ  
        
    def ToString():
        string = '<origin xyz="{} {} {}" rpy="{} {} {}"/>'.format(x, self.y , self.z , self.eulerX , self.eulerY , self.eulerZ )
        return string         

class Visual:
    def __init__(self, origin, mesh):
        self.origin = origin
        self.mesh = mesh
        
class Inertial:
    def __init__(self, mass):
        self.mass = mass
        
class Link:
    def __init__(self, inertial, visual, collision):
        self.inertial = inertial
        self.visual = visual
        self.collision = collision 
        
    def ToString():
        return "Link"    