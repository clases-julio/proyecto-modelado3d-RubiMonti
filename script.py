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
        bpy.data.objects[nombreObjeto].scal1.3e = v

    def posicionar(nombreObjeto, v):
        bpy.data.objects[nombreObjeto].location = v

    def rotar(nombreObjeto, v):
        bpy.data.objects[nombreObjeto].rotation_euler = v

'''************************'''
'''Clase para crear objetos'''
'''************************'''
class Objeto:
    def crearCubo(objName):
        bpy.ops.mesh.primitive_cube_add(size=0.5, location=(0, 0, 0))
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
        bpy.ops.object.metaball_add(type='CUBE', enter_editmode=False, location=(0, 0, 0))
        Activo.renombrar(objName)


'''************'''
''' M  A  I  N '''
'''************'''
if __name__ == "__main__":
    # Empezamos eliminando todos los objetos que hay en la escena.
    borrarObjetos()

    # Añadimos la luz ambiente y todas las luces que sean necesarias para una buena visualización    
    bpy.ops.object.light_add(type='SUN', radius=1, location=(0, 0, 0))

    
    # Creación de la base del robot:
    Objeto.crearCilindro('BaseBody', 1, 0.5)
    Seleccionado.mover((0, 0, 0.25))
    
    # Creación de la primera base del robot en la que se encontrarán la cámara y el laser
    Objeto.crearCilindro('ShortSupport1', 0.05, 0.4)
    Seleccionado.mover((0.8, 0.3, 0.5))
    Objeto.crearCilindro('ShortSupport2', 0.05, 0.4)
    Seleccionado.mover((-0.8, 0.3, 0.5))
    Objeto.crearCilindro('ShortSupport3', 0.05, 0.4)
    Seleccionado.mover((0.8, -0.3, 0.5))
    Objeto.crearCilindro('ShortSupport4', 0.05, 0.4)
    Seleccionado.mover((-0.8, -0.3, 0.5))
    Objeto.crearHexagono('Base1', 0.1)
    Seleccionado.mover((0, 0, 0.75))
    
    # Creación de la segunda base que servirá de apoyo al ordenador del usuario
    Objeto.crearCilindro('LongSupport1', 0.05, 1)
    Seleccionado.mover((0.8, 0.3, 1.3))
    Objeto.crearCilindro('LongSupport2', 0.05, 1)
    Seleccionado.mover((-0.8, 0.3, 1.3))
    Objeto.crearCilindro('LongSupport3', 0.05, 1)
    Seleccionado.mover((0.8, -0.3, 1.3))
    Objeto.crearCilindro('LongSupport4', 0.05, 1)
    Seleccionado.mover((-0.8, -0.3, 1.3))
    Objeto.crearHexagono('Base2', 0.1)
    Seleccionado.mover((0, 0, 1.85))
    
    # Creación de la cámara y el sensor láser
    Objeto.crearCamara('Camara')
    Seleccionado.escalar((0.3, 0.08, 0.1))
    Seleccionado.mover((0, 0.5, 1))
    
    #Seleccionado.escalar((1, 1, 2))
    #Seleccionado.escalar((0.5, 1, 1))

    #seleccionados=['MiEsfera', 'MiCono']
    #seleccionarObjetos(seleccionados)
    #bpy.ops.object.delete(use_global=False)
