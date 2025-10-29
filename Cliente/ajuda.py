# Nome do arquivo: cliente/ajuda.py
# (Versão com correção de scroll)

import pygame
import sys
import importlib

def main():
	pygame.init()
	SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
	screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
	pygame.display.set_caption("Ajuda - Como Jogar")

	# Textos da ajuda baseados na especificação e slides
	paragrafos = [
		"Bem-vindo ao THE HOLLOW CHASE!",
		"O seu objetivo é guiar o personagem (Ichigo) pelo labirinto e coletar todas as 'Bolinhas de Pontuação' para passar de nível.",
		"CONTROLES:",
		"Use as TECLAS SETA (Cima, Baixo, Esquerda, Direita) ou as teclas 'W', 'A', 'S', 'D' para se movimentar.",
		"Pressione 'ESC' para pausar o jogo ou voltar ao menu.",
		"VILÕES (HOLLOWS):",
		"Evite tocar nos 'Hollows' que patrulham o labirinto. Se eles o pegarem, você perde uma vida.",
		"O jogo termina quando você perder todas as suas vidas.",
		"ITENS ESPECIAIS:",
		"- Item de Transformação (Energizador): Ao coletar este item, você pode 'atacar' os Hollows por um curto período para ganhar pontos extras.",
		"- Itens de Ponto Extra (Bônus): Aparecem aleatoriamente no mapa e concedem pontos bônus.",
        "",
        "Este jogo foi desenvolvido para a disciplina de Sistemas Distribuídos.",
        "Aproveite!"
	]

	title_font = pygame.font.Font(pygame.font.match_font('arial'), 44)
	subtitle_font = pygame.font.Font(pygame.font.match_font('arial'), 26)
	body_font = pygame.font.Font(pygame.font.match_font('arial'), 20)
	small_font = pygame.font.Font(pygame.font.match_font('arial'), 16)

	# --- Pré-render das linhas (sem alteração) ---
	lines = []
	line_spacing = 8
	for p in paragrafos:
		words = p.split(' ')
		cur = ''
		for w in words:
			test = f"{cur} {w}".strip()
			surf = body_font.render(test, True, (40, 40, 40))
			if surf.get_width() > SCREEN_WIDTH - 120:
				lines.append(body_font.render(cur, True, (40, 40, 40)))
				cur = w
			else:
				cur = test
		if cur:
			lines.append(body_font.render(cur, True, (40, 40, 40)))
		lines.append(body_font.render('', True, (40, 40, 40)))

	# estado do scroll
	offset_y = 0
	# altura total do conteúdo
	content_height = sum(s.get_height() + line_spacing for s in lines)

	clock = pygame.time.Clock()
	running = True
	while running:
        # --- 1. Pinta o fundo ---
		screen.fill((250, 250, 252)) # Fundo claro

		# --- 2. Desenha o Cabeçalho FIXO ---
		title = title_font.render("Como Jogar", True, (24, 24, 24))
		title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 50))
		screen.blit(title, title_rect)

		subtitle = subtitle_font.render("Objetivos e Controles", True, (80, 80, 80))
		screen.blit(subtitle, subtitle.get_rect(center=(SCREEN_WIDTH // 2, 100)))

		# --- 3. Desenha o Rodapé FIXO ---
		btn_w = 140
		btn_h = 40
		voltar_rect = pygame.Rect((SCREEN_WIDTH - btn_w) // 2, SCREEN_HEIGHT - 60, btn_w, btn_h)

		mx, my = pygame.mouse.get_pos()
		hover_voltar = voltar_rect.collidepoint((mx, my))

		pygame.draw.rect(screen, (255, 255, 255), voltar_rect, border_radius=8)
		pygame.draw.rect(screen, (200, 200, 200), voltar_rect, width=2, border_radius=8)
		
		voltar_txt_color = (0,0,0) if hover_voltar else (10, 10, 10)
		voltar_txt = small_font.render("Voltar", True, voltar_txt_color)
		screen.blit(voltar_txt, voltar_txt.get_rect(center=voltar_rect.center))


        # --- 4. Define a Área de Scroll ---
        # Começa abaixo do cabeçalho (140) e termina acima do rodapé (SCREEN_HEIGHT - 70)
		scroll_area_y_start = 140
		scroll_area_height = (SCREEN_HEIGHT - 70) - scroll_area_y_start
		scroll_area_rect = pygame.Rect(0, scroll_area_y_start, SCREEN_WIDTH, scroll_area_height)

        # Cria a sub-superfície (a "janela" de conteúdo)
		content_surface = screen.subsurface(scroll_area_rect)
        # Limpa APENAS a área de conteúdo (isso é importante para apagar o frame anterior)
		content_surface.fill((250, 250, 252))


		# --- 5. Desenha o conteúdo rolável DENTRO da "janela" ---
		y = 0 + offset_y # Y agora é relativo à 'content_surface'
		left_margin = 60
		for surf in lines:
			rect = surf.get_rect(topleft=(left_margin, y))
			content_surface.blit(surf, rect) # Blit na content_surface, não na screen
			y += surf.get_height() + line_spacing

		# --- Eventos (sem alteração, exceto limites do scroll) ---
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			elif event.type == pygame.KEYDOWN:
				if event.key in (pygame.K_ESCAPE, pygame.K_RETURN, pygame.K_SPACE):
					running = False # Sai do loop para voltar ao menu
				elif event.key == pygame.K_UP:
					offset_y = min(offset_y + 40, 0) # Limite superior é 0
				elif event.key == pygame.K_DOWN:
                    # Limite inferior (não deixa rolar para baixo mais que o necessário)
					max_offset = min(0, scroll_area_height - content_height)
					offset_y = max(offset_y - 40, max_offset)
			elif event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == 1:
					if hover_voltar:
						running = False
				elif event.button == 4:  # roda p/ cima
					offset_y = min(offset_y + 30, 0)
				elif event.button == 5:  # roda p/ baixo
					max_offset = min(0, scroll_area_height - content_height)
					offset_y = max(offset_y - 30, max_offset)

		pygame.display.flip() # Atualiza a tela inteira
		clock.tick(60)

	# --- Loop de retorno ao menu (sem alteração) ---
	try:
		import tela_menu
		importlib.reload(tela_menu)
		tela_menu.main()
	except Exception as e:
		print('Erro ao retornar para o menu:', e)
		pygame.quit()
		sys.exit()


if __name__ == '__main__':
	main()