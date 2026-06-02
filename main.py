
import pygame
import random
import sys
import time
import algorithms  

pygame.init()
pygame.font.init()

WIDTH, HEIGHT = 1000, 700
ARRAY_SIZE = 120


BG_COLOR = (15, 16, 26)       
BAR_DEFAULT = (0, 184, 148)     
BAR_ACTIVE = (255, 118, 117)    
BAR_SORTED = (108, 92, 231)     
UI_PANEL_COLOR = (27, 28, 43)   
TEXT_COLOR = (224, 224, 224)    


FONT_UI = pygame.font.SysFont("Consolas", 16, bold=True)
FONT_LOGO = pygame.font.SysFont("Impact", 28)

class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.vx = random.uniform(-3, 3)
        self.vy = random.uniform(-5, -1)
        self.radius = random.randint(2, 5)
        self.lifetime = 255
        self.color = color

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.lifetime -= 15   

    def draw(self, surface):
        if self.lifetime > 0:
            s = pygame.Surface((self.radius*2, self.radius*2), pygame.SRCALPHA)
            pygame.draw.circle(s, (*self.color, self.lifetime), (self.radius, self.radius), self.radius)
            surface.blit(s, (self.x - self.radius, self.y - self.radius))

def draw_dashboard(screen, algo_name, comparisons, swaps, elapsed_time):
    pygame.draw.rect(screen, UI_PANEL_COLOR, (0, 0, WIDTH, 80))
    pygame.draw.line(screen, (45, 52, 80), (0, 80), (WIDTH, 80), 2)  

    title_surf = FONT_LOGO.render("SORT_ENGINE //", True, BAR_DEFAULT)
    screen.blit(title_surf, (20, 22))

    stats = [
        f"ALGORITHM: {algo_name.upper()}",
        f"COMPARISONS: {comparisons}",
        f"SWAPS: {swaps}",
        f"TIME: {elapsed_time:.2f}s"
    ]

    x_offset = 300
    for stat in stats:
        text_surf = FONT_UI.render(stat, True, TEXT_COLOR)
        screen.blit(text_surf, (x_offset, 32))
        x_offset += 180

def draw_bars(screen, data, colors):
    graph_y_start = 100
    graph_height = HEIGHT - graph_y_start - 20
    bar_width = WIDTH / len(data)
    max_val = max(data) if data else 1

    for i, val in enumerate(data):
        normalized_h = (val / max_val) * graph_height
        
        x = i * bar_width
        y = HEIGHT - normalized_h - 20
        w = bar_width - 1
        h = normalized_h

        pygame.draw.rect(screen, colors[i], (x, y, w, h))
        
        if colors[i] == BAR_ACTIVE:
            pygame.draw.rect(screen, (255, 255, 255), (x, y, w, 3))

def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("⚡ Cyberpunk Sorting Visualizer")
    clock = pygame.time.Clock()

  
    algo_name = "Bubble Sort"
    
    
    data = [random.randint(10, 500) for _ in range(ARRAY_SIZE)]
    

    sorting_generator = algorithms.bubble_sort(data)

   
    running = True
    sorting = True
    comparisons = 0
    swaps = 0
    start_time = time.time()
    elapsed_time = 0.0
    particles = []
    prev_data = list(data)

    while running:
     
        clock.tick(120) 
      
        screen.fill(BG_COLOR)

       
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

        if sorting:
            elapsed_time = time.time() - start_time
            try:
               
                current_state, red_a, red_b, _, _ = next(sorting_generator)
                comparisons += 1
                
                
                if current_state != prev_data:
                    swaps += 1
                    if red_a != -1:
                       
                        bar_width = WIDTH / ARRAY_SIZE
                        px = red_a * bar_width
                        py = HEIGHT - current_state[red_a] - 20
                        for _ in range(5):
                            particles.append(Particle(px, py, BAR_ACTIVE))
                
                prev_data = list(current_state)

                
                colors = []
                for idx in range(len(current_state)):
                    if idx == red_a or idx == red_b:
                        colors.append(BAR_ACTIVE)
                    else:
                        colors.append(BAR_DEFAULT)

                draw_bars(screen, current_state, colors)

            except StopIteration:
                sorting = False
        else:
        
            draw_bars(screen, data, [BAR_SORTED for _ in range(ARRAY_SIZE)])

        
        for particle in particles[:]:
            particle.update()
            particle.draw(screen)
            if particle.lifetime <= 0:
                particles.remove(particle)

        
        draw_dashboard(screen, algo_name, comparisons, swaps, elapsed_time)
        
        pygame.display.flip()

if __name__ == "__main__":
    main()