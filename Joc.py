import pygame
import sys
import random

# Inicializar Pygame
pygame.init()
pygame.mixer.init()  # Inicializar el módulo de mixer para el sonido

# Configuración de la pantalla
WIDTH, HEIGHT = 854, 480  # Cambiado a 800x600 como solicitado
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Kimetsu RPG")

# Cargar música para diferentes secciones del juego
try:
    # Define rutas para los archivos de música (ajusta estas rutas según donde tengas tus archivos)
    menu_music_path = "menu.mp3"  # Música para el menú
    game_music_path = "joc.mp3"  # Música para el juego principal
    credits_music_path = "Kimetsu no Yaiba Opening.mp3"  # Música para los créditos

    # Cargar los archivos de música
    pygame.mixer.music.set_volume(0.5)  # Establece el volumen (0.0 a 1.0)
except pygame.error as e:
    print(f"No se pudo cargar la música: {e}")

# Variable para controlar qué música está sonando
current_music = None


# Función para cambiar la música según el estado del juego
def change_music(music_path):
    global current_music

    # Si es la misma música que ya está sonando, no hacer nada
    if current_music == music_path:
        return

    try:
        # Detener la música actual si hay alguna sonando
        pygame.mixer.music.stop()

        # Cargar y reproducir la nueva música
        pygame.mixer.music.load(music_path)
        pygame.mixer.music.play(-1)  # El -1 hace que se repita indefinidamente

        # Actualizar la variable de seguimiento
        current_music = music_path
    except pygame.error as e:
        print(f"Error al cambiar la música: {e}")
        current_music = None


# Cargar imágenes
try:
    # Fondo
    background_img = pygame.image.load("mapamapa.png").convert_alpha()
    menu_img = pygame.image.load("menu.png").convert_alpha()

    # Imágenes del jugador (4 direcciones)
    player_up_img = pygame.image.load("/home/alumne/PyCharmMiscProject/kimetsu/assets/up0.png").convert_alpha()
    player_down_img = pygame.image.load("/home/alumne/PyCharmMiscProject/kimetsu/assets/down0.png").convert_alpha()
    player_left_img = pygame.image.load("/home/alumne/PyCharmMiscProject/kimetsu/assets/left0.png").convert_alpha()
    player_right_img = pygame.image.load("/home/alumne/PyCharmMiscProject/kimetsu/assets/right0.png").convert_alpha()

    # Imágenes de enemigos - CORREGIDO: Ahora cargando 3 enemigos diferentes
    enemy_img = pygame.image.load("/home/alumne/PyCharmMiscProject/kimetsu/assets/akaza.png").convert_alpha()
    enemy2_img = pygame.image.load("/home/alumne/PyCharmMiscProject/kimetsu/EMMA.png").convert_alpha()
    enemy3_img = pygame.image.load("/home/alumne/PyCharmMiscProject/kimetsu/kyogai.png").convert_alpha()

    # Imagen del boss
    boss_img = pygame.image.load("/home/alumne/PyCharmMiscProject/kimetsu/assets/muzan.png").convert_alpha()

    # Fondo de batalla
    battle_bg_img = pygame.image.load(
        "/home/alumne/PyCharmMiscProject/kimetsu/combatcombat.png").convert_alpha()
except pygame.error as e:
    print(f"No se pudo cargar una imagen: {e}")
    sys.exit()

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 128, 0)  # Verde más oscuro
BLUE = (0, 0, 255)
YELLOW = (255, 215, 0)  # Oro para resaltar
PURPLE = (128, 0, 128)  # Púrpura para contraste
NAVY = (0, 0, 128)  # Azul marino
DARK_RED = (139, 0, 0)  # Rojo oscuro
TRANSPARENT = (0, 0, 0, 0)

# Fuentes
font_36 = pygame.font.Font(None, 36)
font_24 = pygame.font.Font(None, 24)

# Definir los bordes donde no se puede pasar (simulando árboles)
borders = [
    pygame.Rect(100, 100, 200, 50),  # Borde superior izquierdo
    pygame.Rect(500, 100, 200, 50),  # Borde superior derecho
    pygame.Rect(100, 450, 200, 50),  # Borde inferior izquierdo
    pygame.Rect(500, 450, 200, 50),  # Borde inferior derecho
]


# Clases del juego
class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 50
        self.height = 50
        self.speed = 5
        self.hp = 100
        self.max_hp = 100
        self.extra_lives = 1
        self.level = 1
        self.rect = pygame.Rect(x, y, self.width, self.height)

        # Dirección actual del jugador
        self.current_direction = "down"  # Dirección inicial

    def move(self, dx, dy):
        # Guardar posición anterior para poder revertir si hay colisión
        old_x, old_y = self.x, self.y

        # Actualizar dirección
        if dx > 0:
            self.current_direction = "right"
        elif dx < 0:
            self.current_direction = "left"
        elif dy > 0:
            self.current_direction = "down"
        elif dy < 0:
            self.current_direction = "up"

        # Intentar mover
        if self.x + dx > 0 and self.x + dx < WIDTH - self.width:
            self.x += dx
        if self.y + dy > 0 and self.y + dy < HEIGHT - self.height:
            self.y += dy

        # Actualizar rectángulo
        self.rect.x = self.x
        self.rect.y = self.y

    def draw(self):
        # Seleccionar la imagen según la dirección
        current_img = player_down_img  # Imagen por defecto
        if self.current_direction == "up":
            current_img = player_up_img
        elif self.current_direction == "down":
            current_img = player_down_img
        elif self.current_direction == "left":
            current_img = player_left_img
        elif self.current_direction == "right":
            current_img = player_right_img

        # Dibujar el jugador
        screen.blit(current_img, (self.x, self.y))

        # Barra de vida
        pygame.draw.rect(screen, RED, (self.x, self.y - 10, self.width, 5))
        pygame.draw.rect(screen, GREEN, (self.x, self.y - 10, self.width * (self.hp / self.max_hp), 5))


class Enemy:
    def __init__(self, x, y, enemy_type=0, is_boss=False):
        self.x = x
        self.y = y
        self.width = 50
        self.height = 50
        self.is_boss = is_boss
        self.enemy_type = enemy_type  # 0=akaza, 1=EMMA, 2=kyogai

        # Los bosses tienen más HP
        if is_boss:
            self.hp = 100
            self.max_hp = 100
        else:
            self.hp = 50
            self.max_hp = 50

        self.rect = pygame.Rect(x, y, self.width, self.height)

    def draw(self):
        # Dibujar enemigos usando imágenes según su tipo
        if self.is_boss:
            screen.blit(boss_img, (self.x, self.y))
        else:
            # Seleccionar imagen según el tipo de enemigo
            if self.enemy_type == 0:
                screen.blit(enemy_img, (self.x, self.y))  # Akaza
            elif self.enemy_type == 1:
                screen.blit(enemy2_img, (self.x, self.y))  # EMMA
            elif self.enemy_type == 2:
                screen.blit(enemy3_img, (self.x, self.y))  # Kyogai

        # Barra de vida
        pygame.draw.rect(screen, RED, (self.x, self.y - 10, self.width, 5))
        pygame.draw.rect(screen, GREEN, (self.x, self.y - 10, self.width * (self.hp / self.max_hp), 5))


# Creación de objetos del juego
player = Player(WIDTH // 2, HEIGHT // 2)
enemies = []
bosses_defeated = 0
max_bosses = 2  # Solo habrá 2 bosses como solicitado


# Función para verificar si una posición está libre de colisiones
def is_position_valid(x, y, width, height):
    rect = pygame.Rect(x, y, width, height)

    # Comprobar colisiones con bordes (árboles)
    for border in borders:
        if rect.colliderect(border):
            return False

    # Comprobar colisiones con jugador
    if rect.colliderect(player.rect):
        return False

    # Comprobar colisiones con otros enemigos
    for enemy in enemies:
        if rect.colliderect(enemy.rect):
            return False

    return True


# Función para generar enemigos
def generate_enemies():
    enemies.clear()

    # Si aún no hemos derrotado los 2 bosses, generamos uno
    if bosses_defeated < max_bosses:
        # Intentar encontrar una posición válida para el boss
        for _ in range(100):  # Intentar hasta 100 veces
            x = random.randint(50, WIDTH - 100)
            y = random.randint(50, HEIGHT - 100)
            if is_position_valid(x, y, 50, 50) and (abs(x - player.x) > 150 or abs(y - player.y) > 150):
                enemies.append(Enemy(x, y, is_boss=True))
                break

    # Generar enemigos normales (siempre 3 diferentes)
    enemy_types_used = []  # Para controlar qué tipos ya hemos usado

    # Asegurarnos de usar los 3 tipos de enemigo
    for enemy_type in range(3):  # 0=akaza, 1=EMMA, 2=kyogai
        # Intentar encontrar una posición válida
        for _ in range(100):  # Intentar hasta 100 veces
            x = random.randint(50, WIDTH - 100)
            y = random.randint(50, HEIGHT - 100)
            if is_position_valid(x, y, 50, 50) and (abs(x - player.x) > 150 or abs(y - player.y) > 150):
                enemies.append(Enemy(x, y, enemy_type=enemy_type, is_boss=False))
                enemy_types_used.append(enemy_type)
                break


# Estados del juego
MENU = 0
PLAYING = 1
BATTLE = 2
GAME_OVER = 3
VICTORY = 4
GAME_COMPLETE = 5  # Estado para cuando se han derrotado los 2 bosses
CREDITS = 6  # Nuevo estado para los créditos
FINAL_VICTORY = 7  # Nuevo estado para mostrar un mensaje de victoria final antes de volver al menú
game_state = MENU

# Variable para el menú seleccionado
selected_menu_option = 0
menu_options = ["Jugar", "Créditos", "Salir"]

# Variable para controlar si la música está activada
music_enabled = True

# Contador para el mensaje de victoria final
victory_message_timer = 0


# Función para activar/desactivar música
def toggle_music():
    global music_enabled
    music_enabled = not music_enabled

    if music_enabled:
        # Reanudar la música correspondiente al estado actual
        if game_state == MENU:
            change_music(menu_music_path)
        elif game_state == PLAYING or game_state == BATTLE:
            change_music(game_music_path)
        elif game_state == CREDITS:
            change_music(credits_music_path)
    else:
        # Detener toda la música
        pygame.mixer.music.stop()
        global current_music
        current_music = None


# Función para dibujar el menú
def draw_menu():
    # Asegurar que suene la música del menú
    if music_enabled and current_music != menu_music_path:
        change_music(menu_music_path)

    try:
        screen.blit(menu_img, (0, 0))
    except:
        screen.fill(WHITE)

    title = font_36.render("KIMETSU RPG", True, DARK_RED)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 4))

    # Dibujar las opciones del menú
    for i, option in enumerate(menu_options):
        # Cambiar el color si está seleccionada
        if i == selected_menu_option:
            color = PURPLE
        else:
            color = BLACK

        # Renderizar la opción
        option_text = font_24.render(f"{i + 1}. {option}", True, color)
        screen.blit(option_text, (WIDTH // 2 - option_text.get_width() // 2, HEIGHT // 2 + i * 40))

    # Mostrar estado de la música
    music_text = font_24.render(f"Música: {'ON' if music_enabled else 'OFF'} (M para a Apagar o Encender)", True, BLACK)
    screen.blit(music_text, (WIDTH // 2 - music_text.get_width() // 2, HEIGHT - 50))


# Función para dibujar los créditos
def draw_credits():
    # Asegurar que suene la música de créditos
    if music_enabled and current_music != credits_music_path:
        change_music(credits_music_path)

    try:
        # Podemos usar el fondo del menú o un color sólido
        screen.blit(menu_img, (0, 0))
    except:
        screen.fill(WHITE)

    title = font_36.render("CRÉDITOS", True, DARK_RED)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 4))

    # Información de los créditos
    credits_lines = [
        "Desarrollado por: Sergi Salmerón i Carla Rodríguez",
        "Gráficos y Código: Sergi Salmerón i Carla Rodríguez",
        "Música: Banda Sonora Original i recursos de FreeSound",
        "",
        "Grácias por jugar a Kimetsu RPG",
        "",
        "Presiona ESC para salir al menú principal"
    ]

    # Dibujar cada línea
    line_y = HEIGHT // 3
    for line in credits_lines:
        text = font_24.render(line, True, BLACK)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, line_y))
        line_y += 40

    # Mostrar estado de la música
    music_text = font_24.render(f"Música: {'ON' if music_enabled else 'OFF'} (M para cambiar)", True, BLACK)
    screen.blit(music_text, (WIDTH // 2 - music_text.get_width() // 2, HEIGHT - 50))


# Función para dibujar el juego
def draw_game():
    # Asegurar que suene la música del juego
    if music_enabled and current_music != game_music_path:
        change_music(game_music_path)

    try:
        # Usar imagen de fondo escalada al tamaño de la pantalla
        scaled_bg = pygame.transform.scale(background_img, (WIDTH, HEIGHT))
        screen.blit(scaled_bg, (0, 0))
    except:
        screen.fill(BLACK)

    for enemy in enemies:
        enemy.draw()

    player.draw()

    # HUD
    hud_text = font_24.render(
        f"HP: {player.hp}/{player.max_hp} | Vidas: {player.extra_lives} | Nivel: {player.level} | Bosses: {bosses_defeated}/{max_bosses}",
        True, WHITE)
    screen.blit(hud_text, (10, 10))

    # Mostrar estado de la música (pequeño indicador en la esquina)
    music_text = font_24.render(f"Música: {'ON' if music_enabled else 'OFF'} (M)", True, WHITE)
    screen.blit(music_text, (WIDTH - music_text.get_width() - 10, 10))


# Variables de batalla
current_enemy = None
battle_message = ""
battle_options = ["Atacar", "Curarse",]
selected_option = 0


# Función para dibujar la batalla
def draw_battle():
    # Durante la batalla seguimos usando la música del juego
    if music_enabled and current_music != game_music_path:
        change_music(game_music_path)

    # Usar imagen de fondo de batalla
    try:
        # Escalar la imagen al tamaño de la pantalla
        scaled_battle_bg = pygame.transform.scale(battle_bg_img, (WIDTH, HEIGHT))
        screen.blit(scaled_battle_bg, (0, 0))
    except:
        # Respaldo a color blanco si no se puede cargar la imagen
        screen.fill(WHITE)

    # Estadísticas
    player_stats = font_24.render(f"HP: {player.hp}/{player.max_hp}", True, WHITE)

    # Mostrar diferente texto según si es boss o enemigo normal
    if current_enemy.is_boss:
        enemy_title = "Boss"
    else:
        enemy_title = "Enemigo"

    enemy_stats = font_24.render(f"{enemy_title} HP: {current_enemy.hp}/{current_enemy.max_hp}", True, WHITE)
    screen.blit(player_stats, (50, 50))
    screen.blit(enemy_stats, (WIDTH - 200, 50))

    # Personajes
    screen.blit(player_down_img, (150, HEIGHT // 2 - 40))  # Jugador con imagen

    # Color diferente según tipo de enemigo
    if current_enemy.is_boss:
        screen.blit(boss_img, (WIDTH - 230, HEIGHT // 2 - 40))  # Boss
    else:
        # Mostrar la imagen según el tipo de enemigo
        if current_enemy.enemy_type == 0:
            screen.blit(enemy_img, (WIDTH - 230, HEIGHT // 2 - 40))  # Akaza
        elif current_enemy.enemy_type == 1:
            screen.blit(enemy2_img, (WIDTH - 230, HEIGHT // 2 - 40))  # EMMA
        elif current_enemy.enemy_type == 2:
            screen.blit(enemy3_img, (WIDTH - 230, HEIGHT // 2 - 40))  # Kyogai

    # Mensaje de batalla
    message = font_24.render(battle_message, True, BLACK)
    screen.blit(message, (WIDTH // 2 - message.get_width() // 2, HEIGHT - 200))

    # Opciones
    for i, option in enumerate(battle_options):
        color = PURPLE if i == selected_option else BLACK
        option_text = font_24.render(option, True, color)
        screen.blit(option_text, (WIDTH // 2 - option_text.get_width() // 2, HEIGHT - 150 + i * 40))


# Función para dibujar game over
def draw_game_over():
    # Detener música al Game Over
    if music_enabled:
        pygame.mixer.music.stop()
        global current_music
        current_music = None

    screen.fill(WHITE)
    game_over_text = font_36.render("¡GAME OVER!", True, DARK_RED)
    screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 3))

    restart_text = font_24.render("Presiona R para reiniciar", True, BLACK)
    screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2))


# Función para dibujar victoria
def draw_victory():
    screen.fill(WHITE)

    victory_text = font_36.render("¡VICTORIA!", True, GREEN)
    next_text = font_24.render("Presiona N para continuar", True, BLACK)

    screen.blit(victory_text, (WIDTH // 2 - victory_text.get_width() // 2, HEIGHT // 3))
    screen.blit(next_text, (WIDTH // 2 - next_text.get_width() // 2, HEIGHT // 2))


# Función para dibujar victoria final
def draw_final_victory():
    screen.fill(WHITE)

    complete_text = font_36.render("¡FELICIDADES! ¡HAS DERROTADO A TODOS LOS BOSSES!", True, GREEN)
    screen.blit(complete_text, (WIDTH // 2 - complete_text.get_width() // 2, HEIGHT // 3))

    back_text = font_24.render("Volviendo al menú principal...", True, BLACK)
    screen.blit(back_text, (WIDTH // 2 - back_text.get_width() // 2, HEIGHT // 2))


# Función para iniciar batalla
def start_battle(enemy):
    global game_state, current_enemy, battle_message, selected_option
    game_state = BATTLE
    current_enemy = enemy

    if enemy.is_boss:
        battle_message = "¡Un BOSS apareció! ¿Qué harás?"
    else:
        battle_message = "¡Un enemigo apareció! ¿Qué harás?"

    selected_option = 0


# Función para atacar
def attack():
    global battle_message, bosses_defeated

    # Jugador ataca
    damage = random.randint(5, 15)
    current_enemy.hp -= damage
    battle_message = f"¡Atacaste y causaste {damage} de daño!"

    # Verificar si el enemigo fue derrotado
    if current_enemy.hp <= 0:
        # Si era un boss, incrementar contador
        if current_enemy.is_boss:
            bosses_defeated += 1

        # Eliminar enemigo de la lista
        if current_enemy in enemies:
            enemies.remove(current_enemy)

        end_battle(True)
        return

    # Enemigo ataca
    enemy_damage = random.randint(10, 20)
    player.hp -= enemy_damage
    battle_message += f" El enemigo te causó {enemy_damage} de daño."

    # Verificar si el jugador fue derrotado
    if player.hp <= 0:
        if player.extra_lives > 0:
            player.extra_lives -= 1
            player.hp = player.max_hp
            battle_message = "¡Has usado una vida extra!"
        else:
            end_battle(False)


# Función para curarse
def heal():
    global battle_message

    # Curación
    heal_amount = random.randint(15, 25)
    player.hp = min(player.hp + heal_amount, player.max_hp)
    battle_message = f"¡Te has curado {heal_amount} puntos de vida!"

    # Enemigo ataca
    enemy_damage = random.randint(10, 20)
    player.hp -= enemy_damage
    battle_message += f" El enemigo te causó {enemy_damage} de daño."

    # Verificar si el jugador fue derrotado
    if player.hp <= 0:
        if player.extra_lives > 0:
            player.extra_lives -= 1
            player.hp = player.max_hp
            battle_message = "¡Has usado una vida extra!"
        else:
            end_battle(False)


# Función para huir
def escape():
    global game_state, battle_message

    # 50% de probabilidad de escapar
    if random.random() > 0.5:
        game_state = PLAYING
    else:
        battle_message = "¡No pudiste escapar!"

        # Enemigo ataca
        enemy_damage = random.randint(10, 20)
        player.hp -= enemy_damage
        battle_message += f" El enemigo te causó {enemy_damage} de daño."

        # Verificar si el jugador fue derrotado
        if player.hp <= 0:
            if player.extra_lives > 0:
                player.extra_lives -= 1
                player.hp = player.max_hp
                battle_message = "¡Has usado una vida extra!"
            else:
                end_battle(False)


# Función para finalizar batalla
def end_battle(victory):
    global game_state, victory_message_timer

    if victory:
        # Verificar si se han derrotado todos los bosses
        if bosses_defeated >= max_bosses:
            game_state = FINAL_VICTORY
            victory_message_timer = 180  # Aproximadamente 3 segundos a 60 FPS
        else:
            game_state = VICTORY
    else:
        game_state = GAME_OVER


# Función para reiniciar el juego
def restart_game():
    global game_state, player, bosses_defeated

    player = Player(WIDTH // 2, HEIGHT // 2)
    bosses_defeated = 0
    generate_enemies()
    game_state = PLAYING


# Función para continuar después de una victoria
def continue_game():
    global game_state

    player.hp = player.max_hp

    # Si quedan enemigos en la pantalla, no generar nuevos
    if not enemies:
        generate_enemies()

    game_state = PLAYING


# Iniciar el juego generando enemigos
generate_enemies()

# Bucle principal del juego
clock = pygame.time.Clock()
running = True

# Comenzar con la música del menú
if music_enabled:
    change_music(menu_music_path)

while running:
    # Gestión de eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            # Tecla M para activar/desactivar música en cualquier estado
            if event.key == pygame.K_m:
                toggle_music()

            if game_state == MENU:
                # Navegar por las opciones del menú
                if event.key == pygame.K_UP:
                    selected_menu_option = (selected_menu_option - 1) % len(menu_options)
                elif event.key == pygame.K_DOWN:
                    selected_menu_option = (selected_menu_option + 1) % len(menu_options)

                # Seleccionar una opción del menú por número
                if event.key == pygame.K_1:
                    selected_menu_option = 0  # Jugar
                    game_state = PLAYING
                elif event.key == pygame.K_2:
                    selected_menu_option = 1  # Créditos
                    game_state = CREDITS
                elif event.key == pygame.K_3:
                    running = False  # Salir

                # Seleccionar opción con Enter
                elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    if selected_menu_option == 0:  # Jugar
                        game_state = PLAYING
                    elif selected_menu_option == 1:  # Créditos
                        game_state = CREDITS
                    elif selected_menu_option == 2:  # Salir
                        running = False

            elif game_state == CREDITS:
                # Volver al menú desde los créditos
                if event.key == pygame.K_ESCAPE:
                    game_state = MENU

            elif game_state == BATTLE:
                if event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % len(battle_options)
                elif event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % len(battle_options)
                elif event.key == pygame.K_RETURN:
                    if selected_option == 0:  # Atacar
                        attack()
                    elif selected_option == 1:  # Curarse
                        heal()
                    elif selected_option == 2:  # Huir
                        escape()

            elif game_state == GAME_OVER:
                if event.key == pygame.K_r:
                    restart_game()

            elif game_state == VICTORY:
                if event.key == pygame.K_n:
                    continue_game()

    # Lógica del juego
    if game_state == PLAYING:
        # Movimiento del jugador
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            player.move(-player.speed, 0)
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            player.move(player.speed, 0)
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            player.move(0, -player.speed)
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            player.move(0, player.speed)

        # Comprobar colisiones con enemigos
        for enemy in enemies:
            if player.rect.colliderect(enemy.rect):
                start_battle(enemy)
                break

        # Si no quedan enemigos, generar nuevos
        if not enemies:
            generate_enemies()

    # Gestión del temporizador para el mensaje de victoria final
    elif game_state == FINAL_VICTORY:
        victory_message_timer -= 1
        if victory_message_timer <= 0:
            # Reiniciar el juego y volver al menú principal
            player = Player(WIDTH // 2, HEIGHT // 2)
            bosses_defeated = 0
            game_state = MENU

    # Dibujar la pantalla según el estado del juego
    if game_state == MENU:
        draw_menu()
    elif game_state == CREDITS:
        draw_credits()
    elif game_state == PLAYING:
        draw_game()
    elif game_state == BATTLE:
        draw_battle()
    elif game_state == GAME_OVER:
        draw_game_over()
    elif game_state == VICTORY:

        draw_victory()
    elif game_state == FINAL_VICTORY:
        draw_final_victory()

    # Actualizar la pantalla
    pygame.display.flip()
    clock.tick(60)

# Detener toda la música antes de salir
pygame.mixer.music.stop()

# Salir del juego
pygame.quit()
sys.exit()
