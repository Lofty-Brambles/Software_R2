import pygame
from typing import Any
from prantik_das.runners import all_runners

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY_BG = (32, 32, 32)
DARK_BLUE = (0, 100, 250)


class Menu:

    def __init__(self, screen: pygame.Surface, url: str):
        self.screen = screen
        self.server_url = url
        menu = pygame.Rect((1280 - 320 - 24, 24, 320, 720 - 48))
        pygame.draw.rect(self.screen, GRAY_BG, menu, border_radius=15)

        self.buttons: list[tuple[pygame.Rect, Any]] = []
        px = lambda x: (1280 - 320, 48 + x * 48, 320 - 48, 40)
        tx = lambda x: x.capitalize() + " runner"
        for i, x in enumerate(all_runners.items()):
            self.buttons.append(
                self._button_create(
                    tx(x[0]), px(i), DARK_BLUE, self._attach_runner_wrapper()
                )
            )

    def _button_create(
        self, text: str, rect: tuple[int, int, int, int], color: pygame.Color, action
    ):
        button_rect = pygame.Rect(rect)
        pygame.draw.rect(self.screen, color, button_rect, border_radius=15)

        text = pygame.font.Font(None, 32).render(text, True, WHITE)
        text_rect = text.get_rect(center=button_rect.center)
        self.screen.blit(text, text_rect)

        return button_rect, action

    def _attach_runner_wrapper(p):
        return p


class Windows:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.sublets = map(self._init_window, range(6))

    def _init_window(self, number: int):
        border_rect = pygame.Rect((52 + 140 * number, 24, 136, 632))
        rect = pygame.Rect((64 + 140 * number, 36, 112, 608))
        pygame.draw.rect(self.screen, WHITE, border_rect)
        pygame.draw.rect(self.screen, BLACK, rect)

        text = pygame.font.Font(None, 32).render(number + 1, True, WHITE)
        text_rect = text.get_rect(center=(rect.center[0] + 336, rect.center[1]))
        self.screen.blit(text, text_rect)

        return (rect,)
