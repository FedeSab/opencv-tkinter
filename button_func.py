from tkinter import *
from tkinter import filedialog
import cv2
import numpy as np
from PIL import Image
from PIL import ImageTk
import imutils


OPTIONS = ['None',
           'Resize(BGR)',
           'BGR to Gray (will display changes)',
'BGR to HSV (will not display changes)',
'Gray to BGR',
'inRange (HSV, see help, outputs BGR)',
'Circle detection (gray to rgb), Hugh method, soon contour detection + min circle approch',
'Canny (gray)',
'GaussianBlur (BGR, see help)',
'Dilate (Gray or BGR)',
'Erode (Gray or BGR)',
'White Hat (Gray)',
'Black Hat (Gray)',
'Adaptative (Gray to binary for contours, etc)',
'Contour Detection',
'Circle from contours (do not use contour detection before)',
'Rectangle from contours (do not use contour detection before)',
'Otsu (Gray to Gray)'
] #etc

OPTION_DICT = {'None':'None',
               'Resize(BGR)':'Resize',
           'BGR to Gray (will display changes)':'BGR2GRAY',
'BGR to HSV (will not display changes)':'BGR2HSV',
'Gray to BGR':'GRAY2BGR',
'inRange (HSV, see help, outputs BGR)':'inRange',
'Circle detection (gray to rgb), Hugh method, soon contour detection + min circle approch':'Circle',
'Canny (gray)':'Canny',
'GaussianBlur (BGR, see help)':'Blur',
'Dilate (Gray or BGR)':'Dilate',
'Erode (Gray or BGR)':'Erode',
'White Hat (Gray)':'White',
'Black Hat (Gray)':'Black',
'Adaptative (Gray to binary for contours, etc)': 'Adaptative',
'Contour Detection': 'Contour',
'Circle from contours (do not use contour detection before)':'Contour circle',
'Rectangle from contours (do not use contour detection before)':'Contour rectangle',
'Otsu (Gray to Gray)': 'Otsu'
}


def cv2_func_pack(func,frame,params):
    if func == 'BGR2GRAY':
        return cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY), 'gray'
    elif func == 'BGR2HSV':
        return cv2.cvtColor(frame, cv2.COLOR_BGR2HSV), 'hsv'
    elif func=='GRAY2BGR':
        return cv2.cvtColor(frame,cv2.COLOR_GRAY2BGR), 'bgr'
    elif func=='inRange':
        lowr = (int(params['low1_var'].get()), int(params['low2_var'].get()), int(params['low3_var'].get()))
        highr = (int(params['high1_var'].get()), int(params['high2_var'].get()), int(params['high3_var'].get()))
        lowr = np.array(lowr, np.uint8)
        highr = np.array(highr, np.uint8)
        mask = cv2.inRange(frame,lowr, highr)
        #mask = cv2.medianBlur(mask, 7)
        frame = cv2.cvtColor(frame, cv2.COLOR_HSV2BGR)
        invMask = cv2.bitwise_not(mask)
        colorDetected = cv2.bitwise_and(frame, frame, mask=mask )
        black_bg = np.zeros_like(frame, dtype='uint8')
        bgGray2 = cv2.bitwise_and(black_bg,black_bg, mask=invMask)
        finalImage2 = cv2.add(bgGray2, colorDetected)
        return finalImage2, 'bgr'
    elif func=='Resize':
        new_x = int(params['new_x_var'].get())
        new_y = int(params['new_y_var'].get())
        return cv2.resize(frame, (new_x,new_y)), 'bgr'
    elif func=='Circle':
        dp, minDist, Param1  = int(params['dp'].get()), int(params['dist'].get()), int(params['internal_canny'].get())
        Param2, minRadius= int(params['acumulation'].get()), int(params['min_rad'].get())
        maxRadius =int(params['max_rad'].get())
        circles = cv2.HoughCircles(frame, cv2.HOUGH_GRADIENT, dp, minDist,
                                  param1=Param1,param2=Param2, minRadius=minRadius, maxRadius= maxRadius)
        frame = cv2.cvtColor(frame,cv2.COLOR_GRAY2BGR)
        if circles is not None:
            # convert the (x, y) coordinates and radius of the circles to integers
            #circles = np.round(circles[0, :]).astype("int")
            # loop over the (x, y) coordinates and radius of the circles
            for (x, y, r) in circles[0]:
                # draw the circle in the output image, then draw a rectangle
                # corresponding to the center of the circle
                x, y, r = int(x), int(y), int(r)
                cv2.circle(frame, (x, y), r, (0, 255, 0), 4)
                cv2.rectangle(frame, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
        # return cv2.HoughCircles(frame, cv2.HOUGH_GRADIENT, params[0],params[1],params[2],params[3])
        return frame, 'rgb'
    elif func=='Canny':
        lowert, highert, aperture = int(params['lower'].get()), int(params['higher'].get()), 2*int(params['aperture'].get())+3
        return cv2.Canny(frame, lowert, highert, apertureSize=aperture ), 'gray'
    elif func=='Blur':
        krx, kry, dev = int(params['kernelx'].get()), int(params['kernely'].get()), int(params['dev'].get())
        return cv2.GaussianBlur(frame, (krx,kry), dev), 'rgb'
    elif func=='Dilate':
        krx, kry, dev = int(params['kernelx'].get()), int(params['kernely'].get()), int(params['iter'].get())
        return cv2.dilate(frame, (krx,kry), iterations=dev), 'rgb'
    elif func=='Erode':
        krx, kry, dev = int(params['kernelx'].get()), int(params['kernely'].get()), int(params['iter'].get())
        return cv2.erode(frame, (krx,kry), iterations=dev), 'rgb'
    elif func=='White':
        krx, kry = int(params['kernelx'].get()), int(params['kernely'].get())
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT,
                                        (krx,kry))
        return cv2.morphologyEx(frame, cv2.MORPH_TOPHAT, kernel), 'gray'
    elif func=='Black':
        krx, kry = int(params['kernelx'].get()), int(params['kernely'].get())
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT,
                                        (krx,kry))
        return cv2.morphologyEx(frame, 
                              cv2.MORPH_BLACKHAT,
                              kernel), 'gray'
    elif func=='Adaptative':
        blk, conc = int(params['block'].get()), int(params['constant'].get())
        blk, conc = blk*2+1, conc*2 +1
        strategy_dict = {'Gaussian':cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 'Mean':cv2.ADAPTIVE_THRESH_MEAN_C}
        normal_dict = {'normal':cv2.THRESH_BINARY, 'inv':cv2.THRESH_BINARY_INV}
        strat = strategy_dict[params['start'].get()]
        normal = normal_dict[params['normal'].get()]
        return cv2.adaptiveThreshold(frame, 255, strat,
                                          normal , blk, conc), 'gray'
    elif func=='Contour':
        mode = params['mode'].get()
        mode2 = params['mode2'].get()
        mode_dict = {'simple': cv2.CHAIN_APPROX_SIMPLE, 'none':cv2.CHAIN_APPROX_NONE}
        mode2_dict = {'external': cv2.RETR_EXTERNAL, 'tree':cv2.RETR_TREE}
        contours, hierarchy = cv2.findContours(frame, 
            mode2_dict[mode2], mode_dict[mode])
        frame = cv2.cvtColor(frame,cv2.COLOR_GRAY2BGR)
        cv2.drawContours(frame, contours, -1, (0, 255, 0), 3)
        return frame, 'rgb'
    elif func=='Contour circle':
        mode = params['mode'].get()
        mode2 = params['mode2'].get()
        min_radius = int(params['min_radius'].get())
        mode_dict = {'simple': cv2.CHAIN_APPROX_SIMPLE, 'none':cv2.CHAIN_APPROX_NONE}
        mode2_dict = {'external': cv2.RETR_EXTERNAL, 'tree':cv2.RETR_TREE}
        contours, hierarchy = cv2.findContours(frame, 
            mode2_dict[mode2], mode_dict[mode])
        frame = cv2.cvtColor(frame,cv2.COLOR_GRAY2BGR)
        cv2.drawContours(frame, contours, -1, (0, 255, 0), 3)
        cnts = imutils.grab_contours((contours, hierarchy))
        ###
        center = None
        if len(cnts) > 0:
                c = max(cnts, key=cv2.contourArea)
                ((x, y), radius) = cv2.minEnclosingCircle(c)
                M = cv2.moments(c)
                center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
                # only proceed if the radius meets a minimum size
                if radius > min_radius:
                    # draw the circle and centroid on the frame,
                    # then update the list of tracked points
                    cv2.circle(frame, (int(x), int(y)), int(radius),
                        (0, 255, 255), 2)
                    cv2.circle(frame, center, 5, (0, 0, 255), -1)
        return frame, 'rgb'
    elif func=='Contour rectangle':
        mode = params['mode'].get()
        mode2 = params['mode2'].get()
        min_radius = int(params['min_radius'].get())
        mode_dict = {'simple': cv2.CHAIN_APPROX_SIMPLE, 'none':cv2.CHAIN_APPROX_NONE}
        mode2_dict = {'external': cv2.RETR_EXTERNAL, 'tree':cv2.RETR_TREE}
        contours, hierarchy = cv2.findContours(frame, 
            mode2_dict[mode2], mode_dict[mode])
        frame = cv2.cvtColor(frame,cv2.COLOR_GRAY2BGR)
        #cv2.drawContours(frame, contours, -1, (0, 255, 0), 3)
        #cnts = imutils.grab_contours((contours, hierarchy))
        ###
        center = None
        for c in contours:
            x,y,w,h = cv2.boundingRect(c)
            if w*h > min_radius:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (36,255,12), 2)
        return frame, 'rgb'
    elif func=='Otsu':
        llow, hhigh = int(params['var1'].get()), int(params['var2'].get())
        mode = params['mode2'].get()
        mode_dict = {'0': cv2.THRESH_BINARY + cv2.THRESH_OTSU, 
                     '1': cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU}
        ret, thresh1 = cv2.threshold(frame, llow, hhigh, mode_dict[mode])  
        return thresh1, 'gray'
