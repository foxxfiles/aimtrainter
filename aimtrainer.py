import pygame
import os
import random
import time
import sys
import tkinter as tk
from tkinter import filedialog
from tkinter import simpledialog
import math
import json


def solicitar_nombre_usuario():
    """
    Abre un diálogo para pedir el nombre de usuario.
    """
    root = tk.Tk()
    root.withdraw()
    nombre = simpledialog.askstring("Nombre de Usuario", "Ingrese su nombre de usuario:", parent=root)
    root.destroy()
    
    if nombre is None or nombre.strip() == "":
        nombre = "Anónimo"
    
    return nombre


def cargar_puntajes():
    """
    Carga los puntajes desde el archivo score.json.
    Si el archivo no existe, crea uno nuevo.
    """
    try:
        if os.path.exists("score.json"):
            with open("score.json", "r") as f:
                return json.load(f)
        else:
            return {}
    except Exception as e:
        print(f"Error al cargar puntajes: {e}")
        return {}


def guardar_puntajes(puntajes):
    """
    Guarda los puntajes en el archivo score.json.
    """
    try:
        with open("score.json", "w") as f:
            json.dump(puntajes, f, indent=4)
    except Exception as e:
        print(f"Error al guardar puntajes: {e}")


def obtener_mejores_puntajes(puntajes, limite=10):
    """
    Obtiene los mejores puntajes ordenados de mayor a menor.
    Devuelve una lista de tuplas (nombre_usuario, puntaje).
    """
    # Convertir el diccionario a lista de tuplas
    lista_puntajes = [(usuario, score) for usuario, score in puntajes.items()]
    # Ordenar por puntaje de mayor a menor
    lista_puntajes.sort(key=lambda x: x[1], reverse=True)
    # Devolver solo los N mejores
    return lista_puntajes[:limite]


def seleccionar_directorio():
    """
    Lanza el cuadro de diálogo del sistema para seleccionar un directorio.
    Devuelve la ruta seleccionada o una cadena vacía si se cancela.
    """
    root = tk.Tk()
    root.withdraw()
    directorio = filedialog.askdirectory(title="Seleccione el directorio de imágenes")
    root.destroy()
    return directorio


def cargar_imagenes(directorio):
    """
    Carga todas las imágenes válidas desde el directorio especificado.
    Devuelve una lista con las rutas completas de las imágenes.
    """
    imagenes = []
    if not os.path.exists(directorio):
        print(f"El directorio {directorio} no existe.")
        return imagenes
    
    extensiones_validas = (".png", ".jpg", ".jpeg", ".bmp", ".gif")
    for archivo in os.listdir(directorio):
        if archivo.lower().endswith(extensiones_validas):
            ruta_completa = os.path.join(directorio, archivo)
            if os.path.isfile(ruta_completa):
                imagenes.append(ruta_completa)
    
    return imagenes


def dibujar_botones(screen, fuente, btn_change_rect, btn_skip_rect):
    """
    Dibuja los botones en la pantalla.
    """
    pygame.draw.rect(screen, (80, 80, 80), btn_change_rect)
    pygame.draw.rect(screen, (80, 80, 80), btn_skip_rect)
    
    texto_btn1 = fuente.render("Cambiar Directorio", True, (255, 255, 255))
    texto_btn2 = fuente.render("Saltar Nivel", True, (255, 255, 255))
    
    screen.blit(texto_btn1, (
        btn_change_rect.x + btn_change_rect.width//2 - texto_btn1.get_width()//2,
        btn_change_rect.y + btn_change_rect.height//2 - texto_btn1.get_height()//2
    ))
    screen.blit(texto_btn2, (
        btn_skip_rect.x + btn_skip_rect.width//2 - texto_btn2.get_width()//2,
        btn_skip_rect.y + btn_skip_rect.height//2 - texto_btn2.get_height()//2
    ))


def dibujar_ayuda(screen, fuente, width, height):
    """
    Dibuja el texto de ayuda en la parte inferior de la pantalla.
    """
    ayuda_text = "Presione F12 para liberar/capturar el mouse"
    texto_ayuda = fuente.render(ayuda_text, True, (255, 255, 255))
    screen.blit(
        texto_ayuda,
        (width//2 - texto_ayuda.get_width()//2, height - 70)
    )


def dibujar_puntaje(screen, fuente, puntaje, max_puntaje, nombre_usuario, width, mejores_puntajes):
    """
    Dibuja el puntaje actual, el mejor puntaje y la tabla de mejores puntajes en la parte derecha del canvas.
    """
    # Fuente para los puntajes
    fuente_puntaje = pygame.font.SysFont("Arial", 16)
    fuente_titulo = pygame.font.SysFont("Arial", 18, bold=True)
    
    # Dibujar puntaje actual
    texto_puntaje = fuente_puntaje.render(f"Puntaje: {puntaje}", True, (255, 255, 255))
    screen.blit(texto_puntaje, (width - texto_puntaje.get_width() - 20, 60))
    
    # Dibujar mejor puntaje del usuario actual
    texto_max = fuente_puntaje.render(f"Tu mejor: {max_puntaje}", True, (255, 255, 255))
    screen.blit(texto_max, (width - texto_max.get_width() - 20, 80))
    
    # Dibujar nombre de usuario actual
    texto_usuario = fuente_puntaje.render(f"Usuario: {nombre_usuario}", True, (255, 255, 255))
    screen.blit(texto_usuario, (width - texto_usuario.get_width() - 20, 100))
    
    # Dibujar tabla de mejores puntajes (estilo arcade)
    y_pos = 140
    
    # Título de la tabla
    texto_titulo = fuente_titulo.render("HIGH SCORES", True, (255, 255, 0))
    screen.blit(texto_titulo, (width - texto_titulo.get_width() - 20, y_pos))
    y_pos += 25
    
    # Línea separadora
    pygame.draw.line(screen, (150, 150, 150), 
                    (width - 180, y_pos), 
                    (width - 20, y_pos), 
                    1)
    y_pos += 10
    
    # Listar los mejores puntajes
    for i, (user, score) in enumerate(mejores_puntajes):
        # Destacar al usuario actual
        if user == nombre_usuario:
            color = (255, 255, 0)  # Amarillo para el usuario actual
        else:
            color = (200, 200, 200)  # Gris claro para los demás
            
        # Número de ranking
        rank_text = fuente_puntaje.render(f"{i+1}.", True, color)
        screen.blit(rank_text, (width - 180, y_pos))
        
        # Nombre recortado si es muy largo
        nombre_corto = user if len(user) < 10 else user[:8] + ".."
        name_text = fuente_puntaje.render(nombre_corto, True, color)
        screen.blit(name_text, (width - 160, y_pos))
        
        # Puntaje alineado a la derecha
        score_text = fuente_puntaje.render(f"{score}", True, color)
        screen.blit(score_text, (width - score_text.get_width() - 20, y_pos))
        
        y_pos += 20


def dibujar_objetivo(screen, center_x, center_y, tolerancia):
    """
    Dibuja solo el círculo objetivo usando la tolerancia establecida.
    """
    # Círculo de área válida con transparencia
    circle_surface = pygame.Surface((int(tolerancia*2.2), int(tolerancia*2.2)), pygame.SRCALPHA)
    # Círculo externo más suave
    pygame.draw.circle(circle_surface, (255, 0, 0, 30), (int(tolerancia*1.1), int(tolerancia*1.1)), int(tolerancia*1.1))
    # Círculo interno más intenso
    pygame.draw.circle(circle_surface, (255, 0, 0, 70), (int(tolerancia*1.1), int(tolerancia*1.1)), int(tolerancia*0.8))
    # Borde para mayor visibilidad
    pygame.draw.circle(circle_surface, (255, 0, 0, 120), (int(tolerancia*1.1), int(tolerancia*1.1)), int(tolerancia*1.1), 2)
    screen.blit(circle_surface, (center_x - tolerancia*1.1, center_y - tolerancia*1.1))


def calcular_parametros_nivel(nivel, niveles_totales, diametro_inicial=None):
    """
    Calcula los parámetros del nivel actual.
    """
    # Si no hay diámetro inicial especificado, usar el valor por defecto
    if diametro_inicial is None:
        diametro_inicial = 12
        
    tolerancia = diametro_inicial - ((diametro_inicial - 2) * (nivel - 1) / (niveles_totales - 1))
    recoil_y = -0.3 - ((2.5 - 0.3) * (nivel - 1) / (niveles_totales - 1))
    recoil_x_lower = -0.1 - ((1.0 - 0.1) * (nivel - 1) / (niveles_totales - 1))
    recoil_x_upper = 0.1 + ((1.0 - 0.1) * (nivel - 1) / (niveles_totales - 1))
    
    # Tiempo objetivo: 2 -> 5
    tiempo_objetivo = 2 + (5 - 2) * (nivel - 1) / (niveles_totales - 1)
    
    return tolerancia, recoil_y, recoil_x_lower, recoil_x_upper, tiempo_objetivo


def main():
    pygame.init()
    width, height = 800, 600
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Entrenamiento de Puntería")
    clock = pygame.time.Clock()
    
    center_x, center_y = width // 2, height // 2

    # Solicitar nombre de usuario
    nombre_usuario = solicitar_nombre_usuario()
    
    # Cargar puntajes
    puntajes = cargar_puntajes()
    
    # Verificar si el usuario existe y obtener su mejor puntaje
    if nombre_usuario in puntajes:
        max_puntaje = puntajes[nombre_usuario]
    else:
        max_puntaje = 0
        puntajes[nombre_usuario] = max_puntaje
    
    # Obtener tabla de mejores puntajes
    mejores_puntajes = obtener_mejores_puntajes(puntajes)
    
    # Puntaje actual
    puntaje_actual = 0

    # Botones en las esquinas superiores
    btn_width = 180
    btn_height = 40
    btn_margin = 20
    
    # Botón "Cambiar Directorio" en esquina superior izquierda
    btn_change_rect = pygame.Rect(
        btn_margin, 
        btn_margin, 
        btn_width, 
        btn_height
    )
    # Botón "Saltar Nivel" en esquina superior derecha
    btn_skip_rect = pygame.Rect(
        width - btn_width - btn_margin, 
        btn_margin, 
        btn_width, 
        btn_height
    )
    
    # Inicialmente no se selecciona directorio ni se cargan imágenes
    directorio_imagenes = ""
    imagenes = []
    
    # Capturar el mouse hasta que se presione F12
    pygame.event.set_grab(True)
    pygame.mouse.set_visible(False)

    # Cargar el diámetro del círculo desde config.json si existe
    diametro_inicial = None
    try:
        if os.path.exists("config.json"):
            with open("config.json", "r") as f:
                config = json.load(f)
                if "diametro" in config:
                    diametro_inicial = config["diametro"]
                    print(f"Diámetro cargado desde config.json: {diametro_inicial}")
    except Exception as e:
        print(f"Error al cargar config.json: {e}")
        diametro_inicial = 12  # Valor por defecto si hay error

    niveles_totales = 100
    nivel = 1
    factor_shake = 2.0  # Factor de sacudida
    
    # Fuente para textos
    fuente = pygame.font.SysFont("Arial", 24)

    running_game = True
    skip_level_flag = False  # Para saltar nivel manualmente
    
    while running_game and nivel <= niveles_totales:
        # Obtener parámetros para el nivel actual
        tolerancia, recoil_y, recoil_x_lower, recoil_x_upper, tiempo_objetivo = calcular_parametros_nivel(nivel, niveles_totales, diametro_inicial)
        
        # Si no hay imágenes, esperamos a que el usuario seleccione un directorio
        if not imagenes:
            waiting_for_images = True
            while waiting_for_images and running_game:
                dt = clock.tick(60) / 1000.0
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running_game = False
                        waiting_for_images = False
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_F12:
                            # Alternar captura
                            pygame.event.set_grab(not pygame.event.get_grab())
                            pygame.mouse.set_visible(not pygame.mouse.get_visible())
                        elif event.key == pygame.K_ESCAPE:
                            running_game = False
                            waiting_for_images = False
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:  # Clic izquierdo
                            if btn_change_rect.collidepoint(event.pos):
                                # Cambiar directorio
                                nuevo_dir = seleccionar_directorio()
                                if nuevo_dir:
                                    nuevas_imagenes = cargar_imagenes(nuevo_dir)
                                    if nuevas_imagenes:
                                        directorio_imagenes = nuevo_dir
                                        imagenes = nuevas_imagenes
                                        waiting_for_images = False
                            elif btn_skip_rect.collidepoint(event.pos):
                                skip_level_flag = True
                                waiting_for_images = False
                
                if skip_level_flag:
                    skip_level_flag = False
                    # Avanzar de nivel aunque no haya imágenes
                    nivel += 1
                    waiting_for_images = False
                    break
                
                screen.fill((50, 50, 50))  # Fondo gris oscuro
                
                # Mensaje de "No hay imágenes"
                msg = "Sin imágenes. Use 'Cambiar Directorio' para cargar."
                texto_msg = fuente.render(msg, True, (255, 255, 255))
                screen.blit(texto_msg, (width//2 - texto_msg.get_width()//2, height//2 - texto_msg.get_height()//2))
                
                # Dibujar botones y ayuda
                dibujar_botones(screen, fuente, btn_change_rect, btn_skip_rect)
                dibujar_ayuda(screen, fuente, width, height)
                
                # Dibujar puntaje en la parte derecha
                dibujar_puntaje(screen, fuente, puntaje_actual, max_puntaje, nombre_usuario, width, mejores_puntajes)
                
                pygame.display.flip()
            
            if not running_game:
                break
            # Si aún no hay imágenes, se fuerza la salida de este nivel
            if not imagenes:
                nivel += 1
                continue
        
        # Ahora sí hay imágenes
        imagen_path = random.choice(imagenes)
        try:
            reward_image_loaded = pygame.image.load(imagen_path)
        except (pygame.error, FileNotFoundError, PermissionError) as e:
            print(f"Error al cargar imagen: {e}")
            if imagen_path in imagenes:
                imagenes.remove(imagen_path)
            if not imagenes:
                print("No hay más imágenes disponibles. Saliendo.")
                break
            # Saltar este nivel si falla la carga
            nivel += 1
            continue
        
        # Escalado proporcional
        img_w, img_h = reward_image_loaded.get_size()
        ratio = min(width / img_w, height / img_h)
        new_w = int(img_w * ratio)
        new_h = int(img_h * ratio)
        reward_image_loaded = pygame.transform.scale(reward_image_loaded, (new_w, new_h))
        img_x = (width - new_w) // 2
        img_y = (height - new_h) // 2
        
        compensation = [0.0, 0.0]
        recoil_offset = [0.0, 0.0]
        tiempo_en_objetivo_acumulado = 0.0
        
        # Centrar el mouse y vaciar acumulado
        pygame.mouse.set_pos((center_x, center_y))
        pygame.mouse.get_rel()

        running_level = True
        while running_level and running_game:
            dt = clock.tick(60) / 1000.0
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running_game = False
                    running_level = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F12:
                        # Alternar captura
                        pygame.event.set_grab(not pygame.event.get_grab())
                        pygame.mouse.set_visible(not pygame.mouse.get_visible())
                    elif event.key == pygame.K_ESCAPE:
                        running_game = False
                        running_level = False
                        
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Clic izquierdo
                        if btn_change_rect.collidepoint(event.pos):
                            nuevo_dir = seleccionar_directorio()
                            if nuevo_dir:
                                nuevas_imagenes = cargar_imagenes(nuevo_dir)
                                if nuevas_imagenes:
                                    directorio_imagenes = nuevo_dir
                                    imagenes = nuevas_imagenes
                        elif btn_skip_rect.collidepoint(event.pos):
                            skip_level_flag = True
            
            # Si el usuario pulsó "Saltar Nivel"
            if skip_level_flag:
                skip_level_flag = False
                nivel += 1
                running_level = False
                continue

            if not imagenes:
                # Si se vació la lista de imágenes en runtime, salir
                running_game = False
                running_level = False
                continue

            # Leer movimiento relativo si el mouse está "grabado"
            if pygame.event.get_grab():
                rel = pygame.mouse.get_rel()
                compensation[0] += rel[0]
                compensation[1] += rel[1]

            # Actualizar retroceso
            recoil_x_increment = random.uniform(recoil_x_lower, recoil_x_upper)
            recoil_offset[0] += recoil_x_increment * factor_shake
            recoil_offset[1] += recoil_y * factor_shake

            # Calcular posición real
            effective_x_raw = center_x + compensation[0] + recoil_offset[0]
            effective_y_raw = center_y + compensation[1] + recoil_offset[1]

            # Clamping para dibujar
            effective_x_draw = max(0, min(effective_x_raw, width))
            effective_y_draw = max(0, min(effective_y_raw, height))

            # Distancia al centro
            distancia = math.hypot(effective_x_raw - center_x, effective_y_raw - center_y)

            # Verificar si el botón izquierdo está presionado
            left_button_pressed = pygame.mouse.get_pressed()[0]

            # Acumular tiempo SOLO si está en la zona Y el botón izquierdo está presionado
            if distancia <= tolerancia and left_button_pressed:
                tiempo_en_objetivo_acumulado += dt
            else:
                tiempo_en_objetivo_acumulado = 0.0

            # Verificar avance de nivel
            if tiempo_en_objetivo_acumulado >= tiempo_objetivo:
                nivel += 1
                # Aumentar puntaje cuando se completa un nivel
                puntaje_actual += 100 + int(100 * (nivel / niveles_totales))
                
                # Actualizar el mejor puntaje si es necesario
                if puntaje_actual > max_puntaje:
                    max_puntaje = puntaje_actual
                    puntajes[nombre_usuario] = max_puntaje
                    guardar_puntajes(puntajes)
                    # Actualizar la tabla de mejores puntajes
                    mejores_puntajes = obtener_mejores_puntajes(puntajes)
                
                running_level = False
                break

            # Dibujo de la escena
            # Fondo gris oscuro
            screen.fill((50, 50, 50))
            
            # Mostrar la imagen SOLO si está en la zona y el botón está presionado
            if distancia <= tolerancia and left_button_pressed:
                screen.blit(reward_image_loaded, (img_x, img_y))

            # Dibujar solo el círculo objetivo
            dibujar_objetivo(screen, center_x, center_y, tolerancia)
            
            # Mira (cruceta)
            pygame.draw.line(screen, (0, 255, 0), (int(effective_x_draw) - 10, int(effective_y_draw)), (int(effective_x_draw) + 10, int(effective_y_draw)), 2)
            pygame.draw.line(screen, (0, 255, 0), (int(effective_x_draw), int(effective_y_draw) - 10), (int(effective_x_draw), int(effective_y_draw) + 10), 2)
            
            # Texto info de nivel
            texto_info = fuente.render(
                f"Nivel {nivel}  Tiempo: {tiempo_en_objetivo_acumulado:.2f}/{tiempo_objetivo:.2f} seg",
                True, (255, 255, 255)
            )
            screen.blit(texto_info, (10, height - 30))

            # Dibujar botones y ayuda
            dibujar_botones(screen, fuente, btn_change_rect, btn_skip_rect)
            dibujar_ayuda(screen, fuente, width, height)
            
            # Dibujar puntaje en la parte derecha
            dibujar_puntaje(screen, fuente, puntaje_actual, max_puntaje, nombre_usuario, width, mejores_puntajes)

            pygame.display.flip()

    # Mensaje final cuando se completa todo el entrenamiento
    if running_game and nivel > niveles_totales:
        screen.fill((50, 50, 50))
        fuente_final = pygame.font.SysFont("Arial", 36)
        texto_final = fuente_final.render("¡Entrenamiento completado!", True, (255, 255, 255))
        screen.blit(texto_final, (width//2 - texto_final.get_width()//2, height//2 - texto_final.get_height()//2 - 100))
        
        # Mostrar puntaje final
        fuente_puntaje = pygame.font.SysFont("Arial", 28)
        texto_puntaje = fuente_puntaje.render(f"Puntaje final: {puntaje_actual}", True, (255, 255, 0))
        screen.blit(texto_puntaje, (width//2 - texto_puntaje.get_width()//2, height//2 - 60))
        
        # Verificar una vez más si es un nuevo récord
        if puntaje_actual > max_puntaje:
            max_puntaje = puntaje_actual
            puntajes[nombre_usuario] = max_puntaje
            guardar_puntajes(puntajes)
            
            # Mostrar mensaje de nuevo récord
            texto_record = fuente_puntaje.render("¡NUEVO RÉCORD!", True, (255, 50, 50))
            screen.blit(texto_record, (width//2 - texto_record.get_width()//2, height//2 - 20))
        
        # Mostrar mejor puntaje del usuario
        texto_mejor = fuente_puntaje.render(f"Tu mejor puntaje: {max_puntaje}", True, (255, 255, 255))
        screen.blit(texto_mejor, (width//2 - texto_mejor.get_width()//2, height//2 + 20))
        
        # Actualizar lista de mejores puntajes
        mejores_puntajes = obtener_mejores_puntajes(puntajes)
        
        # Dibujar tabla de HIGH SCORES
        y_pos = height//2 + 80
        fuente_high = pygame.font.SysFont("Arial", 24, bold=True)
        texto_high = fuente_high.render("HIGH SCORES", True, (255, 255, 0))
        screen.blit(texto_high, (width//2 - texto_high.get_width()//2, y_pos))
        y_pos += 30
        
        # Línea separadora
        pygame.draw.line(screen, (150, 150, 150), 
                        (width//2 - 150, y_pos), 
                        (width//2 + 150, y_pos), 
                        1)
        y_pos += 10
        
        # Mostrar los 5 mejores puntajes
        for i, (user, score) in enumerate(mejores_puntajes[:5]):
            # Destacar al usuario actual
            if user == nombre_usuario:
                color = (255, 255, 0)  # Amarillo para el usuario actual
            else:
                color = (200, 200, 200)  # Gris claro para los demás
                
            # Crear texto para el ranking
            rank_str = f"{i+1}. {user}"
            if len(rank_str) > 15:
                rank_str = rank_str[:12] + "..."
                
            rank_text = fuente_puntaje.render(rank_str, True, color)
            score_text = fuente_puntaje.render(f"{score}", True, color)
            
            # Posicionar textos (alineados)
            screen.blit(rank_text, (width//2 - 150, y_pos))
            screen.blit(score_text, (width//2 + 150 - score_text.get_width(), y_pos))
            
            y_pos += 30
        
        pygame.display.flip()
        pygame.time.delay(8000)  # Mostrar por más tiempo para que vean la tabla
    
    pygame.quit()


if __name__ == "__main__":
    main()