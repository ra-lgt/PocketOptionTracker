import customtkinter
import tkinter as tk
import os
import configparser
from PocketOptionApp import PocketOption
import time
from threading import Thread
from PIL import Image, ImageTk
from ttkbootstrap.dialogs.dialogs import Messagebox




class PocketOptionUI(PocketOption):
	def __init__(self):
		super().__init__()

		
		self.root = customtkinter.CTk(fg_color="#212121")
		self.root.geometry("400x300")
		self.root.title("Pocket Option Tracker")
		
		# self.miss_bull_power=0
		# self.miss_rate=0
		# self.PO=PocketOption()
		self.backend_thread=None
		self.delete_frames=[]
		self.Flag=True
		self.custom_images={
		'red':customtkinter.CTkImage(light_image=Image.open("./static/red.png"),size=(30, 30)),
		'green':customtkinter.CTkImage(light_image=Image.open("./static/green.png"),size=(30, 30)),
		}
		
		

	def create_config_file(self):
		if(os.path.isfile('./config.ini')):
			return
		else:
			self.config['user-data']={
			'Bull_Power_Line_Color':"None",
			'Rate_Of_Change_Line_Color':"None"
			}
			with open('config.ini', 'w') as configfile:
				self.config.write(configfile)

	
	def save_config(self,bull_value,rate_value):
		if(bull_value.get()=="None" or rate_value.get()=="None"):
			Messagebox.show_error(message="Provide the two values")
			self.Home_page()
		else:

			self.config['user-data']['bull_power_line_color']=bull_value.get()
			self.config['user-data']['rate_of_change_line_color']=rate_value.get()

			with open('config.ini', 'w') as config_file:
				self.config.write(config_file)

			track_thread=Thread(target=self.Tracker_Page)
			track_thread.start()

		# self.Tracker_Page()

	def backend_call(self):
		
		
		self.thread_status=True
		self.backend_thread=Thread(target=self.Main_App)
		self.backend_thread.start()

	def stop_track(self):
		
		
		self.thread_status=False

	def start_track(self):
		# self.info=customtkinter.CTkLabel(master=self.root, text="Hold ON! Tightly we're going to track",text_color="#E0E0E0",font=("Arial",15))
		# self.info.place(relx=0.2,rely=0.9)
		self.backend_call()


	def event_tracker(self):
		prev_miss_bull=self.miss_bull_power
		while True:
			print()
			
			if(prev_miss_bull!=self.miss_bull_power):
				self.Flag=False
				print("**")
				self.Tracker_Page()

				prev_miss_bull=self.miss_bull_power

		




	def Tracker_Page(self):
		for i in self.delete_frames:
			i.destroy()
			i.pack_forget()

		if self.Flag:

			temp=Thread(target=self.event_tracker)
			temp.start()

		

		tracker_frame=customtkinter.CTkFrame(master=self.root, width=400, height=400,fg_color="#212121")
		tracker_frame.place(rely=0.2)

		miss_bull_power_label=customtkinter.CTkLabel(master=tracker_frame, text="Bull-Power Misses",text_color="#E0E0E0",font=("Arial",15))
		miss_bull_power_label.grid(row=0,column=0,sticky=tk.W)

		temp=customtkinter.CTkLabel(master=tracker_frame, text=":",text_color="#E0E0E0",font=("Arial",15))
		temp.grid(row=0,column=1,padx=10,sticky=tk.E)

		miss_bull_power_count=customtkinter.CTkLabel(master=tracker_frame, text=self.miss_bull_power,text_color="#E0E0E0",font=("Arial",15))
		miss_bull_power_count.grid(row=0,column=2,sticky=tk.E)

		miss_rate_label=customtkinter.CTkLabel(master=tracker_frame, text="Rate-Change Misses",text_color="#E0E0E0",font=("Arial",15))
		miss_rate_label.grid(row=1,column=0,sticky=tk.W)

		temp_2=customtkinter.CTkLabel(master=tracker_frame, text=":",text_color="#E0E0E0",font=("Arial",15))
		temp_2.grid(row=1,column=1,padx=10,sticky=tk.E)

		miss_rate_count=customtkinter.CTkLabel(master=tracker_frame, text=self.miss_rate,text_color="#E0E0E0",font=("Arial",15))
		miss_rate_count.grid(row=1,column=2,sticky=tk.E)

		# same_label=customtkinter.CTkLabel(master=tracker_frame, text="Same-Time",text_color="#E0E0E0",font=("Arial",15))
		# same_label.grid(row=2,column=0,sticky=tk.W)

		# if(self.indicator_status==True):
		# 	same = customtkinter.CTkLabel(tracker_frame,image=self.custom_images['green'],text="")
		# 	same.grid(row=2,column=1,sticky=tk.E)
		# else:
		# 	same = customtkinter.CTkLabel(tracker_frame,image=self.custom_images['red'],text="")
		# 	same.grid(row=2,column=1,sticky=tk.E)
			
		


		



		go_button=customtkinter.CTkButton(self.root, text="Track", command=lambda :self.start_track(),fg_color="#149C58")
		go_button.place(relx=0.1,rely=0.8)

		stop_button=customtkinter.CTkButton(self.root, text="Stop", command=lambda :self.stop_track(),fg_color="#94090D")
		stop_button.place(relx=0.6,rely=0.8)

		



	def Home_page(self):
		for i in self.delete_frames:
			i.destroy()
			i.pack_forget()

		bull_power_line_color=None
		rate_of_change_line_color=None

		self.create_config_file()

		bull_power_line_color,rate_of_change_line_color=self.fetch_data_from_config()

		home_frame=customtkinter.CTkFrame(master=self.root, width=400, height=400,fg_color="#212121")
		home_frame.place(rely=0.2)

		bulls_power_label=customtkinter.CTkLabel(master=home_frame, text="Bulls-Power Line color :",text_color="#E0E0E0",font=("Arial",15))
		bulls_power_label.grid(row=0,column=0,sticky=tk.W)

		

		bull_option = customtkinter.CTkOptionMenu(home_frame,dynamic_resizing=False,values=["Light Green", "Blue","Pink","Orange","Red","Yellow"],width=120,fg_color="#0D9488",button_color="#0D9488",dropdown_hover_color="#0D9488")
		bull_option.set(bull_power_line_color)
		bull_option.grid(row=0,column=1,padx=5,sticky=tk.E)

		rate_power_label=customtkinter.CTkLabel(master=home_frame,text="Rate-Change Line color :",text_color="#E0E0E0",font=("Arial",15))
		rate_power_label.grid(row=1,column=0,pady=10,sticky=tk.W)

		rate_option = customtkinter.CTkOptionMenu(home_frame,dynamic_resizing=False,values=["LightGreen", "Blue","Pink","Orange","Red","Yellow"],width=120,fg_color="#0D9488",button_color="#0D9488",dropdown_hover_color="#0D9488")
		rate_option.set(rate_of_change_line_color)
		rate_option.grid(row=1,column=1,padx=5,pady=10,sticky=tk.E)


		go_button=customtkinter.CTkButton(self.root, text="Save", command=lambda :self.save_config(bull_option,rate_option))
		go_button.place(relx=0.3,rely=0.8)

		self.delete_frames.append(home_frame)
		self.delete_frames.append(go_button)






	def Main_UI_App(self):
		self.Home_page()

		title= customtkinter.CTkLabel(master=self.root, text="Pocket Option Tracker", text_color="#E0E0E0",font=("Arial",15))
		title.place(relx=0.35)

		self.root.mainloop()




app=PocketOptionUI()
app.Main_UI_App()
