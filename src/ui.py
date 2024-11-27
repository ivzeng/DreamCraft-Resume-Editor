"""
File: ui.py

Description:
    This module contains a GraphicalUserInterface class. It cantains functions to
open a GUI, create/display various widgets with tkinter, and configure GUI styles.
"""



import tkinter as tk
import tkinter.scrolledtext as st
from tkinter import messagebox 
from PIL import Image, ImageTk
class GraphicalUserInterface:
    '''
    A GUI class through tkinter
    '''
    DEFAULT_WIDTH = 1000
    DEFAULT_HEIGHT = 600
    COL_DEFAULT = "white"
    COL_RED_0 = "#FFD1D1"
    COL_RED_1 = "#FF6767"
    COL_RED_2 = "#FE0606"
    COL_RED_3 = "#DF0101"
    COL_ORANGE_0 = "#FFF0DB"
    COL_ORANGE_1 = "#FFD59A"
    COL_ORANGE_2 = "#FE9A0D"
    COL_ORANGE_3 = "#CF7A01"
    COL_YELLOW_0 = "#FFFCB7"
    COL_YELLOW_1 = "#FFFA73"
    COL_YELLOW_2 = "#FFF601"
    COL_YELLOW_3 = "#DCD501"
    COL_GREEN_0 = "#D0FFCB"
    COL_GREEN_1 = "#A1FF96"
    COL_GREEN_2 = "#45FA02"
    COL_GREEN_3 = "#13B900"
    COL_SKY_0 = "#C5F2FF"
    COL_SKY_1 = "#84E3FF"
    COL_SKY_2 = "#07C5FF"
    COL_SKY_3 = "#019FCE"
    COL_BLUE_0 ="#B6E6FF"
    COL_BLUE_1 = "#55C7FF"
    COL_BLUE_2 = "#01A9FD"
    COL_BLUE_3 = "#008BD0"
    COL_PURPLE_0 = "#E3CCFD"
    COL_PURPLE_1 = "#C186FF"
    COL_PURPLE_2 = "#7B01FD"
    COL_PURPLE_3 = "#5200A9"
    COL_PINK_0 = "#FFA7D2"
    COL_PINK_1 = "#FC469E"
    COL_PINK_2 = "#FF077F"
    COL_PINK_3 = "#CA0163"
    COL_GRAY_0 = "#EEEEEE"
    COL_GRAY_1 = "#C9C9C9"
    COL_GRAY_2 = "#8A8A8A"
    COL_GRAY_3 = "#646464"

    COL_LIME = "#B5F802"
    COL_SEAFOAM = "#71FFD1"
    COL_IVORY = "#FFFFF0"
    COL_PALE_GREEN = "#F0FFF0"

    FONT_FAMILY_1 = "Raleway"
    FONT_FAMILY_2 = "Consolas"
    FONT_FAMILY_3 = "Calibri"


    def __init__(self,
                 title="window",
                 width=DEFAULT_WIDTH,
                 height=DEFAULT_HEIGHT):
        self.state = 'start'
        self.threads = list()
        self.title = title
        self.root = tk.Tk()
        self.root.geometry(f'{width}x{height}')
        self.root.title(title)
        self.frames: dict[str, tuple[tk.Canvas, tk.Frame, dict[str, tk.Widget]]] = dict()
        self.set_menu(command_graph=[['file', [['exit', self.exit]]], ['help', None]])
        self.set_frame(background="grey", x=0, y=0, relheight=1, relwidth=1)
        self.root.bind("<Configure>", self.on_resize)
        self.root.protocol("WM_DELETE_WINDOW", self.exit)
        self.geometry = [width, height]

    def proc(self):
        self.state = 'proc'
        self.root.mainloop()
    
    def exit(self):
        self.state = 'exit'
        self.root.withdraw()
        for t in self.threads:
            t.join()
        self.root.quit()

    def push_thread(self, thread):
        self.threads.append(thread)

    @property
    def get_state(self):
        return self.state

    def clear_frame_content(self, frame_tag = 'frame_0'):
        widgets = self.frames[frame_tag][2]
        for tag in widgets.keys():
            if tag[-9:] == "scrollbar":
                continue
            widget = widgets[tag]
            if widget.winfo_manager():
                widgets[tag].place_forget()
                widgets[tag].pack_forget()

    
    def clear_frame(self, frame_tag = 'frame_0'):
        self.frames[frame_tag][0].place_forget()

    def on_resize(self, event):
        w, h = self.root.winfo_width(), self.root.winfo_height()
        if w == self.geometry[0] and h == self.geometry[1]:
            return
        self.geometry = [w,h]
        for tag in self.frames.keys():
            self.update_frame_geometry(tag)
    
    def update_frame_geometry(self, tag):
        canvas = self.frames[tag][0]
        frame = self.frames[tag][1]
        if not canvas.winfo_manager():
            return
        canvas.update()
        frame.update()
        w, h = canvas.winfo_width(), canvas.winfo_height()
        frame.config(width=w, height=h)

        for child in frame.winfo_children():
            if not child.winfo_manager():
                continue
            cw, ch = self.get_se(child)
            w, h = max(w, cw), max(h, ch)

        # Update the frame size to encompass all child widgets
        frame.config(width=w, height=h)
        canvas.config(scrollregion=(0, 0, w+15, h+15))
    
    def update_frames(self):
        for tag in self.frames.keys():
            self.update_frame_geometry(tag)

    
    def get_se(self, widget: tk.Widget):
        widget.update()
        return widget.winfo_x() + widget.winfo_width(), widget.winfo_y()+widget.winfo_height()

    def show_frame_geometry(self, tag):
        canvas = self.frames[tag][0]
        frame = self.frames[tag][1]
        self.root.update()
        print(f"canvas: {canvas.winfo_width()}x{canvas.winfo_height()}")
        print(f"frame: {frame.winfo_width()}x{frame.winfo_height()}")
        print(self.frames)

    def set_frame(
            self,
            master_tag = None,
            tag = "frame_0",
            x = 0,
            y = 0,
            relx = None,
            rely = None,
            width = DEFAULT_WIDTH,
            height = DEFAULT_HEIGHT,
            relwidth = None,
            relheight = None,
            background = None,
            borderwidth = 0,
            relief = 'flat',
            scroll = '',
            **args
        ):
        # places a frame with scrollbar to the master.

        if master_tag is None:
            master = self.root
        else:
            master = self.frames[master_tag][1]
        
        hs_tag = f"{tag}_hscrollbar"
        vs_tag = f"{tag}_vscrollbar"
        if not tag in self.frames:
            canvas = tk.Canvas(master=master, borderwidth=borderwidth, relief=relief, background='grey')
            if not master_tag is None:
                master_widgets = self.frames[master_tag][2]
                master_widgets[tag] = canvas

            frame = tk.Frame(master=canvas, background=background, **args)
            self.frames[tag] = [canvas, frame, dict()]
            widgets = self.frames[tag][2]
            hs = tk.Scrollbar(
                canvas, orient=tk.HORIZONTAL, command=canvas.xview)
            widgets[hs_tag] = hs
            vs = tk.Scrollbar(
                canvas, orient=tk.VERTICAL, command=canvas.yview)
            widgets[vs_tag] = vs
            canvas.configure(
                xscrollcommand=hs.set,
                yscrollcommand=vs.set)
            
            def on_mouse_wheel(event):
                canvas.yview_scroll(-1 * int((event.delta/120)), "units")

            def bind_mouse_wheel(event):
                canvas.bind_all("<MouseWheel>", on_mouse_wheel)

            def unbind_mouse_wheel(event):
                canvas.unbind_all("<MouseWheel>")
    
            frame.bind("<Enter>", bind_mouse_wheel)
            frame.bind("<Leave>", unbind_mouse_wheel)
            

        canvas = self.frames[tag][0]
        frame = self.frames[tag][1]
        widgets = self.frames[tag][2]
        hs = widgets[hs_tag]
        vs = widgets[vs_tag]


        if not relwidth is None:
            width = -x
        if not relheight is None:
            height = -y

        canvas.place(
            x=x, y=y,
            relx=relx, rely=rely,
            width=width, height=height,
            relwidth=relwidth, relheight=relheight,
            anchor="nw")
        frame.place(x=0, y=0,)
        if 'h' in scroll:
            hs.pack(side=tk.BOTTOM, fill=tk.X)
        else:
            hs.forget()
        if 'v' in scroll:
            vs.pack(side=tk.RIGHT, fill=tk.Y)
        else:
            vs.forget()
        canvas.create_window(0, 0, window=frame, anchor="nw")
        return canvas, frame

    def set_button(
            self,
            master_tag = 'frame_0',
            tag = "button_0",
            text = "",
            font = None,
            command = None,
            x = None,
            y = None,
            relx = None,
            rely = None,
            width = None,
            height = None,
            relwidth = None,
            relheight = None,
            background = None,
            borderwidth = 1,
            relief = 'raised',
            anchor = 'nw',
            **args
           ) -> tk.Button:
        master = self.frames[master_tag][1]
        widgets = self.frames[master_tag][2]
        if (not tag in widgets.keys()) or not isinstance(widgets[tag], tk.Button):
            if tag in widgets.keys():
                widgets[tag].destroy()
                print(widgets[tag].__class__.__name__)
            button = tk.Button(
                master, text=text, command=command,
                font=font, background=background, 
                borderwidth=borderwidth, relief=relief,
                **args)
            widgets[tag] = button
        button = widgets[tag]
        button.configure(
            command=command, text=text, background=background,
            borderwidth=borderwidth, relief=relief, **args)
        button.place(
            x=x, y=y, relx=relx, rely=rely,
            width=width, height=height, relwidth=relwidth, relheight=relheight,
            anchor = anchor)
        return button


    def set_label(
            self,
            master_tag = 'frame_0',
            tag = "label_0",
            text = "",
            font = None,
            x = None,
            y = None,
            relx = None,
            rely = None,
            width = None,
            height = None,
            relwidth = None,
            relheight = None,
            background = None,
            borderwidth = 0,
            relief = None,
            anchor='nw',
            **args
           ) -> tk.Label:
        master = self.frames[master_tag][1]
        widgets = self.frames[master_tag][2]
        if (not tag in widgets.keys()) or not isinstance(widgets[tag], tk.Label):
            if tag in widgets.keys():
                widgets[tag].destroy()
                print(widgets[tag].__class__.__name__)
            label = tk.Label(
                master, text=text,
                font=font, background=background, 
                borderwidth=borderwidth, relief=relief,
                **args)
            widgets[tag] = label
        label = widgets[tag]
        label.configure(
            text=text, background=background,
            borderwidth=borderwidth, relief=relief, **args)
        label.place(
            x=x, y=y, relx=relx, rely=rely,
            width=width, height=height, relwidth=relwidth, relheight=relheight,
            anchor=anchor)
        return label
    
    def set_scrolled_text(
            self,
            master_tag = 'frame_0',
            tag = "text_0",
            text = "",
            font = None,
            x = None,
            y = None,
            relx = None,
            rely = None,
            width = None,
            height = None,
            relwidth = None,
            relheight = None,
            background = None,
            borderwidth = 1,
            relief = None,
            anchor = 'nw',
            wrap = tk.WORD,
            **args
           ) -> st.ScrolledText:
        master = self.frames[master_tag][1]
        widgets = self.frames[master_tag][2]
        if (not tag in widgets.keys()) or not isinstance(widgets[tag], st.ScrolledText):
            if tag in widgets.keys():
                print(widgets[tag].__class__.__name__)
                widgets[tag].destroy()
            stext = st.ScrolledText(
                master,
                font=font,
                background=background, 
                borderwidth=borderwidth,
                relief=relief,
                undo=True, maxundo=-1,
                wrap=wrap,
                **args)
            widgets[tag] = stext
        stext = widgets[tag]
        stext.delete('1.0', tk.END)
        stext.insert('1.0', text)
        stext.configure(
            background=background, borderwidth=borderwidth,
            relief=relief, **args)
        stext.place(
            x=x, y=y, relx=relx, rely=rely,
            width=width, height=height,
            relwidth=relwidth, relheight=relheight,
            anchor = anchor)
        return stext
    

    def set_menu(
            self,
            master = None,
            command_graph = [],
            font = None,
            background = None,
            borderwidth = 1,
            relief = None,
            **args
    ) -> tk.Menu:
        # creates a tkinter Menu based on the command_graph.
        #   A command_graph is a list of nodes, where a nodes is
        #   a list [label: str, command: Callable] or a list
        #   [label: str, commands: command_graph].
        def set_menu_content(cur_menu: tk.Menu, command_graph:list):
            for node in command_graph:
                if isinstance(node[1], list):
                    child_menu = tk.Menu(
                        master=cur_menu, font=font, background=background,
                        borderwidth=borderwidth, relief=relief, **args)
                    set_menu_content(child_menu, node[1])
                    cur_menu.add_cascade(label=node[0], menu=child_menu)
                else:
                    cur_menu.add_command(label=node[0], command=node[1])
        if master is None:
            master = self.root
        menu = tk.Menu(
            master=master, font=font, background=background,
            borderwidth=borderwidth, relief=relief, **args)
        set_menu_content(menu, command_graph)
        master.config(menu=menu, background=background,
            borderwidth=borderwidth, relief=relief, **args)
        return menu


    def set_menu_button(
            self,
            master_tag = 'frame_0',
            tag = "menu_button_0",
            text = "",
            font = None,
            command_graph = [],
            x = None,
            y = None,
            relx = None,
            rely = None,
            width = None,
            height = None,
            relwidth = None,
            relheight = None,
            menu_background = None,
            background = None,
            borderwidth = 1,
            relief = 'raised',
            anchor = 'nw',
            **args
           ) -> tk.Menubutton:
        master = self.frames[master_tag][1]
        widgets = self.frames[master_tag][2]
        if (not tag in widgets.keys()) or not isinstance(widgets[tag], tk.Menubutton):
            if tag in widgets.keys():
                widgets[tag].destroy()
                print(widgets[tag].__class__.__name__)
            mb = tk.Menubutton(
                master, text=text,
                font=font, background=background, 
                borderwidth=borderwidth, relief=relief,
                **args)
            widgets[tag] = mb
        mb = widgets[tag]
        menu = self.set_menu(master=mb, command_graph=command_graph,
                             background=menu_background)
        mb.configure(
            menu=menu, text=text, background=background,
            borderwidth=borderwidth, relief=relief, **args)
        mb.place(
            x=x, y=y, relx=relx, rely=rely,
            width=width, height=height,
            relwidth=relwidth, relheight=relheight,
            anchor = anchor)
        return mb

    def pop_mb_question(self, title: str = None, message:str = None):
        return messagebox.askquestion(title=title, message=message)
    
    def load_images(self, master_tag:str, images: list, width_ratio = 1):
        self.clear_frame_content(master_tag)
        master = self.frames[master_tag][1]
        widgets = self.frames[master_tag][2]
        canvas = self.frames[master_tag][0]
        canvas.update_idletasks()
        canvas_width = canvas.winfo_width()
        for i, img in enumerate(images):
            image = ImageTk.PhotoImage(self.resized_image(img, canvas_width*width_ratio))
            label_tag = f"image_{i}"
            if not label_tag in widgets.keys():
                widgets[label_tag] = tk.Label(master, image=image)
            image_label = widgets[label_tag]
            image_label.config(image=image)
            image_label.image = image
            image_label.pack(fill='x', expand=True)
        self.update_frame_geometry(master_tag)
    
    def resized_image(self, img: Image.Image, new_width:float):
        im_w, im_h = img.size
        ratio = new_width/im_w
        return img.resize((int(im_w*ratio), int(im_h*ratio)))


    def read_text(self, text:tk.Widget):
        return text.get("1.0", tk.END)[:-1]
    
    def get_widget(self, frame_tag:str, text_tag: str):
        return self.frames[frame_tag][2][text_tag]


    
# Example usage:
if __name__ == "__main__":
    ui = GraphicalUserInterface()

    
    '''
    def set_frame():
        ui.set_frame(master_tag="frame_0", tag='frame_1',relx=0.1, relwidth=0.5, relheight=1)
    set_frame()
    button_1 = ui.set_button(master_tag="frame_1", tag="button_1", text="geometry", command=lambda: ui.show_frame_geometry('frame_0'),  x=10, y=10,)
    button_2 = ui.set_button(master_tag="frame_1", tag="button_2", text="Move label",
                             command=lambda: ui.set_label(
                                 master_tag="frame_1", tag="label_0", text="This is a label", x=200, y=1000,
                             ), 
                             x=10, y=40,)
    ui.set_label(master_tag="frame_1", tag="label_0", text="This is a label", x=200, y=10,),
    button_3 = ui.set_button(master_tag="frame_1", tag="button_3", text="clear frame content",
                             command=lambda: ui.clear_frame_content("frame_1"),
                             x=10, y=70,)
    button_4 = ui.set_button(master_tag="frame_1", tag="button_4", text="clear frame",
                             command=lambda: ui.clear_frame("frame_1"),
                             x=10, y=100,)
    
    button_5 = ui.set_button(master_tag="frame_0", tag="button_5", text="open frame",
                             command=lambda: set_frame(),
                             x=600, y=100,)
    
    text_1 = ui.set_scrolled_text(master_tag="frame_1", tag="text_0", text="This is a text", x=10, y=200, width=300, height=100),
    '''



    ui.set_ckeck_button(tag='cb',text="This is a ckeck button",
                        command=lambda:print(ui.get_widget('frame_0', 'cb_iv').get()),
                        x=100, y=100, width=400, height=80)
    ui.update_frames()
    ui.proc()



