
import pygame
import sys
import webbrowser

def main():
	pygame.init()
	SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
	screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
	pygame.display.set_caption("Sobre o Jogo")

	paragrafos = [
		"Este jogo foi desenvolvido como trabalho do curso de Ciência da Computação da Universidade Estadual de Maringá.",
		"O objetivo principal é o aprendizado sobre arquiteturas cliente-servidor na disciplina de Sistemas Distribuídos.",
		"Para fins pedagógicos, criamos um jogo que faz referência ao clássico 'Pac-Man', usando personagens do universo 'Bleach' como inspiração.",
		"Todos os direitos dos personagens pertencem aos seus respectivos autores; este projeto é apenas para fins educacionais e acadêmicos.",
		"Equipe: Marcos Vinicius Barros Petronilo, Maykon Passos Lavezo e Pedro Yoshio."
	]

	title_font = pygame.font.Font(pygame.font.match_font('arial'), 44)
	subtitle_font = pygame.font.Font(pygame.font.match_font('arial'), 26)
	body_font = pygame.font.Font(pygame.font.match_font('arial'), 20)
	small_font = pygame.font.Font(pygame.font.match_font('arial'), 16)

	# Pré-render das linhas para facilitar scroll
	lines = []
	line_spacing = 6
	for p in paragrafos:
		# quebra simples por tamanho aproximado
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
		# linha em branco entre parágrafos
		lines.append(body_font.render('', True, (40, 40, 40)))

	# estado do scroll
	offset_y = 0
	# altura total do conteúdo
	content_height = sum(s.get_height() + line_spacing for s in lines) + 200

	clock = pygame.time.Clock()
	running = True
	while running:
		screen.fill((250, 250, 252))

		# Cabeçalho
		title = title_font.render("Sobre o Projeto", True, (24, 24, 24))
		title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 50))
		screen.blit(title, title_rect)

		subtitle = subtitle_font.render("Trabalho acadêmico - Sistemas Distribuídos", True, (80, 80, 80))
		screen.blit(subtitle, subtitle.get_rect(center=(SCREEN_WIDTH // 2, 100)))

		# Desenha conteúdo com offset (scroll)
		y = 140 + offset_y
		left_margin = 60
		for surf in lines:
			rect = surf.get_rect(topleft=(left_margin, y))
			screen.blit(surf, rect)
			y += surf.get_height() + line_spacing

		# Rodapé com botões
		# Botão Voltar
		btn_w = 140
		btn_h = 40
		voltar_rect = pygame.Rect(40, SCREEN_HEIGHT - 60, btn_w, btn_h)
		visitar_rect = pygame.Rect(SCREEN_WIDTH - btn_w - 40, SCREEN_HEIGHT - 60, btn_w, btn_h)

		mx, my = pygame.mouse.get_pos()
		hover_voltar = voltar_rect.collidepoint((mx, my))
		hover_visitar = visitar_rect.collidepoint((mx, my))

		pygame.draw.rect(screen, (255, 255, 255), voltar_rect, border_radius=8)
		pygame.draw.rect(screen, (200, 200, 200), voltar_rect, width=2, border_radius=8)
		pygame.draw.rect(screen, (255, 255, 255), visitar_rect, border_radius=8)
		pygame.draw.rect(screen, (200, 200, 200), visitar_rect, width=2, border_radius=8)

		voltar_txt = small_font.render("Voltar", True, (10, 10, 10) if not hover_voltar else (0,0,0))
		visitar_txt = small_font.render("Visitar UEM", True, (10, 10, 10) if not hover_visitar else (0,0,0))
		screen.blit(voltar_txt, voltar_txt.get_rect(center=voltar_rect.center))
		screen.blit(visitar_txt, visitar_txt.get_rect(center=visitar_rect.center))

		# eventos
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			elif event.type == pygame.KEYDOWN:
				if event.key in (pygame.K_ESCAPE, pygame.K_RETURN, pygame.K_SPACE):
					running = False
					try:
						import tela_menu
						tela_menu.main()
					except Exception as e:
						print('Erro ao retornar para o menu:', e)
				elif event.key == pygame.K_UP:
					offset_y = min(offset_y + 40, 0)
				elif event.key == pygame.K_DOWN:
					max_offset = min(0, SCREEN_HEIGHT - content_height)
					offset_y = max(offset_y - 40, max_offset)
			elif event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == 1:  # clique esquerdo
					if hover_voltar:
						running = False
						try:
							import tela_menu
							tela_menu.main()
						except Exception as e:
							print('Erro ao retornar para o menu:', e)
					elif hover_visitar:
						try:
							webbrowser.open('https://www.uem.br')
						except Exception as e:
							print('Erro ao abrir navegador:', e)
				elif event.button == 4:  # roda p/ cima
					offset_y = min(offset_y + 30, 0)
				elif event.button == 5:  # roda p/ baixo
					max_offset = min(0, SCREEN_HEIGHT - content_height)
					offset_y = max(offset_y - 30, max_offset)

		pygame.display.flip()
		clock.tick(60)

	pygame.quit()


if __name__ == '__main__':
	main()
