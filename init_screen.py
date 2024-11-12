import pygame 
pygame.init() 
# CREATING CANVAS 
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
# TITLE OF CANVAS 
pygame.display.set_caption("My Board") 
WHITE = (255, 255, 255)
exit = False
while not exit: 
	#starting of start screen
	screen.fill(WHITE)
	font = pygame.font.SysFont(None, 48)
	text = font.render("Press any key to start", True, (0, 0, 0))
	screen.blit(text, (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2))
	pygame.display.flip()
	#end of start screen code
	for event in pygame.event.get(): 
		if event.type == pygame.QUIT: 
			exit = True
	
	pygame.display.update() 
	
