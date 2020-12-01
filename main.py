from PIL import Image, ImageDraw, ImageFont
from math import ceil, sqrt
import os
import gi
import tweepy
import webbrowser
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import sys

# --------------------------------------------------------------------------------- Menus
respuesta_afirmativa = ["sí", "si", "yes", "y", "s"]
respuesta_negativa = ["no", "n"]

menu_principal_str = "------Menu principal------\n" \
                     "a) Imagen\n" \
                     "b) Opciones de Twitter\n" \
                     "c) Ayuda\n" \
                     "x) Salir\n" \
                     " "

menu_a_1_str = "------Imagen------\n" \
               "1) Cargar Imagen\n" \
               "0) Atrás\n" \
               "x) Salir\n" \
               " "
menu_a_2_str = "------Imagen------\n" \
               "1) Cargar Imagen\n" \
               "2) Guardar arte acsii generado\n" \
               "3) Mostrar comparación\n" \
               "0) Atrás\n" \
               "x) Salir\n" \
               " "
menu_a_guardado = "------Guardar------\n" \
                  "1) Guardar Imagen\n" \
                  "2) Guardar Texto\n" \
                  "3) Cambiar nombre\n" \
                  "0) Atrás\n" \
                  "x) Salir\n" \
                  " "
menu_a_ajustes = "Selecciona el aspecto que quieras cambiar o ingresa 0 para continuar\n" \
                 "------Ajustes de Imagen------\n" \
                 "1) Nueva escala ACSII\n" \
                 "2) Invertir colores\n" \
                 "3) Cambiar tamaño\n" \
                 "4) Regresar a la configuración por defecto\n" \
                 "0) Continuar\n" \
                 " "
mostrar_str = "------Comparación de Imagen------\n" \
              "1) Imágenes por separado (recomendado)\n" \
              "2) Imágenes juntas\n" \
              " "

menu_b_1_str = "------Twitter------\n" \
               "1) Ingresar credenciales\n" \
               "0) Atrás\n" \
               "x) Salir\n" \
               " "
menu_b_3_str = "------Twitter------\n" \
               "1) Ingresar credenciales\n" \
               "2) Logout\n" \
               "3) Tweet\n" \
               "0) Atrás\n" \
               "x) Salir\n" \
               " "
tweet_str = "------Tweet------\n" \
            "1) Tweet de imagen (recomendado)\n" \
            "2) Tweet de texto (muy limitado)\n" \
            " "
menu_b_2_str = "------Twitter------\n" \
               "1) Ingresar credenciales\n" \
               "2) Logout\n" \
               "0) Atrás\n" \
               "x) Salir\n" \
               " "

menu_c_str = "------Ayuda------\n" \
             "1) Acerca de\n" \
             "2) Código fuente\n" \
             "0) Atrás\n" \
             "x) Salir\n" \
             " "

consumer_key = os.environ.get("consumer_key")
consumer_secret = os.environ.get("consumer_secret")

callback_uri = 'oob'  # https://cfe.sh/twitter/callback


# Para imprimir las opciones y devolver la opcion elegida si es válida.
def prueba(texto_menu, respuestas_correctas):
    print(texto_menu)
    entrada = input("Elige una opción: ")
    while entrada not in respuestas_correctas:
        print(texto_menu)
        entrada = input("Elige una opción válida: ")
    return entrada


# Para ingresar la ruta y que el programa pueda leerla
def arreglar_direccion_espacios(ruta):
    """
    Cambia en la cadena una secuencia de escape de espacio en blanco por el mismo espacio en blanco.
    :param ruta: Suponiendo que se ingresa una ruta que ha sido copiada de la terminal o cualquier ruta que de
    problemas con la secuencia de escape de espacio.
    :return: la misma ruta que ya puede ser usada por las funciones open() de os y el método .parse() para el archivo
    XML.
    """
    lista_auxiliar = ruta.split("\\")
    direccion_arreglada = ""
    for n in lista_auxiliar:
        direccion_arreglada += n
    return direccion_arreglada


# ------------------------------------------------------------------------------------- Funciones para Arte ACSII
cadena_por_defecto = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/|()1{}[]?-_+~<>i!lI;:,\"^."


def voltear_cadena(cadena):
    resultado = ""
    for c in range(len(cadena)):
        resultado += cadena[- c - 1]
    return resultado


def resize_img_normal(image, nuevo_ancho_f=191):
    ancho_f, alto_f = image.size
    proporcion = alto_f / ancho_f
    nuevo_alto_f = int(nuevo_ancho_f * proporcion)
    resized_image = image.resize((nuevo_ancho_f, nuevo_alto_f))
    return resized_image


def resize_img(image, nuevo_ancho_f=191):
    ancho_f, alto_f = image.size
    proporcion_f = alto_f / ancho_f / 1.65
    nuevo_alto_f = int(nuevo_ancho_f * proporcion_f)
    resized_image = image.resize((nuevo_ancho_f, nuevo_alto_f))
    return resized_image


# convert pixels to a string of ascii characters
def pixels_to_ascii(image, ascii_input):
    ascii_char_str = ascii_input

    ascii_char_tone = []
    for i in ascii_char_str:
        ascii_char_tone.append(i)
    pixels = image.getdata()
    characters = "".join([ascii_char_tone[pixel // ceil(255 / len(ascii_char_tone))] for pixel in pixels])
    return characters


def arte_acsii(ruta, cadena_ascii=cadena_por_defecto, nuevo_ancho=0, invertir_color=False):
    # Para la Ruta
    image = Image.open(ruta).convert("L")

    # Para el tamaño, para el nuevo ancho
    width, height = image.size
    if nuevo_ancho != 0:
        new_width = nuevo_ancho  # Habiendo ingresado el nuevo ancho
    else:
        new_width = width  # El ancho por defecto es el de la imagen original, tantos caracteres como pixeles

    # Para invertir color
    if invertir_color:
        cadena_ascii = voltear_cadena(cadena_ascii)

    # Hacer cadena para arte ACSII
    nueva_cadena_acsii = pixels_to_ascii(resize_img(image, new_width), cadena_ascii)

    # Organizar cadena para arte ACSII
    cantidad_de_pixeles = len(nueva_cadena_acsii)
    cadena_acsii_organizada = "\n".join([nueva_cadena_acsii[index:(index + new_width)]
                                         for index in range(0, cantidad_de_pixeles, new_width)])

    return cadena_acsii_organizada


def imagen_acsii(cadena_organizada):

    lineas = 1
    todas_las_lineas = [[]]
    indice = 0
    for c in range(len(cadena_organizada)):
        todas_las_lineas[indice].append(cadena_organizada[c])
        if cadena_organizada[c] == "\n":
            lineas += 1
            todas_las_lineas.append([])
            indice += 1
    for j in range(len(todas_las_lineas)):
        todas_las_lineas[j] = "".join(todas_las_lineas[j])
    max_linea = max(todas_las_lineas)

    font = ImageFont.truetype("Consolas.ttf", 10)
    max_width, min_height = font.getsize(max_linea)

    img = Image.new('RGB', (max_width, min_height * lineas), "white")

    d = ImageDraw.Draw(img)
    d.multiline_text((0, 0), cadena_organizada, font=font, fill="black")
    return img


class VentanaComparacion(Gtk.ApplicationWindow):

    def __init__(self, app, img1, img2):
        Gtk.Window.__init__(self, title="Paned Example", application=app)
        self.set_default_size(450, 350)

        # a new widget with two adjustable panes,
        # one on the left and one on the right
        paned = Gtk.Paned.new(Gtk.Orientation.HORIZONTAL)
        # To have two vertically aligned panes, use Gtk.Orientation.VERTICAL instead of Gtk.Orientation.HORIZONTAL.
        # The method add1(widget1) will add the widget1 to the top pane, and add2(widget2) will add the widget2 to the
        # bottom pane.

        # two images
        image1 = Gtk.Image()
        image1.set_from_file(img1)
        image2 = Gtk.Image()
        image2.set_from_file(img2)

        # add the first image to the left pane
        paned.add1(image1)
        # add the second image to the right pane
        paned.add2(image2)

        # add the panes to the window
        self.add(paned)


class AplicacionComparacion(Gtk.Application):

    def __init__(self, img_1, img_2):
        Gtk.Application.__init__(self)
        self.img_1 = img_1
        self.img_2 = img_2

    def do_activate(self):
        win = VentanaComparacion(self, self.img_1, self.img_2)
        win.set_position(Gtk.WindowPosition.CENTER)
        win.show_all()

    def do_startup(self):
        Gtk.Application.do_startup(self)


class VentanaCF(Gtk.ApplicationWindow):
    # a window

    def __init__(self, app):
        Gtk.Window.__init__(self, title="Código Fuente", application=app)
        self.set_default_size(250, 50)

        # a linkbutton pointing to the given URI
        button = Gtk.LinkButton(uri="https://github.com/Obsdy/Arte-ACSII")
        # with given text
        button.set_label("Arte ACSII")

        # add the button to the window
        self.add(button)


class CodigoFuente(Gtk.Application):

    def __init__(self):
        Gtk.Application.__init__(self)

    def do_activate(self):
        win = VentanaCF(self)
        win.set_position(Gtk.WindowPosition.CENTER)
        win.show_all()

    def do_startup(self):
        Gtk.Application.do_startup(self)


class AcercaDeVentana(Gtk.ApplicationWindow):

    def __init__(self, app):
        Gtk.Window.__init__(self, title="Acerca de", application=app)
        # self.set_default_size(200, 100)

        label_t = Gtk.Label(label="  Tecnologías:  ")
        label_v = Gtk.Label(label="  Versiones:  ")

        label_t1 = Gtk.Label(label="Python")
        label_t2 = Gtk.Label(label="Gtk+")
        label_t3 = Gtk.Label(label="Pillow")
        label_t4 = Gtk.Label(label="Tweepy")

        label_v1 = Gtk.Label(label="3.8")
        label_v2 = Gtk.Label(label="3.0")
        label_v3 = Gtk.Label(label="8.0")
        label_v4 = Gtk.Label(label="3.9")

        label_a = Gtk.Label(label="  Autor:  ")
        label_a1 = Gtk.Label(label="  Obsdy Jedadías Chet Morales  ")
        label_f = Gtk.Label(label="  Fecha:  ")
        label_f1 = Gtk.Label(label=" 30-11-20 ")
        label_ve = Gtk.Label(label="  Versión:  ")
        label_ve1 = Gtk.Label(label=" 1.0 ")

        hseparator1 = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        hseparator2 = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        hseparator3 = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        hseparator4 = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)

        grid = Gtk.Grid()

        grid.set_row_spacing(10)

        grid.attach(label_t, 0, 0, 1, 1)
        grid.attach(label_v, 1, 0, 1, 1)

        grid.attach(label_t1, 0, 2, 1, 1)
        grid.attach(label_v1, 1, 2, 1, 1)

        grid.attach(label_t2, 0, 3, 1, 1)
        grid.attach(label_v2, 1, 3, 1, 1)

        grid.attach(label_t3, 0, 4, 1, 1)
        grid.attach(label_v3, 1, 4, 1, 1)

        grid.attach(label_t4, 0, 5, 1, 1)
        grid.attach(label_v4, 1, 5, 1, 1)

        grid.attach(hseparator1, 0, 6, 2, 1)

        grid.attach(label_a, 0, 7, 2, 1)
        grid.attach(label_a1, 0, 8, 2, 1)

        grid.attach(hseparator2, 0, 9, 2, 1)

        grid.attach(label_f, 0, 10, 2, 1)
        grid.attach(label_f1, 0, 11, 2, 1)

        grid.attach(hseparator3, 0, 12, 2, 1)

        grid.attach(label_ve, 0, 13, 2, 1)
        grid.attach(label_ve1, 0, 14, 2, 1)

        grid.attach(hseparator4, 0, 15, 2, 1)

        # Supongo que el orden correcto es (child, left, top, width, height)

        grid.set_column_homogeneous(True)
        self.add(grid)


class AcercaDeApp(Gtk.Application):

    def __init__(self):
        Gtk.Application.__init__(self)

    def do_activate(self):
        win = AcercaDeVentana(self)
        win.set_position(Gtk.WindowPosition.CENTER)
        win.show_all()


arte_imagen = " "
arte_str = ""
cadena_imagen = ""
cadena_imagen += ""

credenciales_usuario = False
auth = " "
redirect_url = " "
api = " "
# ----------------------------------------------------------------------------------------------- Programa Principal
while True:
    menu_principal_respuesta = prueba(menu_principal_str, ["a", "b", "c", "x"])
    if menu_principal_respuesta == "x":
        break
    elif menu_principal_respuesta == "a":  # Entramos a las opciones de imagen -------------------------------- IMAGEN
        menu_a_respuesta = ""
        menu_a_respuesta += ""
        cerrar = False
        while True:
            if arte_imagen != " ":
                menu_a_respuesta = prueba(menu_a_2_str, ["1", "2", "3", "0", "x"])
            else:
                menu_a_respuesta = prueba(menu_a_1_str, ["1", "0", "x"])

            if menu_a_respuesta == "0":
                break
            elif menu_a_respuesta == "x":
                cerrar = True
                sys.exit(exit_status)
            elif menu_a_respuesta == "1":

                cadena_acsii_input = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/|()1{}[]?-_+~<>i!lI;:,\"^."
                nuevo_ancho_input = 0
                invertir_color_input = False

                while True:
                    menu_a_ajustes_respuesta = prueba(menu_a_ajustes, ["1", "2", "3", "4", "0"])
                    if menu_a_ajustes_respuesta == "0":
                        break
                    elif menu_a_ajustes_respuesta == "1":
                        cadena_acsii_input = input("Ingresa una cadena nueva\n")
                    elif menu_a_ajustes_respuesta == "3":
                        nuevo_ancho_input = int(input("Ingresa el nuevo ancho\n"))
                    elif menu_a_ajustes_respuesta == "2":
                        pregunta = input("Deseas invertir el color? (sí/no)\n")
                        if pregunta in respuesta_afirmativa:
                            invertir_color_input = True
                        elif pregunta in respuesta_negativa:
                            invertir_color_input = False
                        else:
                            print("Respuesta inválida")
                    elif menu_a_ajustes_respuesta == "4":
                        cadena_acsii_input = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/|()1{}[]?-_+~<>i!lI;:,\"^."
                        nuevo_ancho_input = 0
                        invertir_color_input = False

                cadena_correcta = False
                while not cadena_correcta:
                    try:
                        cadena_imagen = arreglar_direccion_espacios(input("Ingresa la ruta:\n"))
                        arte_str = arte_acsii(cadena_imagen, cadena_acsii_input,
                                              nuevo_ancho_input, invertir_color_input)
                        cadena_correcta = True
                    except FileNotFoundError:
                        print("No existe esta ruta\n")

                arte_imagen = imagen_acsii(arte_str)

            elif menu_a_respuesta == "2":
                nombre_de_guardado = arreglar_direccion_espacios(input("Ingresa el nombre"
                                                                       " para guardar el arte ACSII: "))
                contador = 0
                for a in range(len(nombre_de_guardado)):
                    if nombre_de_guardado[a] == "/":
                        contador += 1
                menu_a_guardado_respuesta = prueba(menu_a_guardado, ["1", "2", "3", "0", "x"])
                if menu_a_guardado_respuesta == "0":
                    pass
                elif menu_a_guardado_respuesta == "x":
                    cerrar = True
                    break
                elif menu_a_guardado_respuesta == "3":
                    nombre_de_guardado = arreglar_direccion_espacios(input("Ingresa el nombre"
                                                                           " para guardar el arte ACSII: "))
                elif menu_a_guardado_respuesta == "1":
                    if contador >= 2:
                        arte_imagen.save(nombre_de_guardado + ".PNG")
                    else:
                        arte_imagen.save("Resultados/" + nombre_de_guardado + ".PNG")
                elif menu_a_guardado_respuesta == "2":
                    if contador >= 2:
                        with open(nombre_de_guardado + ".txt", "w") as f:
                            f.write(arte_str)
                    else:
                        with open("Resultados/" + nombre_de_guardado + ".txt", "w") as f:
                            f.write(arte_str)
            elif menu_a_respuesta == "3":
                original = Image.open(cadena_imagen)

                mostrar_respuesta = prueba(mostrar_str, ["1", "2"])
                if mostrar_respuesta == "1":
                    original.show()
                    arte_imagen.show()
                elif mostrar_respuesta == "2":
                    ancho = input("Ingresa el ancho de la imagen o presiona enter: ")
                    if ancho == "":
                        ancho = 800
                    original_mediano = resize_img_normal(original, int(ancho))
                    arte_imagen_mediano = resize_img_normal(arte_imagen, int(ancho))
                    directorio_actual = os.getcwd()
                    im_1 = directorio_actual + "/Proceso/Imagen_1.PNG"
                    im_2 = directorio_actual + "/Proceso/Imagen_2.PNG"
                    original_mediano.save(im_1)
                    arte_imagen_mediano.save(im_2)
                    app = AplicacionComparacion(im_1, im_2)
                    exit_status = app.run(sys.argv)
        if cerrar:
            break
    elif menu_principal_respuesta == "b":  # Entramos a las opciones de Twitter -------------------------------- Twitter
        menu_b_respuesta = ""
        menu_b_respuesta += ""
        cerrar = False
        while True:
            if credenciales_usuario and arte_imagen != " ":
                menu_b_respuesta = prueba(menu_b_3_str, ["1", "2", "3", "0", "x"])
            elif credenciales_usuario:
                menu_b_respuesta = prueba(menu_b_2_str, ["1", "2", "0", "x"])
            else:
                menu_b_respuesta = prueba(menu_b_1_str, ["1", "0", "x"])

            if menu_b_respuesta == "0":
                break
            elif menu_b_respuesta == "x":
                cerrar = True
                break
            elif menu_b_respuesta == "1":
                auth = tweepy.OAuthHandler(consumer_key, consumer_secret, callback_uri)
                redirect_url = auth.get_authorization_url()
                webbrowser.open(redirect_url)
                user_pint_input = input("Ingresa el pin para otorgar permiso: ")
                auth.get_access_token(user_pint_input)
                api = tweepy.API(auth)
                credenciales_usuario = True

            elif menu_b_respuesta == "2":
                while True:
                    print("Para cerrar la sesión se mostrará la misma pestaña con la que ingresaste.\n"
                          "Selecciona el ícono con la imagen de tu cuenta y cierra la sesión.\n"
                          "Por el momento, así como no podemos abrir la cuenta por ti, tampoco podemos cerrarla.\n")
                    input("Presiona enter para continuar\n")
                    auth = tweepy.OAuthHandler(consumer_key, consumer_secret, callback_uri)
                    redirect_url = auth.get_authorization_url()
                    webbrowser.open(redirect_url)
                    print("Ahora confirmaremos que efectivamente has cerrado sesión")
                    input("Presiona enter para continuar y cierra la pestaña después de haber verificado.\n")
                    webbrowser.open(redirect_url)
                    enter = input("¿Has finalizado sesión? (sí/no)\n")
                    if enter in respuesta_afirmativa:
                        auth = " "
                        redirect_url = " "
                        api = " "
                        credenciales_usuario = False
                        break
                    elif enter in respuesta_negativa:
                        pass

            elif menu_b_respuesta == "3":
                tweet_respuesta = prueba(tweet_str, ["1", "2"])
                if tweet_respuesta == "1":
                    directorio_actual = os.getcwd()
                    im_2 = directorio_actual + "/Proceso/Img_Twt.PNG"
                    arte_imagen.save(im_2)
                    size = os.path.getsize(im_2)
                    if size > 4883000:
                        print("La imagen es muy grande, no se puede publicar")
                        print("Intenta cambiando el tamaño al crear el arte ACSII")
                        enter = input("Quieres publicar la imagen a pesar de perder calidad? (sí/no)\n")
                        if enter in respuesta_afirmativa:
                            arte_imagen_mediano = resize_img_normal(arte_imagen, 600)
                            directorio_actual = os.getcwd()
                            im_2 = directorio_actual + "/Proceso/Img_Twt.PNG"
                            arte_imagen.save(im_2)
                            img_obj = api.media_upload(im_2)
                            new_status = api.update_status("#ASCIIArtPM1", media_ids=[img_obj.media_id_string])

                    else:
                        img_obj = api.media_upload(im_2)
                        new_status = api.update_status("#ASCIIArtPM1", media_ids=[img_obj.media_id_string])
                elif tweet_respuesta == "2":
                    if len(arte_str) > 268:
                        print("El máximo de caracteres en Twitter es de 280, quitando #ASCIIArtPM1 el límite es 268.")
                        print("La imagen que convertiste tiene " + str(len(arte_str)) + " caracteres")
                        datos = arte_str.split("\n")
                        ancho_str = len(datos[0])
                        proporcion_lado = sqrt(268 / len(arte_str))
                        print("Para poder publicarlo te recomiendo hacer de nuevo la imagen pero cambiando el ancho a "
                              + str(int(ancho_str * proporcion_lado)))
                    else:
                        new_status = api.update_status("#ASCIIArtPM1\n" + arte_str)

        if cerrar:
            break

    elif menu_principal_respuesta == "c":  # Entramos a las opciones de ayuda -------------------------------- ayuda
        menu_c_respuesta = ""
        menu_c_respuesta += ""
        cerrar = False
        while True:
            menu_c_respuesta = prueba(menu_c_str, ["1", "2", "0", "x"])
            if menu_c_respuesta == "0":
                break
            elif menu_c_respuesta == "x":
                cerrar = True
                break
            elif menu_c_respuesta == "1":
                app = AcercaDeApp()
                exit_status = app.run(sys.argv)
            elif menu_c_respuesta == "2":
                app = CodigoFuente()
                exit_status = app.run(sys.argv)

        if cerrar:
            break
