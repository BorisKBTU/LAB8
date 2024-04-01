import pygame

class DrawingApp:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((640, 480))
        self.clock = pygame.time.Clock()
        self.radius = 15
        self.mode = 'blue'
        self.colors = {'r': (255, 0, 0), 'g': (0, 255, 0), 'b': (0, 0, 255), 'y': (255, 255, 0)}
        self.points = []
        self.triangle = False
        self.circle = True
        self.rectangle = False

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.KEYDOWN:
                    self.handle_key_events(event.key)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_mouse_events(event.button)
                if event.type == pygame.MOUSEMOTION:
                    self.points.append(event.pos)
                    self.points = self.points[-256:]

            self.draw_frame()
            pygame.display.flip()
            self.clock.tick(60)

    def handle_key_events(self, key):
        if key == pygame.K_c:  # Clear points
            self.points.clear()
        elif key == pygame.K_t:  # Set drawing mode to triangle
            self.triangle = True
            self.circle = False
            self.rectangle = False
        elif key == pygame.K_o:  # Set drawing mode to circle
            self.circle = True
            self.triangle = False
            self.rectangle = False
        elif key == pygame.K_p:  # Set drawing mode to rectangle
            self.circle = False
            self.triangle = False
            self.rectangle = True
        elif key == pygame.K_r:  # Set drawing mode to red
            self.mode = 'red'
        elif key == pygame.K_g:  # Set drawing mode to green
            self.mode = 'green'
        elif key == pygame.K_b:  # Set drawing mode to blue
            self.mode = 'blue'
        elif key == pygame.K_y:  # Set drawing mode to yellow
            self.mode = 'yellow'

    def handle_mouse_events(self, button):
        key_unicode = pygame.key.name(button).lower()
        if key_unicode in self.colors:
            self.current_color = self.colors[key_unicode]
        if button == pygame.BUTTON_LEFT:
            self.radius = min(200, self.radius + 1)
        elif button == pygame.BUTTON_RIGHT:
            self.radius = max(1, self.radius - 1)

    def draw_frame(self):
        self.screen.fill((0, 0, 0))

        i = 0
        while i < len(self.points) - 1:
            self.draw_line_between(i, self.points[i], self.points[i + 1])
            i += 1

    def draw_line_between(self, index, start, end):
        color = self.calculate_color(index)

        dx = start[0] - end[0]
        dy = start[1] - end[1]
        iterations = max(abs(dx), abs(dy))

        for i in range(iterations):
            progress = 1.0 * i / iterations
            aprogress = 1 - progress
            x = int(aprogress * start[0] + progress * end[0])
            y = int(aprogress * start[1] + progress * end[1])
            if self.circle:
                pygame.draw.circle(self.screen, color, (x, y), self.radius)
            elif self.triangle:
                vertices = [(x, y), (x + self.radius, y + self.radius), (x - self.radius, y + self.radius)]
                pygame.draw.polygon(self.screen, color, vertices)
            elif self.rectangle:
                rect_width = 5
                rect_x, rect_y = x - 50, y - 37.5
                rect_size = (100, 75)
                pygame.draw.rect(self.screen, color, pygame.Rect(rect_x, rect_y, rect_size[0], rect_size[1]))
                pygame.draw.rect(self.screen, color, pygame.Rect(rect_x, rect_y, rect_size[0], rect_size[1]),
                                 rect_width)
    def calculate_color(self, index):

        if self.mode == 'blue':
            return self.colors['b']
        elif self.mode == 'red':
            return self.colors['r']
        elif self.mode == 'green':
            return self.colors['g']
        elif self.mode == 'yellow':
            return self.colors['y']
if __name__ == "__main__":
    app = DrawingApp()
    app.run()
