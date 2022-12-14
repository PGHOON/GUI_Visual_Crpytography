import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageDraw, ImageTk
from random import SystemRandom

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        
        #root window
        self.title('Visual Cryptography')
        self.geometry('800x450')
        self.resizable(False, False)

        #button
        self.button = tk.Button(self, text='Encrpyt Image')
        self.button['command'] = self.Encrypt
        self.button.pack()

        self.button2 = tk.Button(self, text='Search Image')
        self.button2['command'] = self.Search
        self.button2.pack()

        #label
        self.label1 = tk.Label(self, text=' ')
        self.label2 = tk.Label(self, text=' ')

        #menu
        menubar = Menu(self)
        self.config(menu=menubar)

    def Encrypt(self):
        random = SystemRandom()
        xrange = range

        selected_img = f'{self.file}'
        img = Image.open(selected_img)

        converted_img = img.convert('1')

        width = img.size[0]*2
        height = img.size[1]*2

        encrypted_A = Image.new('1', (width, height))
        encrypted_B = Image.new('1', (width, height))
        draw_A = ImageDraw.Draw(encrypted_A)
        draw_B = ImageDraw.Draw(encrypted_B)

        patterns = ((1, 1, 0, 0), (1, 0, 1, 0), (1, 0, 0, 1),
                    (0, 1, 1, 0), (0, 1, 0, 1), (0, 0, 1, 1))

        for x in xrange(0, int(width/2)):
            for y in xrange(0, int(height/2)):
                pixel = converted_img.getpixel((x, y))
                pattern = random.choice(patterns)

                draw_A.point((x*2, y*2), pattern[0])
                draw_A.point((x*2+1, y*2), pattern[1])
                draw_A.point((x*2, y*2+1), pattern[2])
                draw_A.point((x*2+1, y*2+1), pattern[3])
                if pixel == 0:
                    draw_B.point((x*2, y*2), 1-pattern[0])
                    draw_B.point((x*2+1, y*2), 1-pattern[1])
                    draw_B.point((x*2, y*2+1), 1-pattern[2])
                    draw_B.point((x*2+1, y*2+1), 1-pattern[3])
                else:
                    draw_B.point((x*2, y*2), pattern[0])
                    draw_B.point((x*2+1, y*2), pattern[1])
                    draw_B.point((x*2, y*2+1), pattern[2])
                    draw_B.point((x*2+1, y*2+1), pattern[3])
        
        encrypted_A.save(f'{self.file}_A.png', 'PNG')
        encrypted_B.save(f'{self.file}_B.png', 'PNG')
        self.button['text'] = 'Done!'

    def Search(self):
        global preview_img
        self.file = filedialog.askopenfilename(initialdir='', title='Choose a file to encrypt',
    filetypes=(('png files', '*.png'), ('all files', '*.*')))
        self.label1 = tk.Label(self, text=self.file).pack()
        preview_img = ImageTk.PhotoImage(Image.open(self.file))
        self.label2 = tk.Label(image=preview_img).pack()

class Menu(tk.Menu):
    def __init__(self, parent):
        tk.Menu.__init__(self, parent)

        #file
        file = tk.Menu(self, tearoff=False)
        self.add_cascade(label='File',underline=0, menu=file)
        file.add_command(label='Exit', underline=1, command=self.destroy)

        #help
        hellp = tk.Menu(self, tearoff=False)
        self.add_cascade(label='Help',underline=0, menu=hellp)