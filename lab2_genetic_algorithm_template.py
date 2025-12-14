import math
import random
import pygame
from pygame.math import Vector2

# Window and visuals
WIDTH, HEIGHT = 800, 600
BG_COLOR = (30, 30, 30)
AMEBA_COLOR = (100, 255, 100, 150)
DEAD_COLOR = (255, 100, 100, 150)
FOOD_COLOR = (255, 200, 100)
TEXT_COLOR = (220, 220, 220)
VECTOR_LEN_PX = 60

# Genetic algorithm parameters
POPULATION_SIZE = 50
LIFESPAN = 400  # Number of frames in one generation
MUTATION_RATE = 0.01
ACTIVE_LEVEL = 0.1  # Force magnitude for each gene

# Obstacle parameters
NUM_OBSTACLES = 5
OBSTACLE_MIN_SIZE = 30
OBSTACLE_MAX_SIZE = 80


class DNA:
    def __init__(self, genes=None):
        self.active_level = ACTIVE_LEVEL
        self.genes = []
        
        if genes:
            self.genes = genes.copy()
        else:
            # Create new random genes
            for _ in range(LIFESPAN):
                # Create a random 2D vector
                angle = random.uniform(0, 2 * math.pi)
                gene = Vector2(math.cos(angle), math.sin(angle))
                gene.scale_to_length(self.active_level)
                self.genes.append(gene)

    def crossover(self, partner_dna):
        new_genes = []
        midpoint = len(self.genes)/2
        
        for i in range(len(self.genes)):
            if i < midpoint:
                new_genes.append(self.genes[i].copy())
            else:
                new_genes.append(partner_dna.genes[i].copy())

        return DNA(new_genes)
    
    def mutation(self):
        for i in range(len(self.genes)):
            if random.random() < MUTATION_RATE:
                angle = random.uniform(0, 2 * math.pi)
                self.genes[i] = Vector2(math.cos(angle), math.sin(angle))
                self.genes[i].scale_to_length(self.active_level)

class Ameba:
    def __init__(self, dna=None):
        self.pos = Vector2(WIDTH - 50, HEIGHT - 50)
        self.vel = Vector2()
        self.acc = Vector2()
        self.fitness = 0
        self.is_dead = False
        
        if dna:
            self.dna = dna
        else:
            self.dna = DNA()
    
    def apply_force(self, force):
        self.acc += force
    
    def update_state(self, food_pos, obstacles):
        # Calculate fitness based on distance to food
        d = self.pos.distance_to(food_pos)

        self.fitness = max(0,100 - d/4)

        if d < 16:
            self.fitness += 100
            self.die()
        
        # Penalty for hitting obstacles
        for obstacle in obstacles:
            if obstacle.rect.collidepoint(self.pos):
                self.fitness -= 50
                self.die()


    def die(self):
        self.is_dead = True

    
    def update(self, time):
        if not self.is_dead:
            # Apply the force from the gene at current time
            if time < len(self.dna.genes):
                self.apply_force(self.dna.genes[time])
            
            # Update physics
            self.vel += self.acc
            self.pos += self.vel
            self.acc.update(0, 0)
            
            # Keep on screen
            if self.pos.x < 0 or self.pos.x > WIDTH:
                self.vel.x *= -1
                self.pos.x = max(0, min(WIDTH, self.pos.x))
            if self.pos.y < 0 or self.pos.y > HEIGHT:
                self.vel.y *= -1
                self.pos.y = max(0, min(HEIGHT, self.pos.y))
    
    def draw(self, surface):
        # Draw the ameba as a rotated rectangle
        if not self.is_dead:
            color = AMEBA_COLOR
        else:
            color = DEAD_COLOR
        
        # Create a surface for the rectangle
        rect_surface = pygame.Surface((10, 3), pygame.SRCALPHA)
        rect_surface.fill(color)
        
        # Rotate based on velocity direction
        if self.vel.length_squared() > 0:
            angle = math.degrees(math.atan2(self.vel.y, self.vel.x))
        else:
            angle = 0
        
        rotated_rect = pygame.transform.rotate(rect_surface, -angle)
        rect_rect = rotated_rect.get_rect(center=(int(self.pos.x), int(self.pos.y)))
        
        surface.blit(rotated_rect, rect_rect)


class Obstacle:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
    
    def draw(self, surface):
        pygame.draw.rect(surface, (150, 50, 50), self.rect)


class Population:
    def __init__(self, size):
        self.population = []
        self.mating_pool = []
        self.generation = 0
        self.food_pos = Vector2(WIDTH // 2, HEIGHT // 2)
        
        # Create obstacles
        self.obstacles = self.create_obstacles()
        
        # Create initial population
        for _ in range(size):
            self.population.append(Ameba())
    
    def create_obstacles(self):
        obstacles = []
        
        # Add some random obstacles
        for _ in range(NUM_OBSTACLES):
            while True:
                width = random.randint(OBSTACLE_MIN_SIZE, OBSTACLE_MAX_SIZE)
                height = random.randint(OBSTACLE_MIN_SIZE, OBSTACLE_MAX_SIZE)
                x = random.randint(50, WIDTH - width - 50)
                y = random.randint(50, HEIGHT - height - 50)
                
                # Create obstacle
                new_obstacle = Obstacle(x, y, width, height)
                
                # Check if it overlaps with food or start position
                food_rect = pygame.Rect(self.food_pos.x - 16, self.food_pos.y - 16, 32, 32)
                start_rect = pygame.Rect(WIDTH - 60, HEIGHT - 60, 20, 20)
                
                if not new_obstacle.rect.colliderect(food_rect) and not new_obstacle.rect.colliderect(start_rect):
                    # Check if it overlaps with other obstacles
                    overlap = False
                    for obstacle in obstacles:
                        if new_obstacle.rect.colliderect(obstacle.rect):
                            overlap = True
                            break
                    
                    if not overlap:
                        obstacles.append(new_obstacle)
                        break
        
        return obstacles
    
    def run(self, time):
        # Update all amebas
        for ameba in self.population:
            ameba.update(time)
            ameba.update_state(self.food_pos, self.obstacles)
            

# --- START Genetic algorithm methods ----------------------------------

    def evaluate(self):
        max_fitness = 0
        for ameba in self.population:
            if ameba.fitness > max_fitness:
                max_fitness = ameba.fitness

        self.mating_pool = []
        for ameba in self.population:
            if max_fitness > 0:
                normalized_fitness = ameba.fitness/ max_fitness 
            else: 
                normalized_fitness = 0

            n = int(normalized_fitness * 100)
            for _ in range(n):
                self.mating_pool.append(ameba)
    
    def selection(self):
        # Create new generation
        new_population = []
        
        for _ in range(len(self.population)):
            if len(self.mating_pool) > 0:
                mother = random.choice(self.mating_pool)
                father = random.choice(self.mating_pool)

                child_dna = mother.dna.crossover(father.dna)
                child_dna.mutation()
                
                new_population.append(Ameba(child_dna))

            else:
                new_population.append(Ameba())
        
        self.population = new_population
        self.generation += 1
        
# --- END Genetic algorithm methods ----------------------------------
    
    def draw(self, surface):
        # Draw all amebas
        for ameba in self.population:
            ameba.draw(surface)
        
        # Draw obstacles
        for obstacle in self.obstacles:
            obstacle.draw(surface)
        
        # Draw food
        pygame.draw.circle(surface, FOOD_COLOR,
                          (int(self.food_pos.x), int(self.food_pos.y)), 16)


class App:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Lab2 - Genetic Algorithm")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 24)
        
        # Create population
        self.population = Population(POPULATION_SIZE)
        
        # Timing
        self.time = 0  # Current frame in generation
        self.running = True
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # Skip to next generation
                    self.time = LIFESPAN
    
    def update(self, dt_ms):
        # Update population
        self.population.run(self.time)
        
        # Increment time
        self.time += 1
        
        # Check if generation is complete
        if self.time >= LIFESPAN:
            # Evaluate and create new generation
            self.population.evaluate()
            self.population.selection()
            self.time = 0


    def draw(self):
        self.screen.fill(BG_COLOR)
        
        # Draw population
        self.population.draw(self.screen)
        
        # Draw UI text
        gen_text = self.font.render(f"Generation: {self.population.generation}", True, TEXT_COLOR)
        self.screen.blit(gen_text, (20, 20))
        
        time_text = self.font.render(f"Time: {self.time}/{LIFESPAN}", True, TEXT_COLOR)
        self.screen.blit(time_text, (20, 50))
        
        # Calculate average fitness
        avg_fitness = sum(ameba.fitness for ameba in self.population.population) / len(self.population.population)
        fitness_text = self.font.render(f"Avg Fitness: {avg_fitness:.2f}", True, TEXT_COLOR)
        self.screen.blit(fitness_text, (20, 80))
        
        # Instructions
        inst_text = self.font.render("Press SPACE to skip to next generation", True, TEXT_COLOR)
        self.screen.blit(inst_text, (20, HEIGHT - 30))
        
        pygame.display.flip()
    
    def run(self):
        while self.running:
            dt = self.clock.tick(60)
            self.handle_events()
            self.update(dt)
            self.draw()
        pygame.quit()


def main():
    App().run()


if __name__ == "__main__":
    main()