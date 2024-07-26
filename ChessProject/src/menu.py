import pygame
import os
from const import WIDTH, HEIGHT

class Menu:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Шатар')
        self.set_fonts()
        self.set_background_image()
        self.selected_option = 0

    def set_fonts(self):
        self.font = pygame.font.SysFont('Cascadia Mono', 50, bold=True)
        self.highlight_font = pygame.font.SysFont('Cascadia Mono', 60, bold=True, italic=True)
        self.instructions_font = pygame.font.SysFont('Times New Roman', 30, bold=True)

    def set_background_image(self):
        self.background_image = pygame.image.load(
            os.path.join('assets', 'images', 'BACKGROUND.jpg')
        )
        self.background_image = pygame.transform.scale(
            self.background_image, (WIDTH, HEIGHT)
        )

    def draw_menu(self):
        self.screen.blit(self.background_image, (0, 0))

        options = ['1 тоглогч', '2 тоглогч', 'Заавар', 'Гарах']
        for index, option in enumerate(options):
            if self.selected_option == index:
                highlight_rect = pygame.Rect(
                    WIDTH // 2 - 80,
                    HEIGHT // 2 + index * 40 - 20,
                    160,  # Width
                    40  # Height
                )
                pygame.draw.rect(self.screen, (72, 99, 160), highlight_rect)  

                option_text = self.highlight_font.render(option, True, (255, 255, 255))
            else:
                option_text = self.font.render(option, True, (255, 255, 255))

            option_rect = option_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + index * 40))
            self.screen.blit(option_text, option_rect)

    def draw_instructions(self):
        self.screen.fill((72, 99, 160)) 

        instructions = [
            "1. Main.py - аас эхлүүлнэ.",
            "2. 3 / 4 дээр дарснаар өрсөлдөгч компьютерийн ",
            "тоглолтыг тохируулах боломжтой.",
            "3. t дээр дарж шатрын хөлгийн өнгийг ",
            "өөрчлөх боломжтой.",
            "4. r дарж дахин эхлүүлнэ.",
            "",
            "ESC дарж меню-рүү буцна уу."
        ]

        y_offset = HEIGHT // 4
        for line in instructions:
            text = self.instructions_font.render(line, True, (255, 255, 255))
            text_rect = text.get_rect(center=(WIDTH // 2, y_offset))
            self.screen.blit(text, text_rect)
            y_offset += 45

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_option = (self.selected_option - 1) % 4
            elif event.key == pygame.K_DOWN:
                self.selected_option = (self.selected_option + 1) % 4
            elif event.key == pygame.K_RETURN:
                if self.selected_option == 3:  
                    pygame.quit()
                    quit()
                elif self.selected_option == 2:
                    self.show_instructions = True
                else:
                    return self.selected_option

            elif event.key == pygame.K_ESCAPE and hasattr(self, 'show_instructions') and self.show_instructions:
                self.show_instructions = False

    def run(self):
        self.show_instructions = False
        running = True
        while running:
            if self.show_instructions:
                self.draw_instructions()
            else:
                self.draw_menu()

            for event in pygame.event.get():
                option = self.handle_event(event)
                if option is not None and not self.show_instructions:
                    return option

            pygame.display.flip()
