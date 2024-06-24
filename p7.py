import queue
import threading
import time
import pygame,os
from pygame.locals import*
from tkinter import*
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Dense, Flatten
from tensorflow.keras.optimizers import Adam
from collections import deque
import concurrent.futures
import random

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

a.mainloop()

def modelo_ia(tamaño_entrada, acciones_salida):
    model = Sequential()
    model.add(Dense(8, input_dim=tamaño_entrada, activation='relu'))
    model.add(Dense(16, activation='relu'))
    model.add(Dense(8, activation='relu'))
    model.add(Dense(acciones_salida, activation='linear'))
    model.compile(loss='mse', optimizer=Adam(learning_rate=0.001))
    return model

# Parámetros
state_size = 4  # Define según tu estado
action_size = 2  # Define según tus acciones posibles
gamma = 0.95
epsilon = 1.0
epsilon_min = 0.01
epsilon_decay = 0.995
replay_buffer = deque(maxlen=2000)
batch_size = 64
reward=0
# Inicializa el estado
state = np.array([0, 0, 0, 0])
state = np.reshape(state, [1, state_size])

# Ruta para guardar el modelo
model_path = "C:/Users/Cancino/Desktop/codigos de programacion/Python/proyecto/1/final_version/IA/modelo_pong.keras"

# Cargar modelo si existe, sino crear uno nuevo
if os.path.exists(model_path):
    model = load_model(model_path, compile=False)
    model.compile(loss='mse', optimizer=Adam(learning_rate=0.001))
    print("Modelo Cargado")
else:
    model = modelo_ia(state_size, action_size)
    print("No se encontró un modelo, se creará uno nuevo")

# Flag de finalización
terminate = threading.Event()

# Crear una cola para experiencias
experience_queue = queue.Queue()

# Funciones de Memoria y Acción
def remember(state, action, reward, next_state, done):
    experience_queue.put((state, action, reward, next_state, done))

def act(state):
    if np.random.rand() <= epsilon:
        return random.randrange(action_size)
    q_values = model.predict(state)
    return np.argmax(q_values[0])

def replay():
    global epsilon
    while not terminate.is_set():
        if experience_queue.qsize() < batch_size:
            time.sleep(0.1)
            continue
        minibatch = random.sample(list(experience_queue.queue), batch_size)
        for state, action, reward, next_state, done in minibatch:
            target = reward
            if not done:
                target = (reward + gamma * np.amax(model.predict(next_state)[0]))
            target_f = model.predict(state)
            target_f[0][action] = target
            model.fit(state, target_f, epochs=1, verbose=0)
        if epsilon > epsilon_min:
            epsilon *= epsilon_decay
        time.sleep(0.1)

# Función de mutación
def mutate(weights, mutation_rate=0.01):
    new_weights = []
    for weight in weights:
        if random.random() < mutation_rate:
            mutation = np.random.normal(scale=0.1, size=weight.shape)
            new_weights.append(weight + mutation)
        else:
            new_weights.append(weight)
    return new_weights

pygame.init()

WEIGHT,HEIGHT=700,400

screen=pygame.display.set_mode((WEIGHT,HEIGHT))

pygame.display.set_caption("Pong")

clock=pygame.time.Clock()

frame_count = 0
prediction_interval = 5
action=None
# Utilizar ThreadPoolExecutor para predicciones en paralelo
executor = concurrent.futures.ThreadPoolExecutor()
future = None
# Creación y inicio del hilo para la función replay
replay_thread = threading.Thread(target=replay)
replay_thread.start()

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
contador=0
player1_win,player2_win=False,False
while running:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            terminate.set()
            running=False
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
            elif event.key==K_s:
                value8=4
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
            # if game_over:
            #     if event.key==K_r:
            #         v1,v2,v3,v4,v5,v6,v7,v8=350,200,150,150,150,100,500,20
            #         value,valor1,valor2,coon=0,0,0,0
            #         FPS=60
            #         sound_back.play(loops=-1)
            #         player1_win,player2_win=False,False
            #         start1,speed,speed1=True,True,True
            #         game_over=False
        if game_over:
                v1,v2,v3,v4,v5,v6,v7,v8=350,200,150,150,150,100,500,20
                valor1,valor2,coon=0,0,0
                sound_back.play(loops=-1)
                player1_win,player2_win=False,False
                start1=True
                contador+=1
                game_over=False
                if contador==10:
                    terminate.set()
                    running=False
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
            terminate.set()
            sound_back.stop()
            screen.fill(background)
            pygame.draw.rect(screen,"black",(12,12,675,375),10)
            text_game_over=fuente2.render("GAME OVER",True,"black")
            text_win_player=fuente1.render(f"player {player1} win",True,"lightgreen")
            text_reset=fuente.render("Reset Press R",True,"black")
            screen.blit(text_game_over,(WEIGHT/2-100,HEIGHT/2-100))
            screen.blit(text_win_player,(25,350))
            screen.blit(text_reset,(WEIGHT/2-50,HEIGHT/2-60))
            reward=-1
            player1_win,player2_win=True,False
            game_over=True
    if valor2==puntos:
            start1=False
            terminate.set()
            sound_back.stop()
            screen.fill(background)
            pygame.draw.rect(screen,"black",(12,12,675,375),10)
            text_game_over=fuente2.render("GAME OVER",True,"black")
            text_win_player=fuente1.render(f"player {player2} win",True,"lightgreen")
            text_reset=fuente.render("Reset Press R",True,"black")
            screen.blit(text_game_over,(WEIGHT/2-100,HEIGHT/2-100))
            screen.blit(text_win_player,(25,350))
            screen.blit(text_reset,(WEIGHT/2-50,HEIGHT/2-60))
            player1_win,player2_win=False,True
            reward=1
            game_over=True
    # ------------------pause-----------------------------------
    if p:
        text_pause=fuente2.render("PAUSE",True,"black")
        screen.blit(text_pause,(WEIGHT/2-50,HEIGHT/2-100))
    #-----------------mutations------------------------------------
    if player1_win:
        print("Mutación aplicada")
        current_weights = model.get_weights()
        mutated_weights = mutate(current_weights, mutation_rate=0.01)
        model.set_weights(mutated_weights)
        player1_win,player2_win=False,False
    if start1:
    #-------------IA---------------------------------------------
        if frame_count % prediction_interval == 0:
            state =np.array([objeto1.y,objeto2.y,objeto3.x,objeto3.y])
            state = np.reshape(state, [1, state_size])
            future=executor.submit(act,state)
        if future and future.done():
            action=future.result()
        if action == 0:
            value3=-4
        elif action == 1:
            value3=4
        else:pass
        reward=0
        # Actualiza el juego y obtén el nuevo estado y la recompensa
        next_state =np.array([objeto1.y,objeto2.y,objeto3.x,objeto3.y])
        next_state = np.reshape(next_state, [1, state_size])
        # Almacena la experiencia y actualiza el estado
        remember(state, action, reward, next_state,running)
        state = next_state
    # ------------players----------------------------------------
        # if v1>=WEIGHT/2-50:v4+=value2
        if v1<=WEIGHT/2-50:v3+=value2
        # elif v5>=WEIGHT/2-50:v4+=value5
        # elif v7>=WEIGHT/2-50:v4+=value7
        # v3+=value8
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
                reward=-1
                v1=300
                v2=200
            if v1<=0:
                valor2+=1
                reward=1
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
            reward=0.5
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
    pygame.display.flip()
    clock.tick(FPS)
    frame_count += 1
    
replay_thread.join()
executor.shutdown()
model.save(model_path)
print("modelo guardado")
pygame.quit()