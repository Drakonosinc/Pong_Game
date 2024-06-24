import pygame,os
import numpy as np
from pygame.locals import*
from tkinter import*
import tensorflow as tf
from keras.optimizers import Adam
import concurrent.futures

a=Tk()

running,game_over=False,False

a.geometry("650x400+350+150")

a.maxsize(650,400)

a.minsize(650,400)

a.configure(background="gray")

opcion_seleccionada = IntVar(value=1)

f=Frame()

f.grid(row=0)

f1=Frame()

f1.grid(row=1)

f2=Frame(background="skyblue")

f2.grid(row=2,sticky="nsew")

text=Label(f,text="Ingrese el Nombre del Jugador 1")

text.grid(row=0,column=0)

text1=Label(f,text="Ingrese el Nombre del Jugador 2")

text1.grid(row=0,column=1)

p1=Entry(f,width=54)

p1.grid(row=1,column=0,pady=2)

p2=Entry(f,width=54)

p2.grid(row=1,column=1,pady=2)

p2.insert(0, "PC")

b1=Button(f1,text="Iniciar Juego",bg="skyblue",command= lambda:start(),width=92,height=2)

b1.grid(row=0,column=0)

text2=Label(f2,text="Ingrese el Modo de Juego",bg="skyblue",border=4)

text2.grid(row=0,column=0,sticky="nsew")

b2=Radiobutton(f2,text="One Ball",command=lambda:rb(1),variable=opcion_seleccionada, value=1,bg="skyblue")

b2.grid(row=0,column=1)

b2=Radiobutton(f2,text="Two Ball",command=lambda:rb(2),variable=opcion_seleccionada,width=10 ,value=2,bg="skyblue")

b2.grid(row=0,column=2)

b2=Radiobutton(f2,text="Three Ball",command=lambda:rb(3),variable=opcion_seleccionada,width=14 ,value=3,bg="skyblue")

b2.grid(row=0,column=3)

text3=Label(f2,text="Ingrese la cantidad de puntos máximos para ganar",bg="skyblue",border=4)

text3.grid(row=1,sticky="nsew",padx=10)

pun_end=Entry(f2)

pun_end.grid(row=1,column=1)

pun_end.insert(0, 5)

two,three=False,False

def rb(e):
    global two,three
    if e==1:two,three=False,False
    elif e==2:two,three=True,False
    elif e==3:two,three=True,True

def start():
    global running,player1,player2,puntos
    running=True
    player1=p1.get()
    player2=p2.get()
    puntos = int(pun_end.get())
    a.destroy()

estados=[]
acciones=[]
def registro(estado,accion):
    global estados,acciones
    estados.append(estado)
    acciones.append(accion)
def save(archivo_estado,archivo_accion):
    global estados,acciones
    np.save(archivo_estado, np.array(estados))
    np.save(archivo_accion, np.array(acciones))

# Cargar el modelo sin el optimizador
modelo_IA = tf.keras.models.load_model("C:/Users/Cancino/Desktop/codigos de programacion/Python/proyecto/1/final_version/IA/pong_ai_version_2.keras", compile=False)

# Compilar el modelo nuevamente con el optimizador deseado
modelo_IA.compile(optimizer=Adam(learning_rate=0.001), loss='mse')

def acciones_ia(estado):
    global modelo_IA
    estado=np.array(estado).reshape(1, -1)
    accion_ia=modelo_IA.predict(estado)
    return accion_ia[0]

a.mainloop()

pygame.init()

WEIGHT,HEIGHT=700,400

screen=pygame.display.set_mode((WEIGHT,HEIGHT))

pygame.display.set_caption("Pong")

clock=pygame.time.Clock()

frame_count = 0
prediction_interval = 5
ia=[0,0]
# Utilizar ThreadPoolExecutor para predicciones en paralelo
executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)
future = None

FPS=60

GRAY=(127,127,127)
WHITE=(255,255,255)
BLACK=(0,0,0)
GREEN=(0,255,0)
YELLOW=(255,255,0)
RED=(255,0,0)
background=GRAY
angle=90
p=False
imagen=pygame.image.load(os.path.join("C:/Users/Cancino/Desktop/codigos de programacion/Python/proyecto/1/final_version/images/planeta.jpg"))
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
fuente1=pygame.font.Font(None,35)
fuente2=pygame.font.Font(None,50)
v1,v2,v3,v4,v5,v6,v7,v8=350,200,150,150,150,100,500,20
valor,valor1,valor2,coon=0,0,0,0
value,value1,value2,value3,value4,value5,value6,value7,value8=0,3,3,0,2,2,1,1,0
start1,speed,speed1=True,True,True
sound=pygame.mixer.Sound("C:/Users/Cancino/Desktop/codigos de programacion/Python/proyecto/1/final_version/sounds/pong.wav")
sound_back=pygame.mixer.Sound("C:/Users/Cancino/Desktop/codigos de programacion/Python/proyecto/1/final_version/sounds/pong_back.mp3")
sound_back.play(loops=-1)
sound_back.set_volume(0.3)
while running:
    action=[0,0]
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
            elif event.key==K_w:
                value8=-4
                action[0] = -1
            elif event.key==K_s:
                value8=4
                action[0] = 1 
            elif event.key==K_ESCAPE:running=False
            elif event.key==K_p:
                start1,p=False,True
                sound_back.stop()
                valor+=1
                if valor==2:
                    start1,p=True,False
                    sound_back.play(loops=-1)
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
#------------------------reset----------------------------------------
            if game_over:
                if event.key==K_r:
                    v1,v2,v3,v4,v5,v6,v7,v8=350,200,150,150,150,100,500,20
                    value,valor1,valor2,coon=0,0,0,0
                    FPS=60
                    sound_back.play(loops=-1)
                    start1,speed,speed1=True,True,True
                    game_over=False
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
    screen.blit(texto1,(340,10))
    screen.blit(texto_jugador1,(45,10))
    screen.blit(texto_jugador2,(580,10))
    # ------------game over--------------------------------------
    if valor1==puntos:
            start1=False
            sound_back.stop()
            screen.fill(background)
            pygame.draw.rect(screen,"black",(12,12,675,375),10)
            text_game_over=fuente2.render("GAME OVER",True,"black")
            text_win_player=fuente1.render(f"player {player1} win",True,"lightgreen")
            text_reset=fuente.render("Reset Press R",True,"black")
            screen.blit(text_game_over,(WEIGHT/2-100,HEIGHT/2-100))
            screen.blit(text_win_player,(25,350))
            screen.blit(text_reset,(WEIGHT/2-50,HEIGHT/2-60))
            game_over=True
    if valor2==puntos:
            start1=False
            sound_back.stop()
            screen.fill(background)
            pygame.draw.rect(screen,"black",(12,12,675,375),10)
            text_game_over=fuente2.render("GAME OVER",True,"black")
            text_win_player=fuente1.render(f"player {player2} win",True,"lightgreen")
            text_reset=fuente.render("Reset Press R",True,"black")
            screen.blit(text_game_over,(WEIGHT/2-100,HEIGHT/2-100))
            screen.blit(text_win_player,(25,350))
            screen.blit(text_reset,(WEIGHT/2-50,HEIGHT/2-60))
            game_over=True
    # ------------------pause-----------------------------------
    if p:
        text_pause=fuente2.render("PAUSE",True,"black")
        screen.blit(text_pause,(WEIGHT/2-50,HEIGHT/2-100))
    if start1:
    #---------------IA-----------------------------------------
        if frame_count % prediction_interval == 0:
        # Obtener la acción de la IA en un hilo separado
            estado=[objeto1.y,objeto2.y,objeto3.x,objeto3.y,value1,value2]
            future = executor.submit(acciones_ia, estado)
        if future and future.done():
            ia = future.result()
        if ia[0]< 0 and objeto2.top>0:
            value3=-4
        if ia[0]>0 and objeto2.bottom<HEIGHT:
            value3=4
    # ------------players----------------------------------------
        # if v1>=WEIGHT/2-50:v4+=value2
        # elif v5>=WEIGHT/2-50:v4+=value5
        # elif v7>=WEIGHT/2-50:v4+=value7
        v3+=value8
        v4+=value3
        if v4>=310:v4=310
        if v4<=0:v4=0
        if v3>=310:v3=310
        if v3<=0:v3=0
    # ---------------------ball one-------------------------------
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
            sound.play(loops=0)
            if coon>=50:
                v1=300
                v2=200
                coon=0
                valor2+=1
        if objeto3.colliderect(objeto2):
            value1*=-1
            coon+=1
            sound.play(loops=0)
            if coon>=50:
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
                sound.play(loops=0)
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
                sound.play(loops=0)
            v7+=value6
            v8+=value7
    #-----------------------datos---------------------------------------
    estado=[objeto1.y,objeto2.y,objeto3.x,objeto3.y,value1,value2]
    registro(estado,action)
    
    pygame.display.flip()
    clock.tick(FPS)
    frame_count += 1

executor.shutdown()
pygame.quit()
save('pong_states.npy', 'pong_actions.npy')