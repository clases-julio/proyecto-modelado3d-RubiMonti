import bpy
from bpy import data as D
from bpy import context 
from mathutils import *
from math import *

'''*********************************************************************'''
'''Funciones comunes útiles para selección/activación/borrado de objetos'''
'''*********************************************************************'''
def seleccionarObjetos(nombresObjetos): # Seleccionar un objeto por su nombre
    bpy.ops.object.select_all(action='DESELECT') # deseleccionamos todos...
    for obj in nombresObjetos:
        bpy.ops.object.select_pattern(pattern=obj,case_sensitive=True,extend=True) # ...excepto el buscado

def activarObjeto(nombreObjeto): # Activar un objeto por su nombre
    bpy.context.scene.objects.active = bpy.data.objects[nombreObjeto]

def borrarObjeto(nombreObjeto): # Borrar un objeto por su nombre
    seleccionarObjeto(nombreObjeto)
    bpy.ops.object.delete(use_global=False)

def borrarObjetos(): # Borrar todos los objetos
    if(len(bpy.data.objects) != 0):
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete(use_global=False)

'''****************************************************************'''
'''Clase para realizar transformaciones sobre objetos seleccionados'''
'''****************************************************************'''
class Seleccionado:
    def mover(v):
        bpy.ops.transform.translate(
            value=v, constraint_axis=(True, True, True))

    def escalar(v):
        bpy.ops.transform.resize(value=v, constraint_axis=(True, True, True))

    def rotarX(v):
        bpy.ops.transform.rotate(value=v, orient_axis='X')

    def rotarY(v):
        bpy.ops.transform.rotate(value=v, orient_axis='Y')

    def rotarZ(v):
        bpy.ops.transform.rotate(value=v, orient_axis='Z')
        
    def unir(new_name):
        bpy.ops.object.join()
        Activo.renombrar(new_name)

'''**********************************************************'''
'''Clase para realizar transformaciones sobre objetos activos'''
'''**********************************************************'''
class Activo:
    def posicionar(v):
        bpy.context.object.location = v

    def escalar(v):
        bpy.context.object.scale = v

    def rotar(v):
        bpy.context.object.rotation_euler = v

    def renombrar(nombreObjeto):
        bpy.context.object.name = nombreObjeto

'''**************************************************************'''
'''Clase para realizar transformaciones sobre objetos específicos'''
'''**************************************************************'''
class Especifico:
    def escalar(nombreObjeto, v):
        bpy.data.objects[nombreObjeto].scale = v

    def posicionar(nombreObjeto, v):
        bpy.data.objects[nombreObjeto].location = v

    def rotar(nombreObjeto, v):
        bpy.data.objects[nombreObjeto].rotation_euler = v

'''************************'''
'''Clase para crear objetos'''
'''************************'''
class Objeto:
    def crearCubo(objName):
        bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0))
        Activo.renombrar(objName)

    def crearEsfera(objName):
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.5, location=(0, 0, 0))
        Activo.renombrar(objName)

    def crearCono(objName):
        bpy.ops.mesh.primitive_cone_add(radius1=0.5, location=(0, 0, 0))
        Activo.renombrar(objName)
    
    def crearCilindro(objName, r=1, h=2):
        bpy.ops.mesh.primitive_cylinder_add(vertices=50, radius=r, depth=h, enter_editmode=False, location=(0, 0, 0))
        Activo.renombrar(objName)
    
    def crearHexagono(objName, h=2):
        bpy.ops.mesh.primitive_cylinder_add(vertices=6, depth=h, enter_editmode=False, location=(0, 0, 0))
        Activo.renombrar(objName)
        
    def crearCamara(objName):
        # Creamos las lentes:
        Objeto.crearCono("Lens1")
        Seleccionado.escalar((0.15, 0.15, 0.02))
        Seleccionado.mover((0, 0.09, 0))
        Seleccionado.rotarX(1.57)
        Seleccionado.rotarZ(3.14)
        Objeto.crearCono("Lens2")
        Seleccionado.escalar((0.15, 0.15, 0.02))
        Seleccionado.mover((-0.15, 0.09, 0))
        Seleccionado.rotarX(1.57)
        Seleccionado.rotarZ(3.14)
        Objeto.crearCono("Lens3")
        Seleccionado.escalar((0.15, 0.15, 0.02))
        Seleccionado.mover((0.3, 0.09, 0))
        Seleccionado.rotarX(1.57)
        Seleccionado.rotarZ(3.14)
        
        # Creamos el cuerpo de la camara y le restamos las lentes para obtener los agujeros de las mismas 
        Objeto.crearCubo(objName)
        Seleccionado.escalar((1.2, 0.2, 0.2))
        seleccion = ['Lens1','Lens3','Lens2', objName]
        seleccionarObjetos(seleccion)
        bpy.ops.object.modifier_apply(modifier="Auto Boolean")
        bpy.ops.object.booltool_auto_difference()
        
        # Creamos el soporte de la camara y lo unimos con lo que hemos obtenido arriba
        Objeto.crearCilindro('CameraSupport', 0.08, 0.1)
        Seleccionado.escalar((2, 1, 1))
        Seleccionado.mover((0.0, 0, -0.15))
        seleccion = ['Camara','CameraSupport']
        seleccionarObjetos(seleccion)
        Seleccionado.unir('Camera')
    
    def crearLaser(objName):
        # Crearemos la parte interior del laser sobre la que gira el dispositivo
        Objeto.crearCilindro('R_Laser_Support', 0.4, 2)
        Seleccionado.mover((0, 0, -0.2))
        Objeto.crearCono("Laser_Support")
        Seleccionado.escalar((0.3, 0.3, 1))
        Seleccionado.rotarX(3.14)
        
        # Restaremos las dos piezas creadas para obtener un cono truncado donde se apoyara la semiesfera
        seleccion = ['Laser_Support','R_Laser_Support']
        seleccionarObjetos(seleccion)
        bpy.ops.object.modifier_apply(modifier="Auto Boolean")
        bpy.ops.object.booltool_auto_difference()
        
        # Crearemos la base del laser igual que el punto de apoyo
        Objeto.crearCilindro('R_LaserBody', 0.5, 2)
        Seleccionado.mover((0, 0, -0.15))
        Objeto.crearCono("LaserBody")
        Seleccionado.escalar((0.5, 0.5, 1))
        Seleccionado.rotarX(3.14)
        seleccion = ['LaserBody','R_LaserBody']
        seleccionarObjetos(seleccion)
        bpy.ops.object.modifier_apply(modifier="Auto Boolean")
        bpy.ops.object.booltool_auto_difference()
        
        # Creamos ahora la semiesfera que sera la que gire sobre el soporte y la base
        Objeto.crearCilindro('R_Rotatory', 0.5, 0.4)
        Seleccionado.mover((0, 0, 0.2))
        Objeto.crearEsfera('Rotatory')
        Seleccionado.escalar((0.4, 0.4, 0.4))
        seleccion = ['Rotatory','R_Rotatory']
        seleccionarObjetos(seleccion)
        bpy.ops.object.modifier_apply(modifier="Auto Boolean")
        bpy.ops.object.booltool_auto_difference()
        Seleccionado.mover((0,0,0.82))
        seleccion = ['LaserBody','Laser_Support','Rotatory']
        seleccionarObjetos(seleccion)
        Seleccionado.unir(objName)
        
'''************'''
''' M  A  I  N '''
'''************'''
if __name__ == "__main__":
    # Empezamos eliminando todos los objetos que hay en la escena.
    borrarObjetos()

    # Añadimos la luz ambiente y todas las luces que sean necesarias para una buena visualización    
    bpy.ops.object.light_add(type='SUN', radius=1, location=(0, 0, 0))
    
    # Creamos las ruedas del robot y los agujeros en la base que las contengan:
    Objeto.crearCilindro('Wheel1', 0.07, 0.07)
    Seleccionado.rotarY(1.57)
    Seleccionado.mover((0, 0.8, 0))
    Objeto.crearCilindro('H_Wheel1', 0.075, 0.075)
    Seleccionado.rotarY(1.57)
    Seleccionado.mover((0, 0.8, 0))
    Objeto.crearCilindro('Wheel2', 0.07, 0.07)
    Seleccionado.rotarY(1.57)
    Seleccionado.mover((0, -0.8, 0))
    Objeto.crearCilindro('H_Wheel2', 0.075, 0.075)
    Seleccionado.rotarY(1.57)
    Seleccionado.mover((0, -0.8, 0))
    Objeto.crearCilindro('Wheel3', 0.18, 0.1)
    Seleccionado.rotarY(1.57)
    Seleccionado.mover((0.7, 0, 0))
    Objeto.crearCilindro('H_Wheel3', 0.2, 0.12)
    Seleccionado.rotarY(1.57)
    Seleccionado.mover((0.7, 0, 0))
    Objeto.crearCilindro('Wheel4', 0.18, 0.1)
    Seleccionado.rotarY(1.57)
    Seleccionado.mover((-0.7, -0, 0))
    Objeto.crearCilindro('H_Wheel4', 0.2, 0.12)
    Seleccionado.rotarY(1.57)
    Seleccionado.mover((-0.7, -0, 0))
    
    # Creación de la base del robot y le aplicamos la resta de los agujeros de las ruedas:
    Objeto.crearCilindro('BaseBody', 1, 0.5)
    Seleccionado.mover((0, 0, 0.25))
    seleccion = ['H_Wheel1','H_Wheel2','H_Wheel3','H_Wheel4','BaseBody']
    seleccionarObjetos(seleccion)
    bpy.ops.object.modifier_apply(modifier="Auto Boolean")
    bpy.ops.object.booltool_auto_difference()
    
    # Creamos todos los botones y agujeros del panel
    Objeto.crearCubo("Conector1")
    Seleccionado.escalar((0.03, 0.05, 0.03))
    Seleccionado.mover((0.25, 0.25, 0.17))
    Objeto.crearCubo("USB1")
    Seleccionado.escalar((0.025, 0.05, 0.03))
    Seleccionado.mover((0.18, 0.25, 0.17))
    Objeto.crearCubo("Conector2")
    Seleccionado.escalar((0.25, 0.05, 0.03))
    Seleccionado.mover((0, 0.25, 0.17))
    Objeto.crearCubo("Conector3")
    Seleccionado.escalar((0.03, 0.05, 0.03))
    Seleccionado.mover((-0.25, 0.25, 0.17))
    Objeto.crearCubo("USB2")
    Seleccionado.escalar((0.025, 0.05, 0.03))
    Seleccionado.mover((-0.18, 0.25, 0.17))
    Objeto.crearCubo("Conector4")
    Seleccionado.escalar((0.01, 0.05, 0.025))
    Seleccionado.mover((-0.28, 0.25, 0.17))
    Objeto.crearCubo("Conector5")
    Seleccionado.escalar((0.04, 0.05, 0.03))
    Seleccionado.mover((0.1, 0.25, 0.13))
    Objeto.crearCilindro('Boton1', 0.02, 0.02)
    Seleccionado.rotarX(1.57)
    Seleccionado.mover((-0.15, 0.25, 0.13))
    Objeto.crearCilindro('Boton2', 0.02, 0.02)
    Seleccionado.rotarX(1.57)
    Seleccionado.mover((-0.20, 0.25, 0.13))
    Objeto.crearCilindro('Boton3', 0.02, 0.02)
    Seleccionado.rotarX(1.57)
    Seleccionado.mover((-0.25, 0.25, 0.13))
    
    # Creamos los leds con esferas para unirlas al panel
    Objeto.crearEsfera('Led1')
    Seleccionado.escalar((0.01, 0.02, 0.01))
    Seleccionado.mover((0.25, 0.25, 0.13))
    Objeto.crearEsfera('Led2')
    Seleccionado.escalar((0.01, 0.02, 0.01))
    Seleccionado.mover((0.21, 0.25, 0.13))
    Objeto.crearEsfera('Led3')
    Seleccionado.escalar((0.01, 0.02, 0.01))
    Seleccionado.mover((0.17, 0.25, 0.13))
    
    # Creamos lo que dara forma al panel y restamos todos los conectores y botones
    Objeto.crearCilindro('R_Panel', 0.95, 0.5)
    Seleccionado.mover((0, 0, 0.35))
    Objeto.crearCubo("Panel")
    Seleccionado.escalar((2, 0.5, 0.5))
    seleccion = ['Conector1','Conector2','USB1','Conector3','USB2','Conector4','Conector5','Boton1','Boton2','Boton3','Panel']
    seleccionarObjetos(seleccion)
    bpy.ops.object.modifier_apply(modifier="Auto Boolean")
    bpy.ops.object.booltool_auto_difference()
    
    seleccion = ['Panel','Led1','Led2','Led3']
    seleccionarObjetos(seleccion)
    Seleccionado.unir('Panel')
    
    # Lo rotamos y tras darle forma lo unimos a la base del robot
    Seleccionado.rotarX(-0.5)
    Seleccionado.mover((0, 0.72, 0.3))
    
    seleccion = ['R_Panel','Panel']
    seleccionarObjetos(seleccion)
    bpy.ops.object.modifier_apply(modifier="Auto Boolean")
    bpy.ops.object.booltool_auto_intersect()
    
    seleccion = ['Panel','BaseBody']
    seleccionarObjetos(seleccion)
    Seleccionado.unir('BaseBody')
    
    # Creación de la primera base del robot
    Objeto.crearCilindro('ShortSupport1', 0.05, 0.2)
    Seleccionado.mover((0.8, 0.3, 0))
    Objeto.crearCilindro('ShortSupport2', 0.05, 0.2)
    Seleccionado.mover((-0.8, 0.3, 0))
    Objeto.crearCilindro('ShortSupport3', 0.05, 0.2)
    Seleccionado.mover((0.8, -0.3, 0))
    Objeto.crearCilindro('ShortSupport4', 0.05, 0.2)
    Seleccionado.mover((-0.8, -0.3, 0))
    Objeto.crearCubo("R_Base1")
    Seleccionado.escalar((2, 0.5, 0.5))
    Seleccionado.mover((0, 0.9, 0.1))
    Objeto.crearHexagono('Base1', 0.1)
    Seleccionado.mover((0, 0, 0.1))
    seleccion = ['R_Base1','Base1']
    seleccionarObjetos(seleccion)
    bpy.ops.object.modifier_apply(modifier="Auto Boolean")
    bpy.ops.object.booltool_auto_difference()
    seleccion = ['ShortSupport1','ShortSupport2','ShortSupport3','ShortSupport4','Base1']
    seleccionarObjetos(seleccion)
    Seleccionado.unir('LowerBase1')
    Seleccionado.mover((0, 0, 0.6))
    
    # Creación de la segunda base del robot en la que se encontrarán la cámara y el laser
    Objeto.crearCilindro('ShortSupport1', 0.05, 0.4)
    Seleccionado.mover((0.8, 0.3, 0))
    Objeto.crearCilindro('ShortSupport2', 0.05, 0.4)
    Seleccionado.mover((-0.8, 0.3, 0))
    Objeto.crearCilindro('ShortSupport3', 0.05, 0.4)
    Seleccionado.mover((0.8, -0.3, 0))
    Objeto.crearCilindro('ShortSupport4', 0.05, 0.4)
    Seleccionado.mover((-0.8, -0.3, 0))
    Objeto.crearHexagono('Base2', 0.1)
    Seleccionado.mover((0, 0, 0.2))
    seleccion = ['ShortSupport1','ShortSupport2','ShortSupport3','ShortSupport4','Base2']
    seleccionarObjetos(seleccion)
    Seleccionado.unir('LowerBase2')
    Seleccionado.mover((0, 0, 0.95))
    

    # Creación de la segunda base que servirá de apoyo al ordenador del usuario
    Objeto.crearCilindro('LongSupport1', 0.05, 1)
    Seleccionado.mover((0.8, 0.3, 0))
    Objeto.crearCilindro('LongSupport2', 0.05, 1)
    Seleccionado.mover((-0.8, 0.3, 0))
    Objeto.crearCilindro('LongSupport3', 0.05, 1)
    Seleccionado.mover((0.8, -0.3, 0))
    Objeto.crearCilindro('LongSupport4', 0.05, 1)
    Seleccionado.mover((-0.8, -0.3, 0))
    Objeto.crearHexagono('Base3', 0.1)
    Seleccionado.mover((0, 0, 0.5))
    seleccion = ['LongSupport1','LongSupport2','LongSupport3','LongSupport4','Base3']
    seleccionarObjetos(seleccion)
    Seleccionado.unir('UpperBase')
    Seleccionado.mover((0, 0, 1.7))
    
    # Unimos todas las piezas del robot que llevamos hasta ahora. Estas formarn la estructura del robot
    seleccion = ['BaseBody','LowerBase1','LowerBase2','UpperBase']
    seleccionarObjetos(seleccion)
    Seleccionado.unir('Body')
    
    # Creación de la cámara y el sensor láser
    Objeto.crearCamara('Camara')
    Seleccionado.mover((0, 0.5, 1.4))
    
    Objeto.crearLaser('Laser')
    Seleccionado.mover((0,0,1.2))
