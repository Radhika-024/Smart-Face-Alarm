import cv2
import pygame
import time
import datetime  

##config
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
ALARM_FILE = "alarm_sound.mp3"  
CAMERA_INDEX = 1

##SET ALARM
print("--- SMART FACE ALARM ---")
alarm_input = input("Enter alarm time (HH:MM in 24-hour format, e.g., 07:30): ")

print(f"Alarm set for {alarm_input}. Waiting...")

##WAITING 
while True:
    #current time 
    current_time = datetime.datetime.now().strftime("%H:%M")
    
    if current_time == alarm_input:
        print("WAKE UP! IT IS TIME!")
        break 
    
    time.sleep(1)
##alram buzzing and open camera 
pygame.mixer.init()
pygame.mixer.music.load(ALARM_FILE)
pygame.mixer.music.play(-1) # Loop the alarm sound

cap = cv2.VideoCapture(CAMERA_INDEX)
start_time = None # Timer for face 

while True:
    ret, frame = cap.read()
    if not ret: break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 5)

    # If face is found
    if len(faces) > 0:
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        
        # Start counting
        if start_time is None:
            start_time = time.time()
        else:
            elapsed = time.time() - start_time
            print(f"Face detected... {int(elapsed)} seconds")
            
            if elapsed >= 2: # Look for 2 seconds to stop
                print("GOOD MORNING! Alarm stopped.")
                pygame.mixer.music.stop()
                break
    else:
        # If you look away or hide under covers, timer resets!
        start_time = None
        print("Show your face to stop the alarm!")

    cv2.imshow('Smart Alarm', frame)
    
    # Press 'q' quit manually
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
