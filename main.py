from tkinter import *
import tkinter as tk
import tkinter.messagebox as mbox
from tkinter import filedialog
from PIL import ImageTk, Image
import cv2
import argparse
import numpy as np 
import imutils

window = tk.Tk()
window.title("Human Detection & Counting")    #pencere adı
window.geometry('1000x700')      #pencere büyüklüğü
window.configure(bg='#43cd80')

start1 = tk.Label(text = "HUMAN \n DETECTION  &  COUNTING", font=("Arial", 50), fg="black") # same way bg
start1.place(x = 70, y = 10)

start1.configure(bg='#43cd80')

def start():
    window.destroy()

# start button created
Button(window, text="▶ START",command=start,font=("Arial", 25), activeforeground='white', activebackground='black', fg = "black", cursor="hand2", borderwidth=3, relief="raised").place(x =130 , y =570 )
#active ile tıklaynca renk değişiyor 



# image on the main window
path1 = "logo.png"
img2 = ImageTk.PhotoImage(Image.open(path1))
panel1 = tk.Label(window, image = img2)
panel1.place(x = 400, y = 250)
panel1.configure(bg='#43cd80')


exit1 = False
# function created for exiting from window
def exit_win():
    global exit1
    if mbox.askokcancel("Exit", "Do you want to exit?"):
        exit1 = True
        window.destroy()

# exit button created
Button(window, text="❌ EXIT",command=exit_win,font=("Arial", 25),activeforeground='white', activebackground='black', fg = "black", cursor="hand2", borderwidth=3, relief="raised").place(x =680 , y = 570 )
#command ile btonun ne yapacagını belirle


window.protocol("WM_DELETE_WINDOW", exit_win)
window.mainloop()   #pencereyi görmek için

if exit1==False:
    # Main Window & Configuration of window1
    window1 = tk.Tk()
    window1.title("Real Time Human Detection & Counting")
    window1.geometry('1000x700')
    window1.configure(bg='#43cd80')   #ikinci sayfa

    filename=""
    filename1=""
    filename2=""
#######################################################


hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

def detectByCamera():
    
 cam = cv2.VideoCapture('http://192.168.1.6:4747/video')
 width=int(cam.get(cv2.CAP_PROP_FRAME_WIDTH))    #frame boyutu 
 height=int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT))

 print(width,height)    #terminalde aldıgımız görüntünün ölçülerini gösterir

 fourcc = cv2.VideoWriter_fourcc(*'MP4V')    #format

 writer = cv2.VideoWriter("kayit.mp4",fourcc,20,(width,height))   #20:saniyelik görüntü sayısı


 while True:
    
    ret,frame = cam.read()  
                            
    frame = cv2.resize(frame, (640,480))      #faster detection
    
    gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)      #also for faster detection 
    
    # returns the bounding boxes for the detected objects
    boxes, weights = hog.detectMultiScale(frame, winStride=(8,8))
    
    boxes = np.array([[x, y, x + w, y + h] for (x, y, w, h) in boxes])  #Coordinates 
    #cv2.putText(frame, 'Total Persons : ', (40,70), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,0,0), 2)
    
    person=0 
    for(xA, yA, xB, yB) in boxes:  #xA,yA start coordinate  xB yB end coordinate
        person += 1
        cv2.rectangle(frame, (xA, yA), (xB, yB), (0, 255, 0), 2) #(image, start_point, end_point, color, thickness)
        cv2.putText(frame, 'person: {}'.format(person), (xA ,yA), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 1)  #for counting
        
        
    cv2.putText(frame, 'Total Persons : {}'.format(person), (40,70), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,0,0), 2)
        

    cv2.imshow("Human_Detection_and_Counting_webcam",frame)

    if cv2.waitKey(30) & 0xFF == ord('q'):
        break
    
    writer.write(frame)   #for record

 cam.release()#release the cam
 writer.release()    #to close the already opened file.
 cv2.destroyAllWindows()
    
#####################################################################

def detectByImage():
    image = cv2.imread('people1.jpg')  
    imageWidth = image.shape[1]
    image = imutils.resize(image,        
					width=min(400, image.shape[1]))   

    (regions, _) = hog.detectMultiScale(image,
									winStride=(4, 4),
									padding=(4, 4),
									scale=1.05)

    Human, weights = hog.detectMultiScale(image, winStride=(4, 4), padding=(8, 8), scale=1.2)
    Human = np.array([[x, y, x + w, y + h] for (x, y, w, h) in Human])


    Count=0

    for x, y, w, h in Human:
        cv2.rectangle(image, (x, y), (w, h), (0, 0, 100), 2)
        cv2.rectangle(image, (x, y - 20), (w,y), (0, 0, 255), -1)
        Count += 1
        cv2.putText(image, f'Human{Count}', (x, y-5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

    
    cv2.putText(image, 'Total Persons : {}'.format(Count), (40,70), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,0,0), 2)


    cv2.imshow('Human_Detection_and_Counting_image', image)
    cv2.imwrite('NewImage.jpg', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()



#################################################################
    
lbl1 = tk.Label(text="OPTIONS", font=("Arial", 50),fg="black")  # same way bg
lbl1.place(x=340, y=20)
lbl1.configure(bg='#43cd80')

    # image on the main window
pathi = "imagelogo.jpg"
imgi = ImageTk.PhotoImage(Image.open(pathi))
paneli = tk.Label(window1, image = imgi)
paneli.place(x = 90, y = 150)
#paneli.configure(bg='blue')   çerçeve


    # image on the main window
pathv = "camlogo.jpg"
imgv = ImageTk.PhotoImage(Image.open(pathv))
panelv = tk.Label(window1, image = imgv)
panelv.place(x = 575, y = 150)

    # created button for all option
Button(window1, text="FROM IMAGE ",command=detectByImage, cursor="hand2", font=("Arial",30), bg = "pink", fg = "black").place(x = 90, y = 475)
Button(window1, text="FROM PHONECAM",command=detectByCamera, cursor="hand2", font=("Arial", 30), bg = "pink", fg = "black").place(x = 530, y = 475) #90, 300

    # function defined to exit from window1
def exit_win1():
    if mbox.askokcancel("Exit", "Do you want to exit?"):
        window1.destroy()

    # created exit button
Button(window1, text="❌ EXIT",command=exit_win1,  cursor="hand2", font=("Arial", 25), activeforeground='white', activebackground='red').place(x = 390, y = 600)

window1.protocol("WM_DELETE_WINDOW", exit_win1)
window1.mainloop()


