from tkinter import *
from tkinter import filedialog
import cv2
import numpy as np
from PIL import Image
from PIL import ImageTk
from button_func import OPTIONS, cv2_func_pack, OPTION_DICT
#Main shape



func_dict = {}
func_list = []
mask_list = []

def open_file():
    global image, to_display, base_image, func_dict, func_list, abs_width, abs_height

    path_img = filedialog.askopenfilename(filetypes= [("Image","*.*")])
    if path_img:
        image = cv2.imread(path_img)
        abs_height, abs_width = image.shape[0], image.shape[1]
        image_rz = cv2.resize(image, (400,400)).copy()
        #base_image = image.copy()
        to_display = cv2.cvtColor(image_rz,cv2.COLOR_BGR2RGB).copy()
        to_display = Image.fromarray(to_display)
        to_display2 = ImageTk.PhotoImage(image=to_display)
        image_label.configure(image=to_display2)
        image_label.image = to_display2
        functions_in_order()
        
        
def delete(name):
    func_dict[name]['frame'].destroy()
    # for i in func_dict[name]:
    #     print(i)
    #     func_dict[name][i].destroy()
    del func_dict[name]
    for i in range(len(func_list)):
        if func_list[i][1] == name:
            func_list.pop(i)
            functions_in_order()
            return
        
def option_menu(x):
    ''' 
    I need to create the slicers and the delete button
    '''
    x = OPTION_DICT[x]
    base = x
    if x == 'None':
        return
    if x not in func_dict:
        func_dict[x] = {}
    else:
        x = x+'1'
        func_dict[x] = {}
    #Func frame
    func_list.append([base,x])
    func_dict[x]['frame'] = LabelFrame(display_frame,text=x)
    func_dict[x]['frame'].pack()
    func_dict[x]['delete'] = Button(func_dict[x]['frame'] , text='Delete',command=lambda: delete(x))
    func_dict[x]['delete'].grid(row=0,column=0)
    #Func values, slicers and others
    if base=='inRange':
        func_dict[x]['text1'] = Label(func_dict[x]['frame'], text='Low Range').grid(row=0,column=1)
        func_dict[x]['text2'] = Label(func_dict[x]['frame'], text='High Range').grid(row=1,column=1)
        func_dict[x]['low1_var']  = StringVar()
        func_dict[x]['low1'] = Entry(func_dict[x]['frame'],textvariable=func_dict[x]['low1_var'], width=5).grid(row=0,column=2)
        func_dict[x]['low2_var']  = StringVar()
        func_dict[x]['low2'] = Entry(func_dict[x]['frame'],textvariable=func_dict[x]['low2_var'], width=5).grid(row=0,column=3)
        func_dict[x]['low3_var']  = StringVar()
        func_dict[x]['low3'] = Entry(func_dict[x]['frame'],textvariable=func_dict[x]['low3_var'], width=5).grid(row=0,column=4)
        func_dict[x]['high1_var']  = StringVar()
        func_dict[x]['high1'] = Entry(func_dict[x]['frame'],textvariable=func_dict[x]['high1_var'], width=5).grid(row=1,column=2)
        func_dict[x]['high2_var']  = StringVar()
        func_dict[x]['high2'] = Entry(func_dict[x]['frame'],textvariable=func_dict[x]['high2_var'], width=5).grid(row=1,column=3)
        func_dict[x]['high3_var']  = StringVar()
        func_dict[x]['high3'] = Entry(func_dict[x]['frame'],textvariable=func_dict[x]['high3_var'], width=5).grid(row=1,column=4)
        func_dict[x]['setb'] = Button(func_dict[x]['frame'] , text='set', command=functions_in_order).grid(row=1,column=0)
        func_dict[x]['low1_var'].set('0')
        func_dict[x]['low2_var'].set('140')
        func_dict[x]['low3_var'].set('90')
        func_dict[x]['high1_var'].set('8')
        func_dict[x]['high2_var'].set('255')
        func_dict[x]['high3_var'].set('255')
    elif base=='Circle':
        func_dict[x]['text1'] = Label(func_dict[x]['frame'],text='Min resolution:').grid(row=0, column=1)
        func_dict[x]['text2'] = Label(func_dict[x]['frame'],text='Min distance:').grid(row=1, column=1)
        func_dict[x]['text3'] = Label(func_dict[x]['frame'],text='Internal canny of the circles:').grid(row=0, column=3)
        func_dict[x]['text4'] = Label(func_dict[x]['frame'],text='Accumulation of point needed:').grid(row=1, column=3)
        func_dict[x]['text5'] = Label(func_dict[x]['frame'],text='Min radius:').grid(row=0, column=5)
        func_dict[x]['text6'] = Label(func_dict[x]['frame'],text='Max radius:').grid(row=1, column=5)
        func_dict[x]['dp'] = StringVar()
        func_dict[x]['dist'] =  StringVar()
        func_dict[x]['internal_canny'] =  StringVar()
        func_dict[x]['acumulation'] =  StringVar()
        func_dict[x]['min_rad'] = StringVar()
        func_dict[x]['max_rad'] = StringVar()
        func_dict[x]['dp'].set('1')
        func_dict[x]['dist'].set('20')
        func_dict[x]['internal_canny'].set('50')
        func_dict[x]['acumulation'].set('30')
        func_dict[x]['min_rad'].set('100')
        func_dict[x]['max_rad'].set('500')
        func_dict[x]['dp_entry'] = Entry(func_dict[x]['frame'],textvariable=func_dict[x]['dp'], width=5).grid(row=0,column=2)
        func_dict[x]['dist_entry'] =  Entry(func_dict[x]['frame'],textvariable=func_dict[x]['dist'], width=5).grid(row=1,column=2)
        func_dict[x]['internal_canny_entry'] =  Entry(func_dict[x]['frame'],textvariable=func_dict[x]['internal_canny'], width=5).grid(row=0,column=4)
        func_dict[x]['acumulation_entry'] =  Entry(func_dict[x]['frame'],textvariable=func_dict[x]['acumulation'], width=5).grid(row=1,column=4)
        func_dict[x]['min_rad_entry'] = Entry(func_dict[x]['frame'],textvariable=func_dict[x]['min_rad'], width=5).grid(row=0,column=6)
        func_dict[x]['max_rad_entry'] = Entry(func_dict[x]['frame'],textvariable=func_dict[x]['max_rad'], width=5).grid(row=1,column=6)
        func_dict[x]['setb'] = Button(func_dict[x]['frame'] , text='set', command=functions_in_order).grid(row=1,column=0)
    elif base=='Canny':
        func_dict[x]['lower'] = Scale(func_dict[x]['frame'],label='Lower threshold',orient=HORIZONTAL,
                                      command=functions_in_order,from_=0,to=255)
        func_dict[x]['lower'].grid(row=0, column=1)
        func_dict[x]['lower'].set(100)
        #Scale(cv2_functions, from_=0, to=255,orient=HORIZONTAL, command=add_adaptative_thre)
        func_dict[x]['higher'] = Scale(func_dict[x]['frame'],label='Higher threshold',orient=HORIZONTAL,
                                      command=functions_in_order,from_=0,to=255)
        func_dict[x]['higher'].grid(row=0, column=2)
        func_dict[x]['higher'].set(200)
        func_dict[x]['aperture'] = Scale(func_dict[x]['frame'],label='Aperture size',orient=HORIZONTAL,
                                      command=functions_in_order,from_=0,to=2)
        func_dict[x]['aperture'].set(1)
        func_dict[x]['aperture'].grid(row=0, column=3)
    elif base=='Resize':
        func_dict[x]['new_x_var']  = StringVar()
        func_dict[x]['new_x'] = Entry(func_dict[x]['frame'],textvariable=func_dict[x]['new_x_var'], width=5).grid(row=0,column=2)
        func_dict[x]['new_y_var']  = StringVar()
        func_dict[x]['new_y'] = Entry(func_dict[x]['frame'],textvariable=func_dict[x]['new_y_var'], width=5).grid(row=0,column=3)  
        func_dict[x]['setb'] = Button(func_dict[x]['frame'] , text='set', command=functions_in_order).grid(row=1,column=0)
    elif base=='Blur':
        func_dict[x]['text1'] = Label(func_dict[x]['frame'],text='Kernel sz x:').grid(row=0, column=1)
        func_dict[x]['text2'] = Label(func_dict[x]['frame'],text='Kernel sz y:').grid(row=1, column=1)
        func_dict[x]['text3'] = Label(func_dict[x]['frame'],text='Deviation:').grid(row=3, column=3)
        func_dict[x]['kernelx'] = StringVar()
        func_dict[x]['kernely'] = StringVar()
        func_dict[x]['dev'] = StringVar()
        func_dict[x]['kernelx'].set(5)
        func_dict[x]['kernely'].set(5)
        func_dict[x]['dev'].set(1)
        func_dict[x]['kernelx_entry'] = Entry(func_dict[x]['frame'],textvariable=func_dict[x]['kernelx'], width=5).grid(row=0,column=2)
        func_dict[x]['kernely_entry'] = Entry(func_dict[x]['frame'],textvariable=func_dict[x]['kernely'], width=5).grid(row=1,column=2)
        func_dict[x]['dev_entry'] = Entry(func_dict[x]['frame'],textvariable=func_dict[x]['dev'], width=5).grid(row=0,column=4)
        func_dict[x]['setb'] = Button(func_dict[x]['frame'] , text='set', command=functions_in_order).grid(row=1,column=0)
    elif base=='Erode':
        func_dict[x]['text1'] = Label(func_dict[x]['frame'],text='Kernel sz x:').grid(row=0, column=1)
        func_dict[x]['text2'] = Label(func_dict[x]['frame'],text='Kernel sz y:').grid(row=1, column=1)
        func_dict[x]['text3'] = Label(func_dict[x]['frame'],text='Iterations:').grid(row=3, column=3)
        func_dict[x]['kernelx'] = StringVar()
        func_dict[x]['kernely'] = StringVar()
        func_dict[x]['iter'] = StringVar()
        func_dict[x]['kernelx'].set(5)
        func_dict[x]['kernely'].set(5)
        func_dict[x]['iter'].set(1)
        func_dict[x]['kernelx_entry'] = Entry(func_dict[x]['frame'],textvariable=func_dict[x]['kernelx'], width=5).grid(row=0,column=2)
        func_dict[x]['kernely_entry'] = Entry(func_dict[x]['frame'],textvariable=func_dict[x]['kernely'], width=5).grid(row=1,column=2)
        func_dict[x]['dev_entry'] = Entry(func_dict[x]['frame'],textvariable=func_dict[x]['iter'], width=5).grid(row=0,column=4)
        func_dict[x]['setb'] = Button(func_dict[x]['frame'] , text='set', command=functions_in_order).grid(row=1,column=0)
    elif base=='Dilate':
        func_dict[x]['text1'] = Label(func_dict[x]['frame'],text='Kernel sz x:').grid(row=0, column=1)
        func_dict[x]['text2'] = Label(func_dict[x]['frame'],text='Kernel sz y:').grid(row=1, column=1)
        func_dict[x]['text3'] = Label(func_dict[x]['frame'],text='Iterations:').grid(row=3, column=3)
        func_dict[x]['kernelx'] = StringVar()
        func_dict[x]['kernely'] = StringVar()
        func_dict[x]['iter'] = StringVar()
        func_dict[x]['kernelx'].set(5)
        func_dict[x]['kernely'].set(5)
        func_dict[x]['iter'].set(1)
        func_dict[x]['kernelx_entry'] = Entry(func_dict[x]['frame'],textvariable=func_dict[x]['kernelx'], width=5).grid(row=0,column=2)
        func_dict[x]['kernely_entry'] = Entry(func_dict[x]['frame'],textvariable=func_dict[x]['kernely'], width=5).grid(row=1,column=2)
        func_dict[x]['dev_entry'] = Entry(func_dict[x]['frame'],textvariable=func_dict[x]['iter'], width=5).grid(row=0,column=4)
        func_dict[x]['setb'] = Button(func_dict[x]['frame'] , text='set', command=functions_in_order).grid(row=1,column=0)
    elif base=='White':
        func_dict[x]['text1'] = Label(func_dict[x]['frame'],text='Kernel sz x:').grid(row=0, column=1)
        func_dict[x]['text2'] = Label(func_dict[x]['frame'],text='Kernel sz y:').grid(row=1, column=1)
        func_dict[x]['kernelx'] = StringVar()
        func_dict[x]['kernely'] = StringVar()
        func_dict[x]['kernelx'].set(5)
        func_dict[x]['kernely'].set(5)
        func_dict[x]['kernelx_entry'] = Entry(func_dict[x]['frame'],textvariable=func_dict[x]['kernelx'], width=5).grid(row=0,column=2)
        func_dict[x]['kernely_entry'] = Entry(func_dict[x]['frame'],textvariable=func_dict[x]['kernely'], width=5).grid(row=1,column=2)
        func_dict[x]['setb'] = Button(func_dict[x]['frame'] , text='set', command=functions_in_order).grid(row=1,column=0)
    elif base=='Black':
        func_dict[x]['text1'] = Label(func_dict[x]['frame'],text='Kernel sz x:').grid(row=0, column=1)
        func_dict[x]['text2'] = Label(func_dict[x]['frame'],text='Kernel sz y:').grid(row=1, column=1)
        func_dict[x]['kernelx'] = StringVar()
        func_dict[x]['kernely'] = StringVar()
        func_dict[x]['kernelx'].set(5)
        func_dict[x]['kernely'].set(5)
        func_dict[x]['kernelx_entry'] = Entry(func_dict[x]['frame'],textvariable=func_dict[x]['kernelx'], width=5).grid(row=0,column=2)
        func_dict[x]['kernely_entry'] = Entry(func_dict[x]['frame'],textvariable=func_dict[x]['kernely'], width=5).grid(row=1,column=2)
        func_dict[x]['setb'] = Button(func_dict[x]['frame'] , text='set', command=functions_in_order).grid(row=1,column=0)
    elif base=='Adaptative':
        func_dict[x]['block'] = Scale(func_dict[x]['frame'],label='Neighborhood Block sz',orient=HORIZONTAL,
                                      command=functions_in_order,from_=0,to=150)
        func_dict[x]['block'].grid(row=0,column=1)
        func_dict[x]['constant'] = Scale(func_dict[x]['frame'],label='Constant',orient=HORIZONTAL,
                                      command=functions_in_order,from_=0,to=150)
        func_dict[x]['constant'].grid(row=0,column=2)
        func_dict[x]['start'] = StringVar()
        func_dict[x]['block'].set(5)
        func_dict[x]['constant'].set(1)
        func_dict[x]['start'].set('Gaussian')
        func_dict[x]['button1'] = Radiobutton(func_dict[x]['frame'], text='Gaussian',variable=func_dict[x]['start'],value='Gaussian', command=functions_in_order).grid(row=0,column=3)
        func_dict[x]['button1'] = Radiobutton(func_dict[x]['frame'], text='Mean',variable=func_dict[x]['start'],value='Mean', command=functions_in_order).grid(row=1,column=3)
        func_dict[x]['normal'] = StringVar()
        func_dict[x]['normal'].set('inv')
        func_dict[x]['button1'] = Radiobutton(func_dict[x]['frame'], text='Normal',variable=func_dict[x]['normal'],value='normal', command=functions_in_order).grid(row=0,column=4)
        func_dict[x]['button1'] = Radiobutton(func_dict[x]['frame'], text='Invert',variable=func_dict[x]['normal'],value='inv', command=functions_in_order).grid(row=1,column=4)
    elif base=='Contour':
        func_dict[x]['mode'] = StringVar()
        func_dict[x]['mode'].set('simple')
        func_dict[x]['button1'] = Radiobutton(func_dict[x]['frame'], text='Simple Approch',variable=func_dict[x]['mode'],value='simple', command=functions_in_order).grid(row=0,column=1)
        func_dict[x]['button1'] = Radiobutton(func_dict[x]['frame'], text='All points',variable=func_dict[x]['mode'],value='none', command=functions_in_order).grid(row=1,column=1)
        func_dict[x]['mode2'] = StringVar()
        func_dict[x]['mode2'].set('external')
        func_dict[x]['button1'] = Radiobutton(func_dict[x]['frame'], text='Ret. external',variable=func_dict[x]['mode2'],value='external', command=functions_in_order).grid(row=0,column=2)
        func_dict[x]['button1'] = Radiobutton(func_dict[x]['frame'], text='Ret. Tree',variable=func_dict[x]['mode2'],value='tree', command=functions_in_order).grid(row=1,column=2)
    elif base=='Contour circle':
        func_dict[x]['mode'] = StringVar()
        func_dict[x]['mode'].set('simple')
        func_dict[x]['button1'] = Radiobutton(func_dict[x]['frame'], text='Simple Approch',variable=func_dict[x]['mode'],value='simple', command=functions_in_order).grid(row=0,column=1)
        func_dict[x]['button1'] = Radiobutton(func_dict[x]['frame'], text='All points',variable=func_dict[x]['mode'],value='none', command=functions_in_order).grid(row=1,column=1)
        func_dict[x]['mode2'] = StringVar()
        func_dict[x]['mode2'].set('external')
        func_dict[x]['button1'] = Radiobutton(func_dict[x]['frame'], text='Ret. external',variable=func_dict[x]['mode2'],value='external', command=functions_in_order).grid(row=0,column=2)
        func_dict[x]['button1'] = Radiobutton(func_dict[x]['frame'], text='Ret. Tree',variable=func_dict[x]['mode2'],value='tree', command=functions_in_order).grid(row=1,column=2)
        func_dict[x]['min_radius'] = Scale(func_dict[x]['frame'],label='Min Radius',orient=HORIZONTAL,
                                      command=functions_in_order,from_=0,to=600)
        func_dict[x]['min_radius'].set(400)
        func_dict[x]['min_radius'].grid(row=0,column=3)
    elif base=='Contour rectangle':
        func_dict[x]['mode'] = StringVar()
        func_dict[x]['mode'].set('simple')
        func_dict[x]['button1'] = Radiobutton(func_dict[x]['frame'], text='Simple Approch',variable=func_dict[x]['mode'],value='simple', command=functions_in_order).grid(row=0,column=1)
        func_dict[x]['button1'] = Radiobutton(func_dict[x]['frame'], text='All points',variable=func_dict[x]['mode'],value='none', command=functions_in_order).grid(row=1,column=1)
        func_dict[x]['mode2'] = StringVar()
        func_dict[x]['mode2'].set('external')
        func_dict[x]['button1'] = Radiobutton(func_dict[x]['frame'], text='Ret. external',variable=func_dict[x]['mode2'],value='external', command=functions_in_order).grid(row=0,column=2)
        func_dict[x]['button1'] = Radiobutton(func_dict[x]['frame'], text='Ret. Tree',variable=func_dict[x]['mode2'],value='tree', command=functions_in_order).grid(row=1,column=2)
        func_dict[x]['min_radius'] = Scale(func_dict[x]['frame'],label='Min Radius',orient=HORIZONTAL,
                                      command=functions_in_order,from_=0,to=600)
        func_dict[x]['min_radius'].set(400)
        func_dict[x]['min_radius'].grid(row=0,column=3)
    elif base=='Otsu':
        func_dict[x]['var1'] = Scale(func_dict[x]['frame'],label='Low Thresh',orient=HORIZONTAL,
                                      command=functions_in_order,from_=0,to=255)
        func_dict[x]['var1'].grid(row=0,column=1)
        func_dict[x]['var2'] = Scale(func_dict[x]['frame'],label='Output Value',orient=HORIZONTAL,
                                      command=functions_in_order,from_=0,to=255)
        func_dict[x]['var2'].grid(row=1,column=1)
        func_dict[x]['var1'].set(0)
        func_dict[x]['var2'].set(255)
        func_dict[x]['mode2'] = StringVar()
        func_dict[x]['mode2'].set('0')
        func_dict[x]['button1'] = Radiobutton(func_dict[x]['frame'], text='Binary + Otsu',variable=func_dict[x]['mode2'],value='0', command=functions_in_order).grid(row=0,column=2)
        func_dict[x]['button1'] = Radiobutton(func_dict[x]['frame'], text='Invert Binary + Otsu',variable=func_dict[x]['mode2'],value='1', command=functions_in_order).grid(row=1,column=2)
    functions_in_order()
    variable.set(OPTIONS[0])

    
    
def functions_in_order(none_param='none_param'):
    #In the for loop add the template creation
    global frame
    frame = image
    if len(mask_list) > 2:
        mask = np.zeros(frame.shape[0:2], dtype=np.uint8)
        points = np.array(mask_list)
        mask = cv2.drawContours(mask, [points], -1, (255, 255, 255), -1, cv2.LINE_AA)
        frame = cv2.bitwise_and(frame,frame,mask = mask)
    state = ''
    print('Func list: ', func_list)
    for i in func_list:
        frame, state = cv2_func_pack(i[0],frame,func_dict[i[1]])
    if state == 'gray':
         frame = cv2.cvtColor(frame,cv2.COLOR_GRAY2RGB)
    elif state== 'hsv':
        frame = cv2.cvtColor(frame,cv2.COLOR_HSV2RGB)
    else:
        frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    if len(mask_list) > 2:
        frame = cv2.cvtColor(frame,cv2.COLOR_RGB2BGR)
        frame2 = image
        res = cv2.bitwise_and(frame,frame,mask = mask)
        cv2.imwrite('ex1.jpg',frame2)
        mask2 =  cv2.bitwise_not(mask)
        frame2 = cv2.bitwise_or(frame2,frame2,mask =mask2 )
        cv2.imwrite('ex2.jpg',frame2)
        frame = cv2.bitwise_or(frame2, res)
        frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        
    
    image_rz = cv2.resize(frame, (400,400))
    to_display = Image.fromarray(image_rz )  
    to_display2 = ImageTk.PhotoImage(image=to_display)             
    image_label.configure(image=to_display2)
    image_label.image = to_display2
    print(func_dict)

### Mask creator        
def mask_creator(event):
    x_rel = image_label.winfo_rootx()
    y_rel = image_label.winfo_rooty()
    x_rel2 = image_frame.winfo_rootx()
    y_rel2 = image_frame.winfo_rooty()
    rex =  event.x - (x_rel-x_rel2)
    rey =  event.y - (y_rel-y_rel2) + 36
    rep_x, rep_y = int(((event.x)/4)*abs_width/100), int(((event.y)/4)*abs_height/100)
    print('hello',event.x,event.y,'abs', abs_height, abs_width,'repara',rep_x, rep_y)       
    mask_list.append((rep_x, rep_y))
    if len(mask_list) > 2:
        functions_in_order()
    print(mask_list)
    mask_points.delete("1.0","end")
    mask_points.insert(END, f"{mask_list}")
    
def reset_mask(event):
    mask_list.clear()
    mask_points.delete("1.0","end")
    functions_in_order()
    
def function_leave(event):
    root.unbind('<Button-1>')
    root.unbind("<BackSpace>")
    image_label.bind("<Enter>", function_enter)
    
def function_enter(event):
    root.bind('<Button-1>', mask_creator)
    root.bind("<space>", reset_mask)
    image_label.bind("<Leave>", function_leave)

#####Downloads
def download_file(file_type):
    if file_type=='image':
        filename = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("Image files", "*.jpg"), ("All Files", "*.*")])
        if filename:
            frame = cv2.cvtColor(frame,cv2.COLOR_RGB2BGR)
            cv2.imwrite(f'{filename}.jpg',frame)
    if file_type=='params':
        try:
            functions_in_order()
            filename = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("Image files", "*.jpg"), ("All Files", "*.*")])
        except:
            print("Error")
        
        
#####


##### Zoom function
# def zoom_in_out(event):
#     global scale_factor
#     if event.delta > 0:
#         scale_factor = 1.2
#     else:
#         scale_factor = 0.8
#     update_image()

# def update_image():
#     width = int(frame.shape[1] * scale_factor)
#     height = int(frame.shape[0] * scale_factor)
#     resized_image = frame.resize((width, height), Image.ANTIALIAS)
#     self.photo = ImageTk.PhotoImage(resized_image)
#     self.label.config(image=self.photo)
#  "<MouseWheel>"   
#####
###################GUI           
#Main        
root = Tk()
root.title("OpenCV GUI")

#File dialog and image display
image_frame = LabelFrame(root)
file_button = Button(image_frame,text="Open File", command=open_file)
image_frame.grid(row=0,column=0)
file_button.grid(row=0,column=0,pady=5,padx=5)
image_label = Label(image_frame)
image_label.grid(column=0,row=1)
image_label.bind("<Enter>", function_enter)
mask_text = Label(image_frame, text="You can select a mask by clicking on the img (Delete with backspace, min 3 points)",height=1, borderwidth=0)
#mask_text.configure(state="disabled")
mask_text.grid(column=0,row=2)
mask_points = Text(image_frame,height=1,width=50)
#mask_points.configure(state="disabled")
mask_points.grid(column=0,row=3)
#Code: Not yet
code_frame = LabelFrame(root,text="Code")
code_frame.grid(row=0,column=1)      
#Download Image, Parameters and Code
download_frame = LabelFrame(root,text="Downloads")
download_frame.grid(row=2,column=0)
image_button = Button(download_frame, text="File", command=lambda:download_file('image') )
code_button = Button(download_frame,text="Params", command=lambda:download_file('code') )
code_button.pack()
#Option menu  
option_frame = LabelFrame(root,text="Select a function")
option_frame.grid(row=3,column=0)  
variable = StringVar(option_frame)
variable.set(OPTIONS[0]) # default value
w = OptionMenu(option_frame, variable, *OPTIONS, command=option_menu)
w.pack()
        
#Display options
display_frame = LabelFrame(root,text="Tune the function")
display_frame.grid(row=0,column=1)  
        
if __name__ =='__main__':
    root.mainloop()
    #Code + params
    #Params first then code