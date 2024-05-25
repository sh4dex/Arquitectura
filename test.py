import pygame
import pygame.camera
import pytesseract
from PIL import Image

# Configuración de Tesseract
# Cambia la ruta según donde hayas instalado Tesseract
pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'

# Inicializar Pygame y la cámara
pygame.init()
pygame.camera.init()

# Configurar pantalla
screen_width = 640
screen_height = 480
text_area_height = 100
screen = pygame.display.set_mode((screen_width, screen_height + text_area_height))  # Espacio adicional para texto
pygame.display.set_caption('Reconocimiento de Texto en Tiempo Real')

# Detectar cámaras conectadas
cameras = pygame.camera.list_cameras()
if not cameras:
    raise ValueError("No se encontró ninguna cámara")

# Usar la primera cámara encontrada
cam = pygame.camera.Camera(cameras[0], (screen_width, screen_height))
cam.start()

# Fuente para mostrar texto en la pantalla
font = pygame.font.Font(None, 36)

running = True
while running:
    # Capturar imagen
    image = cam.get_image()

    # Convertir la imagen de Pygame a formato compatible con PIL
    image_str = pygame.image.tostring(image, 'RGB')
    pil_image = Image.frombytes('RGB', (screen_width, screen_height), image_str)

    # Realizar OCR
    extracted_text = pytesseract.image_to_string(pil_image)

    # Mostrar la imagen en pantalla
    screen.blit(image, (0, 0))

    # Limpiar la zona de texto
    pygame.draw.rect(screen, (0, 0, 0), (0, screen_height, screen_width, text_area_height))

    # Mostrar el texto reconocido
    y_offset = screen_height + 10
    for line in extracted_text.split('\n'):
        if line.strip():  # Evitar líneas vacías
            text_surface = font.render(line, True, (255, 255, 255))
            screen.blit(text_surface, (10, y_offset))
            y_offset += text_surface.get_height() + 5  # Añadir un poco de espacio entre líneas

    # Actualizar pantalla
    pygame.display.flip()

    # Manejar eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

# Limpiar recursos
cam.stop()
pygame.quit()

