# Proyecto Modelado-Creación de un diseño en blender
## (CC-BY-NC-SA) Rubén Montilla

## 0. Introducción

Esta practica tiene como objetivo demostrar las habilidades adquiridas durante las clases a traves de la creación de un diseño en blender. El diseño que se ha elegido a desarrollar se basa en el de un robot que se ha visto por la universidad, el robot Kobuki. Aquí podemos ver varias fotos del mismo:

![alt text](https://github.com/clases-julio/proyecto-modelado3d-RubiMonti/blob/main/images/kobuki.jpeg "Kobuki 1")
![alt text](https://github.com/clases-julio/proyecto-modelado3d-RubiMonti/blob/main/images/kobuki2.jpeg "Kobuki 2")

## 1. Implementación

Para crear este modelo, usaremos la herramienta de scripting que nos proporciona blender. Realizaremos un script en python que al ejecutarlo nos genere el robot dentro del mundo.

Procederemos a montar el robot en distintas partes, primero haremos la base del robot que incluirá las ruedas y un pequeño panel de control, después haremos las dos bases que tiene el robot, y por último haremos la cámara y el laser que pondremos entre la primera y la segunda base.

Para crear la base del robot, haremos un cilindro que representará el cuerpo del robot. A este, le añadiremos las ruedas en la parte inferior, el kobuki posee dos ruedas móviles y dos puntos de apoyo con rudeas sin motor, las ruedas que le dan movimiento al robot las encontramos a los lados y son mas grandes que las que hacen de apoyo. Las ruedas pequeñas se situan una en la parte de alante del robot y la otra en la parte de atrás. 
También hemos añadido al robot un pequeño panel como el del kobuki con distintos conectores, botones y leds. Todo ello lo hemos hecho con una herramienta que es "Bool Tool" que nos permite hacer operaciones booleanas con los cuerpos geométricos. Con un cilindro y un prisma rotado le damos la forma al panel y lo ponemos en el sitio correspondiente.

Después hemos creado las bases que dotarán de altura al robot. Todas las bases estan formadas por cuatro cilindros que soportan la pieza principal de la base, un prisma hexagonal. Cada base tendrá su altura de las barras, pero el prisma es del mismo tamaño en las tres bases. En la primera base, hay que cortar dicho prisma para dejar espacio al panel que hemos creado previamente, esta acción la volvemos a crear con "Bool Tool". Cuando todas las bases están puestas en el sitio correcto tenemos el cuerpo completo por lo que unimos las cuatro piezas: la base móvil y las tres bases fijas.

Por último, crearemos la cámara y el laser. Para ello, hemos utilizado otra vez la herramienta "Bool Tool". 
Empezamos creando la cámara. La base de la cámara será un prisma rectangular que tendrá tres agujeros por las tres lentes que tiene la cámara. Estos agujeros los haremos al hacer la difereencia del prisma con tres conos que hemos definido y colocado para que la punta del cono esté dentro del prisma. Para la base simplemente usaremos un cilindro al que al cambiarle uno de los ejes se convierte en una elipse que sujeta el cuerpo de la cámara.
Para el láser lo que haremos será crear dos troncos de cono que darán la estructura al laser y una semiesfera que será la que contendrá el laser y que en la vida real gira constantemente. Para ello definiremos los dos conos y los cortamos con la ayuda de un cilindro y la herramienta "Bool Tool". La esfera tambien la partimos por la mitad y hacemos que coincida con el tronco de cono pequeño para obtener el laser final.

El resultado final se puede ver a continuación.

## 2. Imágenes

Aquí podemos ver imagenes del modelo de frente y desde una perspectiva oblicua:
![alt text](https://github.com/clases-julio/proyecto-modelado3d-RubiMonti/blob/main/images/front_view.jpeg "Front View")
![alt text](https://github.com/clases-julio/proyecto-modelado3d-RubiMonti/blob/main/images/camera_view.jpeg "Camera View")
