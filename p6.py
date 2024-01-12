import pygame,os
from pygame.locals import*
from tkinter import*

a=Tk()

running=False

a.geometry("650x400+350+150")

a.maxsize(650,400)

a.minsize(650,400)

a.configure(background="gray")

opcion_seleccionada = IntVar()

f=Frame()

f.grid(row=0)

f1=Frame()

f1.grid(row=1)

f2=Frame()

f2.grid(row=2)

text=Label(f,text="Ingrese el Nombre del Jugador 1")

text.grid(row=0,column=0)

text1=Label(f,text="Ingrese el Nombre del Jugador 2")

text1.grid(row=0,column=1)

p1=Entry(f,width=54)

p1.grid(row=1,column=0,pady=2)

p2=Entry(f,width=54)

p2.grid(row=1,column=1,pady=2)

b1=Button(f1,text="Iniciar Juego",bg="skyblue",command= lambda:start(),width=92,height=2)

b1.grid(row=0,column=0)

text2=Label(f2,text="Ingrese el Modo de Juego",bg="skyblue",width=30,border=4)

text2.grid(row=2,column=0)

b2=Radiobutton(f2,text="One Ball",command=lambda:rb(1),variable=opcion_seleccionada, value=1,bg="skyblue",width=10)

b2.grid(row=2,column=1)

b2=Radiobutton(f2,text="Two Ball",command=lambda:rb(2),variable=opcion_seleccionada, value=2,bg="skyblue",width=10)

b2.grid(row=2,column=2)

b2=Radiobutton(f2,text="Three Ball",command=lambda:rb(3),variable=opcion_seleccionada, value=3,bg="skyblue",width=10)

b2.grid(row=2,column=3)

radio=False
two,three=False,False
def rb(e):
    global radio,two,three
    if e==1:radio,two,three=True,False,False
    elif e==2:radio,two,three=True,True,False
    elif e==3:radio,two,three=True,True,True

def start():
    global running,player1,player2
    if radio:
        running=True
        player1=p1.get()
        player2=p2.get()
        a.destroy()

a.mainloop()

pygame.init()

WEIGHT,HEIGHT=700,400

screen=pygame.display.set_mode((WEIGHT,HEIGHT))

pygame.display.set_caption("Pong")

clock=pygame.time.Clock()

FPS=60

GRAY=(127,127,127)
WHITE=(255,255,255)
BLACK=(0,0,0)
GREEN=(0,255,0)
YELLOW=(255,255,0)
RED=(255,0,0)
background=GRAY
angle=90
imagen=pygame.image.load(os.path.join("C:/Users/Cancino/Desktop/codigos de programacion/Python/proyecto/1/final_version/images/planeta.png"))
imagen=pygame.transform.scale(imagen,(700,400))
planeta=pygame.image.load(os.path.join("C:/Users/Cancino/Desktop/codigos de programacion/Python/proyecto/1/final_version/images/marte1.png")).convert_alpha()
planeta=pygame.transform.scale(planeta,(36,36))
planeta1=pygame.image.load(os.path.join("C:/Users/Cancino/Desktop/codigos de programacion/Python/proyecto/1/final_version/images/tierra.png")).convert_alpha()
planeta1=pygame.transform.scale(planeta1,(36,36))
planeta2=pygame.image.load(os.path.join("C:/Users/Cancino/Desktop/codigos de programacion/Python/proyecto/1/final_version/images/saturno.png")).convert_alpha()
planeta2=pygame.transform.scale(planeta2,(40,40))
nave1=pygame.image.load(os.path.join("C:/Users/Cancino/Desktop/codigos de programacion/Python/proyecto/1/final_version/images/nave1.png")).convert_alpha()
nave1=pygame.transform.scale(nave1,(350,200))
nave1=pygame.transform.rotate(nave1,angle)
nave2=pygame.image.load(os.path.join("C:/Users/Cancino/Desktop/codigos de programacion/Python/proyecto/1/final_version/images/nave1.png")).convert_alpha()
nave2=pygame.transform.scale(nave1,(350,200))
nave2=pygame.transform.rotate(nave1,angle*2)
fuente=pygame.font.Font(None,25)
v1,v2,v3,v4,v5,v6,v7,v8=350,200,150,150,150,100,500,20
valor,valor1,valor2,coon=0,0,0,0
value,value1,value2,value3,value4,value5,value6,value7,value8=0,3,3,0,2,2,1,1,0
start1,speed,speed1=True,True,True
sound=pygame.mixer.Sound("C:/Users/Cancino/Desktop/codigos de programacion/Python/proyecto/1/final_version/sounds/pong.wav")
sound_back=pygame.mixer.Sound("C:/Users/Cancino/Desktop/codigos de programacion/Python/proyecto/1/final_version/sounds/pong_back.mp3")
sound_back.play(loops=-1)
sound_back.set_volume(0.3)
while running:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:running=False
        if event.type==KEYUP:
            if event.key==K_UP or event.key==K_DOWN:value3=0
            elif event.key==K_w or event.key==K_s:value8=0
            elif event.key==K_1:two,three=False,False
            elif event.key==K_2:two,three=True,False
            elif event.key==K_3:two,three=True,True
        if event.type==KEYDOWN:
            if event.key==K_UP:value3=-4
            elif event.key==K_DOWN:value3=4
            elif event.key==K_w:value8=-4
            elif event.key==K_s:value8=4
            elif event.key==K_ESCAPE:running=False
            elif event.key==K_p:
                start1=False
                valor+=1
                if valor==2:
                    start1=True
                    valor=0
            if speed:
                if event.key==K_KP_PLUS:
                    FPS+=25
                    value+=1
                    speed1=True
                    if value==5:speed=False
            if speed1:
                if event.key==K_KP_MINUS:
                    FPS-=25
                    value-=1
                    speed=True
                    if value==-1:speed1=False
    screen.blit(imagen,[0,0])
    objeto1=pygame.draw.rect(screen,GREEN,(25,v3,11,90))
    objeto2=pygame.draw.rect(screen,GREEN,(665,v4,11,90))
    objeto3=pygame.draw.ellipse(screen,BLACK,(v1,v2,25,25))
    screen.blit(planeta,(v1-5,v2-5))
    screen.blit(nave1,(-77,v3-130))
    screen.blit(nave2,(578,v4-130))
    if two:
        objeto4=pygame.draw.ellipse(screen,RED,(v5,v6,25,25))
        screen.blit(planeta1,(v5-5,v6-5))
    if three:
        objeto5=pygame.draw.ellipse(screen,YELLOW,(v7,v8,25,25))
        screen.blit(planeta2,(v7-8,v8-8))
    texto_puntaje1=fuente.render(f"Puntaje {valor1}", True, YELLOW)
    texto_puntaje2=fuente.render(f"Puntaje {valor2}", True, YELLOW)
    texto1=fuente.render(f"V {value}", True, YELLOW)
    texto_jugador1=fuente.render(f"{player1}", True, GREEN)
    texto_jugador2=fuente.render(f"{player2}", True, GREEN)
    screen.blit(texto_puntaje1,(45,30))
    screen.blit(texto_puntaje2,(580,30))
    screen.blit(texto1,(330,10))
    screen.blit(texto_jugador1,(45,10))
    screen.blit(texto_jugador2,(580,10))
    
    if start1:
    # ------------players----------------------------------------
        if v1>=WEIGHT/2-50:v4+=value2
        v3+=value8
        # v4+=value3
        if v4>=310:v4=310
        if v4<=0:v4=0
        if v3>=310:v3=310
        if v3<=0:v3=0
    # ---------------------ball one-----------------------------------
        if v1>=WEIGHT-25 or v1<=0:
            value1*=-1
            sound.play(loops=1)
            if v1>=WEIGHT-25:
                valor1+=1
                v1=300
                v2=200
            if v1<=0:
                valor2+=1
                v1=300
                v2=200
        if v2>=HEIGHT-25 or v2<=0:value2*=-1
        if objeto3.colliderect(objeto1):
            value1*=-1
            coon+=1
            sound.play(loops=1)
            if coon>=100:
                v1=300
                v2=200
                coon=0
                valor2+=1
        if objeto3.colliderect(objeto2):
            value1*=-1
            coon+=1
            sound.play(loops=1)
            if coon>=100:
                v1=300
                v2=200
                coon=0
                valor1+=1
        v1+=value1
        v2+=value2
        # -------------------------two ball-------------------------
        if two:
            if v5>=WEIGHT-25 or v5<=0:
                value4*=-1
                sound.play(loops=1)
                if v5>=WEIGHT-25:
                    valor1+=1
                    v5=300
                    v6=200
                if v5<=0:
                    valor2+=1
                    v5=300
                    v6=200
            if v6>=HEIGHT-25 or v6<=0:value5*=-1
            if objeto4.colliderect(objeto1) or objeto4.colliderect(objeto2) or objeto4.colliderect(objeto3):
                value4*=-1
                sound.play(loops=1)
            v5+=value4
            v6+=value5
        # ------------------------three ball-------------------------------
        if three:
            if v7>=WEIGHT-25 or v7<=0:
                value6*=-1
                sound.play(loops=1)
                if v7>=WEIGHT-25:
                    valor1+=1
                    v7=300
                    v8=200
                if v7<=0:
                    valor2+=1
                    v7=300
                    v8=200
            if v8>=HEIGHT-25 or v8<=0:value7*=-1
            if objeto5.colliderect(objeto1) or objeto5.colliderect(objeto2) or objeto5.colliderect(objeto3) or objeto5.colliderect(objeto4):
                value6*=-1
                sound.play(loops=1)
            v7+=value6
            v8+=value7
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()