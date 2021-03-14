import serial, time
import tensorflow as tf
import keras
import numpy as np
import time
import cv2

arduino = serial.Serial("COM4", 9600)
time.sleep(2)

model = tf.keras.models.load_model('mask.h5')
face_clsfr=cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

labels_dict={0:'No acceder',1:'Acceder',2:'Verificando'}
color_dict={0:(107,17,236),1:(247,247,10),2:(105,246,45)}

def deteccion():
    arduino.write(b'2')

def acceder():
    arduino.write(b'1')

def no_acceder():
    arduino.write(b'0')


cantidad_detecciones=0 #Cuenta la cantidad de veces seguidas que se ha detectado como Uso de Mascarilla
source=cv2.VideoCapture(0)

no_acceder()
while(True):
    ret,img=source.read()
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    faces=face_clsfr.detectMultiScale(gray,1.3,5)  

    for (x,y,w,h) in faces:
        face_img=gray[y:y+h,x:x+w]
        resized=cv2.resize(face_img,(100,100))
        normalized=resized/255.0
        reshaped=np.reshape(normalized,(1,100,100,1))
        result=model.predict(reshaped)

        if result[0][0] > 0.65: # Si está 65% seguro de mascarilla, marcar como 'acceder'
            label = 2 #Detectando
            cantidad_detecciones+=1
            deteccion()
            
            if cantidad_detecciones >= 20:
                label=1           

                if cantidad_detecciones == 28:
                    acceder()
                    cantidad_detecciones=0
                    no_acceder()
                    
        else:
            label=0
            cantidad_detecciones = 0
            no_acceder()

        #print(cantidad_detecciones)
        cv2.rectangle(img,(x,y),(x+w,y+h),color_dict[label],2)
        cv2.rectangle(img,(x,y-40),(x+w,y),color_dict[label],-1)
        cv2.putText(img, labels_dict[label], (x, y-10),cv2.FONT_HERSHEY_SIMPLEX,0.8,(255,255,255),2)
        
    cv2.imshow('LIVE',img)
    key=cv2.waitKey(1)
    
    if(key==27):
        break

arduino.close()
cv2.destroyAllWindows()
source.release()