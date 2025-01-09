import tkinter as tk
from tkinter import ttk as ttk
from tkinter import *
from tkinter import messagebox
from PIL import ImageTk,Image
import google.generativeai as palm
import webbrowser
import socket
import threading


def open_url1():
    webbrowser.open_new("https://aistudio.google.com/app/apikey")


def api_page_func():
    global api_entry, api_page
    api_page = tk.Tk()
    api_page.geometry('400x200')
    api_page.title('Repair The Page - API Key')
    api_page.config(bg='black')
    api_page.iconbitmap("Icon.ico")

    Label(api_page, text="Enter API Key", font=("arial", 12, 'bold'), background='Black', foreground='White').place(relx=0.5, rely=0.3, anchor=CENTER)
    api_entry = Entry(api_page)
    api_entry.place(relx=0.5, rely=0.4, anchor=CENTER, width=250)

    link_label = Label(api_page, text="Get API Key CLICK HERE", font=("arial", 10), bg='black',fg='lightblue', cursor="hand2")
    link_label.place(relx=0.5, rely=0.6, anchor=CENTER, height=20)
    link_label.bind("<Button-1>", lambda event: open_url1())     
    
    Button(api_page, text="Enter Key", font=("italic_iv50", 10), command=check_api_key).place(relx=0.5, rely=0.9, anchor=CENTER)
    
    screen_width = api_page.winfo_screenwidth()
    screen_height = api_page.winfo_screenheight()
    window_width = 400  
    window_height = 200
    x = int((screen_width - window_width) / 2)
    y = int((screen_height - window_height) / 2)
    api_page.geometry("+{}+{}".format(x, y))
    
    api_page.mainloop()


def check_api_key():
    api_key = api_entry.get()

    if not api_key:
        messagebox.showerror("Error", "Please enter API key.")
    else:
        try:
            palm.configure(api_key=api_key)
            models = [m for m in palm.list_models() if 'generateText' in m.supported_generation_methods]
            if not models:
                messagebox.showerror("Error", "No models available.")
            else:
                api_page.destroy()
                prompt_page_func()
        except Exception as e:
            print(e)
            messagebox.showerror("Error", f"Invalid API key")
            

def prompt_page_func():
    global prompt_text_widget1,prompt_text_widget2,ip1, ip2

    prompt_page = tk.Tk()
    prompt_page.geometry('1000x700')
    prompt_page.title('Repair The Page - Prompt Page')
    prompt_page.state('zoomed')
    prompt_page.iconbitmap("Icon.ico")
    prompt_pagepic=ImageTk.PhotoImage(Image.open("BG.png"))
    prompt_pagepicpanel=Label(prompt_page,image=prompt_pagepic)
    prompt_pagepicpanel.pack(side='top',fill='both',expand='yes')

    Label(prompt_page, text="Enter Prompt",bg='black',fg='white', font=("italic_iv50", 12)).place(relx=0.1, rely=0.05)

    prompt_text_widget1 = Text(prompt_page, wrap=WORD, width=80, height=8.5, font=("italic_iv50", 10))
    prompt_text_widget1.place(relx=0.1, rely=0.1)
    
    prompt_text_widget2 = Text(prompt_page, wrap=WORD, width=80, height=23,bg='black',fg='white', font=("italic_iv50", 10))
    prompt_text_widget2.place(relx=0.1, rely=0.35)
    prompt_text_widget2.config(state="disabled")
    
    generate_button = Button(prompt_page, text="Generate Text", font=("italic_iv50", 12), width = 12, command=generate_text)
    generate_button.place(relx=0.8, rely=0.3, anchor=CENTER)
    
    del_button = Button(prompt_page, text="Delete Promt", font=("italic_iv50", 12), width = 12, command=clear_text)
    del_button.place(relx=0.8, rely=0.4, anchor=CENTER)
    
    cost_button = Button(prompt_page, text="Cost Info", font=("italic_iv50", 12), width = 12, command=cost_cri)
    cost_button.place(relx=0.8, rely=0.5, anchor=CENTER)
    
    ip1 = Entry(prompt_page)
    ip1.place(relx=0.7, rely=0.6, anchor=CENTER)
    pt_button = Button(prompt_page, text="Send Promt", font=("italic_iv50", 12), width = 12, command=send_text)
    pt_button.place(relx=0.8, rely=0.6, anchor=CENTER)
    
    ip2 = Entry(prompt_page)
    ip2.place(relx=0.7, rely=0.7, anchor=CENTER)
    rc_button = Button(prompt_page, text="Receive Promt", font=("italic_iv50", 12), width = 12, command=rev_text)
    rc_button.place(relx=0.8, rely=0.7, anchor=CENTER)

    prompt_page.mainloop()
    
    
def cost_cri():
    messagebox.showinfo("Cost Details", """""")


def generate_text():
    prompt_text = prompt_text_widget1.get("1.0", "end-1c")

    if not prompt_text.strip():
        messagebox.showerror("Error", "Please enter prompt text.")
        return

    try:
        model = palm.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt_text)
        response = response.text
        prompt_text_widget2.config(state="normal")
        prompt_text_widget2.delete("1.0", END)
        prompt_text_widget2.insert(END, response)
        prompt_text_widget2.config(state="disabled")
        
        with open('Result_file.txt', 'w') as f:
            
            result = "=================================================\n===================== PROMT =====================\n=================================================\n\n" + prompt_text + "\n\n=================================================\n===================== RESULT ====================\n=================================================\n\n" + response
            
            f.write(result + '\n')

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

    
def clear_text():
    prompt_text_widget1.delete("1.0", END)
    prompt_text_widget2.config(state="normal")
    prompt_text_widget2.delete("1.0", END)
    prompt_text_widget2.config(state="disabled")
    

def send_text():
    host = ip1.get()
    port = 22041

    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, port))
        
        with open("Result_file.txt", 'r') as f:
            message = f.read()
            client_socket.sendall(message.encode())
        
        clear_text()
        ip1.delete(0, END)
        
        messagebox.showinfo("Success", "Message sent successfully!")
    
    except FileNotFoundError:
        messagebox.showerror("Error", "Result_file.txt not found.")
    
    except ConnectionRefusedError:
        messagebox.showerror("Error", "Connection refused. Please check the server IP and port.")
    
    except socket.error as e:
        messagebox.showerror("Socket Error", f"An error occurred: {e}")
    
    finally:
        try:
            client_socket.close()
        except:
            pass


def rev_text():
    def handle_connection():
        port = 22041
        host = ip2.get()
        
        clear_text()
        prompt_text_widget1.insert(END, 'Connecting...')

        try:
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.bind((host, port))
            server_socket.listen(1)
        
            client_socket, client_address = server_socket.accept()
            response = client_socket.recv(1024).decode('utf-8') 
            
            clear_text()
            prompt_text_widget1.insert(END, response)

            client_socket.close()
        except Exception as e:
            messagebox.showerror("Error", f"Connection failed: {e}")
        finally:
            server_socket.close()
    
    threading.Thread(target=handle_connection, daemon=True).start()


icon = tk.Tk()
icon.title('Repair The Page')
icon.iconbitmap("Icon.ico")
image = Image.open("Front.png")
tk_image = ImageTk.PhotoImage(image)
image_label = tk.Label(icon, image=tk_image)
image_label.pack()
icon.update()
screen_width = icon.winfo_screenwidth()
screen_height = icon.winfo_screenheight()
window_width = 432  
window_height = 171
x = int((screen_width - window_width) / 2)
y = int((screen_height - window_height) / 2)
icon.geometry("+{}+{}".format(x, y))
icon.after(2000, icon.destroy)
icon.mainloop()

api_page_func()

