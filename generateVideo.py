import cv2
import numpy as np
from os import path


prediction = np.loadtxt('a1-a2-window.txt')
query = 'Afternoon2-GPS'
database = 'Afternoon1-GPS'

videow = cv2.VideoWriter("a1-a2-f.avi", fourcc=cv2.VideoWriter_fourcc('X','V','I','D'), fps=21, frameSize=(1080,720))

for q, db in enumerate(prediction): 

    qFile = "{:0>3d}.jpg".format(q)
    print("Processing: ",path.join(query,qFile))
    qImage = cv2.imread(path.join(query,qFile))
    qlabel = np.zeros(shape=(qImage.shape[0]//2,qImage.shape[1], qImage.shape[2]), dtype=qImage.dtype)
    cv2.putText(qlabel, text='query: Dusk1 '+qFile, org=(100,150), fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=3, color=(255, 255, 255), thickness=4)


    dblabel = np.zeros(shape=qlabel.shape,dtype=qlabel.dtype)
    if db!=-1:
        dbFile = "{:0>3d}.jpg".format(int(db)-1)
        dbImage = cv2.imread(path.join(database, dbFile))
        if not path.exists(path.join(database, dbFile)):
            print(path.join(database, dbFile))
    else:
        dbImage = np.zeros(shape=qImage.shape,dtype=qlabel.dtype)

    
    cv2.putText(dblabel, text='database: Afternoon1 '+dbFile, org=(100,150), fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=3, color=(255, 255, 255), thickness=4)

    img1 = np.append(qlabel, qImage, axis=0)
    img2 = np.append(dblabel, dbImage, axis=0)
    img = np.append(img1, img2, 0)

    img = cv2.resize(img, (1080,720))


#    cv2.imshow('img', img)
    cv2.waitKey(1)


    videow.write(img)

videow.release()

         
    
