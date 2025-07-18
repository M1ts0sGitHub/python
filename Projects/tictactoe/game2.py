import pygame
import ctypes
from ctypes import wintypes

# Αρχικοποίηση Pygame
pygame.init()

# Δημιουργία frameless παραθύρου
screen = pygame.display.set_mode((400, 300), pygame.NOFRAME)

# Παίρνουμε το HWND του παραθύρου
hwnd = pygame.display.get_wm_info()['window']

# Win32 API calls για layered window και οβάλ σχήμα
user32 = ctypes.windll.user32
gdi32 = ctypes.windll.gdi32

# Ορισμός layered window (για διαφάνεια)
WS_EX_LAYERED = 0x80000
GWL_EXSTYLE = -20
LWA_COLORKEY = 1

# Προσθήκη extended style για layered window
style = user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
user32.SetWindowLongW(hwnd, GWL_EXSTYLE, style | WS_EX_LAYERED)

# Ορισμός χρώματος που θα είναι διαφανές (π.χ. μαύρο)
user32.SetLayeredWindowAttributes(hwnd, 0x000000, 0, LWA_COLORKEY)

# # Δημιουργία οβάλ region
# hrgn = gdi32.CreateEllipticRgn(0, 0, 400, 300)
# user32.SetWindowRgn(hwnd, hrgn, True)

running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))  # Μαύρο χρώμα (θα είναι διαφανές)
    pygame.draw.rect(screen, (250, 20, 20), (0, 0, 400, 300), border_radius=15)  # Στρογγυλό.rect στο παράθυρο
    # img = pygame.image.load('c:/temp.jpg')
    # rect = img.get_rect()
    # rect.center = (200, 150)
    # screen.blit(img, rect)
    pygame.display.update()
    clock.tick(60)

pygame.quit()
