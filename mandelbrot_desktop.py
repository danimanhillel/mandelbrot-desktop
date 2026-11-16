import pygame
import numpy as np
from numba import njit, prange
import colorsys
import sys

# Configuration
WIDTH, HEIGHT = 1200, 800
MAX_ITER_DEFAULT = 300

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Mandelbrot Explorer - Desktop")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 16)

@njit(parallel=True, fastmath=True)
def compute_mandelbrot(width, height, center_x, center_y, scale, max_iter, hue_shift, sat, val):
    img = np.zeros((height, width, 3), dtype=np.uint8)
    aspect = width / height
    for y in prange(height):
        cy = center_y + (y / height - 0.5) * scale
        for x in range(width):
            cx = center_x + (x / width - 0.5) * scale * aspect
            zx = 0.0
            zy = 0.0
            zx2 = 0.0
            zy2 = 0.0
            iter_count = 0
            for i in range(max_iter):
                if zx2 + zy2 > 4.0:
                    break
                zy = 2.0 * zx * zy + cy
                zx = zx2 - zy2 + cx
                zx2 = zx * zx
                zy2 = zy * zy
                iter_count = i
            if iter_count >= max_iter - 1:
                img[y, x] = (0, 0, 0)
            else:
                # Smooth coloring
                log_zn = np.log(zx2 + zy2) / 2.0
                nu = np.log(log_zn / np.log(2.0)) / np.log(2.0)
                smooth = iter_count + 1 - nu
                t = smooth / max_iter
                h = (t * 5.0 + hue_shift / 360.0) % 1.0
                r, g, b = colorsys.hsv_to_rgb(h, sat, val)
                img[y, x] = (int(r * 255), int(g * 255), int(b * 255))
    return img

def main():
    center_x = -0.75
    center_y = 0.0
    scale = 2.5
    max_iter = MAX_ITER_DEFAULT
    hue_shift = 0.0
    sat = 0.8
    val = 1.0
    scheme = 0  # not fully used yet, can expand

    dragging = False
    last_mouse = (0, 0)
    need_redraw = True

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.VIDEORESIZE:
                global WIDTH, HEIGHT
                WIDTH, HEIGHT = event.w, event.h
                screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
                need_redraw = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    dragging = True
                    last_mouse = event.pos
                elif event.button == 4:  # scroll up
                    scale *= 0.85
                    need_redraw = True
                elif event.button == 5:  # scroll down
                    scale *= 1.15
                    need_redraw = True
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    dragging = False
            elif event.type == pygame.MOUSEMOTION and dragging:
                dx = (event.pos[0] - last_mouse[0]) / WIDTH
                dy = (event.pos[1] - last_mouse[1]) / HEIGHT
                aspect = WIDTH / HEIGHT
                center_x -= dx * scale * aspect
                center_y += dy * scale
                last_mouse = event.pos
                need_redraw = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # reset
                    center_x, center_y, scale = -0.75, 0.0, 2.5
                    need_redraw = True
                elif event.key == pygame.K_UP:
                    max_iter = min(2000, max_iter + 50)
                    need_redraw = True
                elif event.key == pygame.K_DOWN:
                    max_iter = max(50, max_iter - 50)
                    need_redraw = True
                elif event.key == pygame.K_LEFT:
                    hue_shift = (hue_shift - 10) % 360
                    need_redraw = True
                elif event.key == pygame.K_RIGHT:
                    hue_shift = (hue_shift + 10) % 360
                    need_redraw = True
                elif event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:
                    sat = min(1.0, sat + 0.05)
                    need_redraw = True
                elif event.key == pygame.K_MINUS:
                    sat = max(0.0, sat - 0.05)
                    need_redraw = True

        if need_redraw:
            img = compute_mandelbrot(WIDTH, HEIGHT, center_x, center_y, scale, max_iter, hue_shift, sat, val)
            surface = pygame.surfarray.make_surface(np.transpose(img, (1, 0, 2)))
            screen.blit(surface, (0, 0))
            # Info overlay
            info = font.render(f"Zoom: {1/scale:.1f}x | Iter: {max_iter} | Hue: {int(hue_shift)} | Sat: {sat:.2f}", True, (255, 255, 255))
            screen.blit(info, (10, 10))
            pygame.display.flip()
            need_redraw = False

        clock.tick(60)

if __name__ == "__main__":
    main()
