from PIL import ImageGrab
import threading
import time
import cv2
import pyautogui
import numpy as np
from queue import Queue
import importlib
# from PocketOptionUI import PocketOptionUI




class PocketOption():
    def __init__(self):
        # super().__init__(PocketOption)
       
        self.bulls_power = Queue()
        self.miss_bull_power=0
        self.miss_rate=0
        self.rate_of_change=Queue()
        self.prev_bulls_power=None
        self.prev_rate_of_change=None
        self.thread_status=False
        self.indicator_status=True
        # self.base_class = importlib.import_module('PocketOptionUI')
        # self.base_instance = self.base_class.PocketOptionUI()

    def detect_color_lines(self,pocket_option_frame,color):

        if(color=="pink"):

            hsv = cv2.cvtColor(pocket_option_frame, cv2.COLOR_BGR2HSV)
            lower_pink = np.array([140, 100, 100])
            upper_pink = np.array([170, 255, 255])
            pink_mask = cv2.inRange(hsv, lower_pink, upper_pink)
            kernel = np.ones((5, 5), np.uint8)
            pink_mask = cv2.morphologyEx(pink_mask, cv2.MORPH_CLOSE, kernel)
            pink_mask = cv2.morphologyEx(pink_mask, cv2.MORPH_OPEN, kernel)
            contours, _ = cv2.findContours(pink_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            output_image = np.zeros_like(pocket_option_frame)

            for contour in contours:
                epsilon = 0.02 * cv2.arcLength(contour, True)
                approx = cv2.approxPolyDP(contour, epsilon, True)
                cv2.drawContours(output_image, [approx], 0, (255, 0, 255), 2)

        elif(color=="orange"):
            hsv = cv2.cvtColor(pocket_option_frame, cv2.COLOR_BGR2HSV)
            lower_orange = np.array([10, 100, 100])
            upper_orange = np.array([20, 255, 255])
            orange_mask = cv2.inRange(hsv, lower_orange, upper_orange)
            kernel = np.ones((5, 5), np.uint8)
            orange_mask = cv2.morphologyEx(orange_mask, cv2.MORPH_CLOSE, kernel)
            orange_mask = cv2.morphologyEx(orange_mask, cv2.MORPH_OPEN, kernel)
            contours, _ = cv2.findContours(orange_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            output_image = np.zeros_like(pocket_option_frame)

            for contour in contours:
                epsilon = 0.02 * cv2.arcLength(contour, True)
                approx = cv2.approxPolyDP(contour, epsilon, True)
                cv2.drawContours(output_image, [approx], 0, (0, 165, 255), 2)

        return output_image

    def matrix_conversion(self,image):
        bw_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        _, binary_matrix = cv2.threshold(bw_image, 10, 1, cv2.THRESH_BINARY)

        # cv2.imshow('Original Image', image)
        # cv2.imshow('Binary Matrix Image', binary_matrix.astype(np.uint8) * 255)

        return binary_matrix




    def capture_active_window_screen(self):

        index=0
        try:
            while self.thread_status:
                print("hello")
                bull_bool=True
                rate_bool=True
                screenshot = pyautogui.screenshot()
                frame = np.array(screenshot)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                detect_yellow_thread=threading.Thread(target=lambda:self.bulls_power.put(self.detect_color_lines(frame,"pink")))
                detect_yellow_thread.start()

                detect_orange_thread=threading.Thread(target=lambda:self.rate_of_change.put(self.detect_color_lines(frame,"orange")))
                detect_orange_thread.start()

                detect_yellow_thread.join()
                detect_orange_thread.join()




                bull=self.bulls_power.get()
                rate=self.rate_of_change.get()

                bulls_matrix=self.matrix_conversion(bull).astype(np.uint8) * 255


                rate_matrix=self.matrix_conversion(rate).astype(np.uint8) * 255
                # cv2.imwrite('orange_matrix'+str(index)+'.jpg', orange_matrix)
                # cv2.imshow("hello",orange_matrix)

                if(self.prev_bulls_power is None):
                    self.prev_bulls_power=bulls_matrix

                if(self.prev_rate_of_change is None):
                    self.prev_rate_of_change=rate_matrix

                if(self.prev_bulls_power is not None and self.prev_rate_of_change is not None):
                    if(np.array_equal(self.prev_rate_of_change,rate_matrix)):
                        if(not np.array_equal(self.prev_bulls_power,bulls_matrix)):
                            # cv2.imwrite('bulls_matrix'+str(index)+'.jpg', bulls_matrix)
                            # cv2.imwrite('rate'+str(index)+'.jpg', rate_matrix)
                            # cv2.imwrite('prev_bulls_matrix'+str(index)+'.jpg', self.prev_bulls_power)
                            # cv2.imwrite('prev_rate'+str(index)+'.jpg', self.prev_rate_of_change)


                            # np.savetxt("bulls_prev.txt", self.prev_bulls_power)

                            
                            # np.savetxt("bulls.txt",bulls_matrix)

                            
                            # np.savetxt("rate_prev.txt",self.prev_rate_of_change)

                            
                            # np.savetxt("rate.txt",rate_matrix)
                            rate_bool=False
                            print("first")

                            

                    if(np.array_equal(self.prev_bulls_power,bulls_matrix)):
                        if(not np.array_equal(self.prev_rate_of_change,rate_matrix)):
                            # cv2.imwrite('bulls_matrix'+str(index)+'.jpg', bulls_matrix)
                            # cv2.imwrite('rate'+str(index)+'.jpg', rate_matrix)
                            # cv2.imwrite('prev_bulls_matrix'+str(index)+'.jpg', self.prev_bulls_power)
                            # cv2.imwrite('prev_rate'+str(index)+'.jpg', self.prev_rate_of_change)
                            
                            # np.savetxt("bulls_prev.txt", self.prev_bulls_power)

                            
                            # np.savetxt("bulls.txt",bulls_matrix)

                            
                            # np.savetxt("rate_prev.txt",self.prev_rate_of_change)

                            
                            # np.savetxt("rate.txt",rate_matrix)
                            bull_bool=False
                            print("second")
                if(bull_bool==False):
                    self.indicator_status=False
                    self.miss_bull_power+=1

                if(rate_bool==False):
                    self.indicator_status=False
                    self.miss_rate+=1

                # if(bull_bool==True and miss_rate==True):
                #     self.indicator_status=True

                            
                            
                

                self.prev_bulls_power=bulls_matrix
                self.prev_rate_of_change=rate_matrix



                # cv2.imshow("hello",result)

                
                # cv2.imwrite('rate'+str(index)+'.jpg', rate)
                index+=1

                if cv2.waitKey(1) == ord('q'):
                    break
        finally:
            cv2.destroyAllWindows()




    def Main_App(self):
        time.sleep(5)
        self.capture_active_window_screen()
        





# if __name__ == "__main__":
#     # time.sleep(3)
#     PO=PocketOption()
#     PO.Main_App()
    
