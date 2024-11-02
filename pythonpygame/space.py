import pygame
pygame.font.init()
pygame.mixer.init()

# Set up the display
WIDTH,HEIGHT  = 900,500
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('Poorna Games....!!')

black = (0,51,102)
color = (13,24,15)
white = (255,255,51)
dark=(255,102,102)

FPS = 60
velocity = 5
bullet_vel = 7
max_bullet = 3

yellow_hit = pygame.USEREVENT +1
red_hit = pygame.USEREVENT + 2

border = pygame.Rect(WIDTH//2-5,0,10,HEIGHT) #(X,Y,WIDTH,HEIGHT)

bullet_hit_sound = pygame.mixer.Sound(r"C:\Users\Poornatejas\OneDrive\Desktop\pythonpygame\file testing\Gun+Silencer.mp3")
bullet_fire_sound = pygame.mixer.Sound(r"C:\Users\Poornatejas\OneDrive\Desktop\pythonpygame\file testing\Gun+Silencer.mp3")

health_font = pygame.font.SysFont('comicsans',40)
winner_font = pygame.font.SysFont('comicsans',100)

Spaceship_Weidth,Spaceship_Height = 55,40

Yellow_spaceship_image = pygame.image.load(r"C:\Users\Poornatejas\OneDrive\Desktop\pythonpygame\file testing\spaceship_yellow.png")
yellow_spaceship = pygame.transform.rotate(pygame.transform.scale(Yellow_spaceship_image,(Spaceship_Weidth,Spaceship_Height)),90) # reduceing the size of the image

Red_spaceship_image = pygame.image.load(r"C:\Users\Poornatejas\OneDrive\Desktop\pythonpygame\file testing\spaceship_red.png")
Red_spaceship = pygame.transform.rotate(pygame.transform.scale(Red_spaceship_image,(Spaceship_Weidth,Spaceship_Height)),270)

space = pygame.transform.scale(pygame.image.load(r"C:\Users\Poornatejas\OneDrive\Desktop\pythonpygame\file testing\space.png"),(WIDTH,HEIGHT))

def color_window(red,yellow,red_bullet,yellow_bullet,red_health,yellow_health):
    WIN.blit(space,(0,0))
    pygame.draw.rect(WIN,black,border)
    
    red_health  = health_font.render('Health : ' + str(red_health),1,white)
    yellow_health  = health_font.render('Health : ' + str(yellow_health),1,dark)
    WIN.blit(red_health,(WIDTH-red_health.get_width()-10,10))
    WIN.blit(yellow_health,(0,10))
    WIN.blit(yellow_spaceship,(yellow.x,yellow.y))  # To display the image on the screen
    WIN.blit(Red_spaceship,(red.x,red.y))
    
    for bullet in red_bullet:
        pygame.draw.rect(WIN,white,bullet)

    
    for bullet in yellow_bullet:
        pygame.draw.rect(WIN,dark,bullet)

    pygame.display.update()

def yellow_movement(key_pressed,yellow):

    if key_pressed[pygame.K_a] and yellow.x-velocity > 0 :
            yellow.x -= velocity

    if key_pressed[pygame.K_d] and yellow.x + velocity +yellow.width< border.x:
            yellow.x += velocity

    if key_pressed[pygame.K_w] and yellow.y - velocity > 0 :
            yellow.y -= velocity

    if key_pressed[pygame.K_s] and yellow.y + velocity + yellow.height < HEIGHT-15:
            yellow.y += velocity

def red_movement(key_pressed,red):

    if key_pressed[pygame.K_LEFT] and red.x-velocity > border.x+border.width :
            red.x -= velocity

    if key_pressed[pygame.K_RIGHT] and red.x + velocity +red.width< WIDTH:
            red.x += velocity

    if key_pressed[pygame.K_UP] and red.y - velocity > 0 :
            red.y -= velocity

    if key_pressed[pygame.K_DOWN] and red .y + velocity + red.height < HEIGHT-15 :
            red.y += velocity

def handle_bullets(yellow_bullet,red_bullet,yellow,red):
        for bullet in yellow_bullet:
                bullet.x+=bullet_vel

                if red.colliderect(bullet):
                        pygame.event.post(pygame.event.Event(red_hit))
                        yellow_bullet.remove(bullet)
                        
                elif bullet.x > WIDTH:
                        yellow_bullet.remove(bullet)

        for bullet in red_bullet:
                bullet.x -=bullet_vel

                if yellow.colliderect(bullet):
                        pygame.event.post(pygame.event.Event(yellow_hit))
                        red_bullet.remove(bullet)

                elif bullet.x < 0:
                        red_bullet.remove(bullet)

def winner(text):
      draw_text = winner_font.render(text,1,white)
      WIN.blit(draw_text,(WIDTH/2-draw_text.get_width()/2,
                          HEIGHT/2-draw_text.get_height()/2))
      pygame.display.update()
      pygame.time.wait(5000)
        
def main():

    red = pygame.Rect(700,300,Spaceship_Weidth,Spaceship_Height)
    yellow = pygame.Rect(100,300,Spaceship_Weidth,Spaceship_Height)
    
    clock = pygame.time.Clock() # Frame per Second
    run = True
    yellow_bullet= []
    red_bullet = []
    red_health = 10
    yellow_health = 10

    while run:
        clock.tick(FPS)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullet) < max_bullet:
                        bullet = pygame.Rect(yellow.x+yellow.width,yellow.y+yellow.height//2-2,10,5)
                        yellow_bullet.append(bullet)
                        bullet_fire_sound.play()

                if event.key == pygame.K_RCTRL and  len(red_bullet) < max_bullet :
                        bullet = pygame.Rect(red.x,red.y+red.height//2-2,10,5)
                        red_bullet.append(bullet)
                        bullet_fire_sound.play()

            if event.type == red_hit:
                        red_health -= 1
                        bullet_hit_sound.play()

            if event.type == yellow_hit:
                        yellow_health -= 1
                        bullet_hit_sound.play()

        winner_Text = ''
        if red_health<=0:
              winner_Text = 'Yellow Wins..!!'
        
        if yellow_health<=0:
              winner_Text = 'Red Wins...!!'

        if winner_Text != '':
              winner(winner_Text)
              break


        key_pressed = pygame.key.get_pressed()
        yellow_movement(key_pressed,yellow)
        red_movement(key_pressed,red)
        
        handle_bullets(yellow_bullet,red_bullet,yellow,red)

        color_window(red,yellow,red_bullet,yellow_bullet,red_health,yellow_health)        
    
    pygame.quit()

if __name__ == '__main__':
    main()