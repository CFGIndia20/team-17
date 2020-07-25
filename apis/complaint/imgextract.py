import os
import cv2
from PIL import Image
import imagehash
import glob
  

def extract_images(vloc):
        
    # Read the video from specified path 
    cam = cv2.VideoCapture(vloc) 
    
    try: 
        
        # creating a folder named data 
        if not os.path.exists('data'): 
            os.makedirs('data') 
    
    # if not created then raise error 
    except OSError: 
        print ('Error: Creating directory of data') 
    
    # frame 
    currentframe = 0
    
    while(True): 
        
        # reading from frame 
        ret,frame = cam.read() 
    
        if ret:
            if(currentframe%30==0):
                # location to store the image
                name = './data/frame' + str(currentframe) + '.jpg'
                print ('Creating...' + name) 
        
                # writing the extracted images 
                cv2.imwrite(name, frame) 
        
            # increasing counter so that it will 
            # show how many frames are created 
            currentframe += 1
        else: 
            break
    
    # Release all space and windows once done 
    cam.release() 
    cv2.destroyAllWindows() 


def delete_similar_images():
    img_list=(glob.glob("./data/*.jpg"))
    cutoff = 10
    if(len(img_list)>0):
        mem_img= imagehash.average_hash(Image.open(img_list[0]))
        for loc in range(1,len(img_list)):
            new_image = imagehash.average_hash(Image.open(img_list[loc]))

            if abs(new_image - mem_img) < cutoff:
                # print('images are similar')
                os.remove(img_list[loc])
            else:
                # print('images are not similar')
                mem_img=imagehash.average_hash(Image.open(img_list[loc]))
    else:
        print("Error: No images")


if __name__=="__main__":
    #vloc -> input video location
    vloc=r"C:\Users\sidha\Desktop\evideo\trial.mp4"
    extract_images(vloc)
    delete_similar_images()