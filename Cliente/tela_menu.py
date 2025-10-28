import os
import pygame


def main():
    # --- Configurações Iniciais ---
    pygame.init()

    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("THE HOLLOW CHASE")

    # Cores
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GRAY = (150, 150, 150)
    HIGHLIGHT_COLOR = (0, 0, 0)

    # Fonte
    try:
        menu_font = pygame.font.Font(pygame.font.match_font('arial'), 40)
        title_font = pygame.font.Font(pygame.font.match_font('arial'), 70)
    except Exception:
        menu_font = pygame.font.Font(None, 50)
        title_font = pygame.font.Font(None, 80)

    # --- Carrega a Imagem de Fundo ---
    # procura por background.png/jpg na mesma pasta do arquivo ou assets
    base_dir = os.path.dirname(__file__)
    candidates = [
        os.path.join(base_dir, 'background1.png'),
        os.path.join(base_dir, 'background1.jpg'),
        os.path.join(base_dir, '..', 'Assets', 'background1.png'),
        os.path.join(base_dir, '..', 'Assets', 'background1.jpg'),
        os.path.join(base_dir, '..', 'Assets', 'background1.png'),
        os.path.join(base_dir, '..', 'Assets', 'background1.jpg'),
    ]
    background_image = None
    for p in candidates:
        if os.path.isfile(p):
            try:
                background_image = pygame.image.load(p).convert()
                background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
                break
            except Exception as e:
                print(f"Erro ao carregar {p}: {e}")
                background_image = None

    if background_image is None:
        print("[tela_menu] nenhum background encontrado; usando fundo preto")

    # --- Opções do Menu ---
    menu_options = ["Iniciar jogo", "Ajuda", "Sobre", "Sair"]
    selected_option = 0

    # --- Funções Auxiliares ---
    def draw_text(text, font, color, surface, x, y):
        textobj = font.render(text, True, color)
        textrect = textobj.get_rect(center=(x, y))
        surface.blit(textobj, textrect)

    # --- Loop Principal do Menu ---
    running = True
    clock = pygame.time.Clock()
    while running:
        # --- Desenha o Fundo ---
        if background_image:
            screen.blit(background_image, (0, 0))
        else:
            screen.fill(BLACK)

        # Desenha o Título
        draw_text("THE HOLLOW CHASE", title_font, WHITE, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4)

        # Desenha as opções em horizontal
        total_width = 0
        option_surfs = []
        spacing = 60  # espaçamento entre opções
        for i, option in enumerate(menu_options):
            color = HIGHLIGHT_COLOR if i == selected_option else GRAY
            surf = menu_font.render(option, True, color)
            option_surfs.append(surf)
            total_width += surf.get_width()
        total_width += spacing * (len(menu_options) - 1)

        # Posição inicial para centralizar
        start_x = (SCREEN_WIDTH - total_width) // 2
        y_pos = SCREEN_HEIGHT // 2
        y_pos = int(SCREEN_HEIGHT * 0.65)

        # Desenha cada opção
        x = start_x
        for surf in option_surfs:
            rect = surf.get_rect(midtop=(x + surf.get_width() // 2, y_pos))
            screen.blit(surf, rect)
            x += surf.get_width() + spacing

        # --- Tratamento de Eventos ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    selected_option = (selected_option - 1) % len(menu_options)
                elif event.key == pygame.K_RIGHT:
                    selected_option = (selected_option + 1) % len(menu_options)
                elif event.key == pygame.K_RETURN:
                    option_text = menu_options[selected_option]
                    print(f"Opção selecionada: {option_text}")
                    if option_text == "Iniciar jogo":
                        print("Iniciando o jogo...")
                        running = False
                    elif option_text == "Ajuda":
                        print("Mostrando Ajuda...")
                    elif option_text == "Sobre":
                        try:
                            import sobre
                            sobre.main()
                        except Exception as e:
                            print("Erro ao abrir página Sobre:", e)
                    elif option_text == "Sair":
                        running = False

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    return


if __name__ == '__main__':
    main()