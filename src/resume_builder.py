"""
File: resume_builder.py

Description:
    This module contains the ResumeBuilder class, which draws and update the UI
with relevant functions for ResumeContent and GraphicalUserInterface classes.
"""


from .ui import GraphicalUserInterface
from .resume_content import ResumeContent
import asyncio
import threading
import time
import random
import tkinter as tk



class ResumeBuilder:

    def __init__(self, ui: GraphicalUserInterface) -> None:
        self.ui = ui
        self.content = None
        self.current_state = 'start'

        self.open_main_page()


    def proc(self):
        self.ui.proc()
        self.current_state = 'exit'


    @property
    def main_state(self):
        return "main"
    
    @property
    def workspace_state(self):
        return "workspace"

    @property
    def main_page_tag(self):
        return "main_page"
    
    @property
    def workspace_tag_1(self):
        return "workspace_1"

    @property
    def workspace_tag_2(self):
        return "workspace_2"
    
    @property
    def workspace_tag_3(self):
        return "workspace_3"


    def open_main_page(self):
        self.current_state = self.main_state
        self.draw_main_page()
    
    def open_workspace(self):
        self.current_state = self.workspace_state
        id = self.ui.read_text(
            self.ui.get_widget(
                self.main_page_tag, 'main_resume_id'))
        self.content = ResumeContent(id)
        self.draw_workspace()
        self.start_content_display()
    
    def draw_main_page(self):
        def get_random(items):
            cur = col_rd[0]
            col_rd[0] = random.randint(0, len(col_rd[1])-1)
            while col_rd[0] == cur:
                col_rd[0] = random.randint(0, len(col_rd[1])-1)
            return col_rd[1][col_rd[0]]

        self.ui.clear_frame_content()
        master_tag = self.main_page_tag
        title = self.ui.title
        font_header = (self.ui.FONT_FAMILY_1, 32, "bold")
        font_normal = (self.ui.FONT_FAMILY_2, 20)
        col_rd = [0,
                  [self.ui.COL_GREEN_3, self.ui.COL_PURPLE_3,
                   self.ui.COL_RED_3, self.ui.COL_BLUE_3,
                   self.ui.COL_ORANGE_3, self.ui.COL_PINK_3]]
        col_bg_main = self.ui.COL_SKY_0
        col_title = col_rd[1][col_rd[0]]
        col_button = self.ui.COL_GRAY_1
        self.ui.set_frame(
            master_tag='frame_0', tag=master_tag,
            relx=0, rely=0, relwidth=1, relheight=1,
            background=col_bg_main)
        main_title = self.ui.set_label(
            master_tag=master_tag, tag="main_title",
            text=title, font=font_header,
            relx=0, y=100, relwidth=1, height=60,
            background=col_title, anchor="nw",
            fg=col_bg_main)
        main_title.bind("<Enter>", lambda event:
                        main_title.configure(background=get_random(col_rd)))
        self.ui.set_label(
            master_tag=master_tag, tag="main_label_0",
            text="Resume ID:", font=font_normal,
            relx=0.3, y=280,
            relwidth=0.2, height=30,
            background=col_bg_main,
            anchor='center')
        self.ui.set_scrolled_text(
            master_tag=master_tag, tag="main_resume_id",
            text="resume_0", font=font_normal,
            relx=0.5, y=320,
            relwidth=0.4, height=38,
            background=self.ui.COL_GRAY_0,
            anchor='center')
        self.ui.set_button(
            master_tag=master_tag, tag="main_submit",
            text="Load", font=font_normal,
            command= self.open_workspace,
            relx=0.37, y=390, relwidth=0.20, height=40,
            background=col_button,
            activebackground=self.ui.COL_BLUE_2,
            anchor='center')
        self.ui.set_button(
            master_tag=master_tag, tag="main_exit",
            text="Quit", font=font_normal,
            command= self.ui.exit,
            relx=0.63, y=390, relwidth=0.20, height=40,
            background=col_button,
            activebackground=self.ui.COL_RED_3,
            anchor='center')
        self.ui.update_frames()
        
    
    def draw_workspace(self):
        self.ui.clear_frame_content()
        self.draw_workplace_menu()
        self.draw_workplace_displayer()
        self.draw_workplace_editor()
        self.ui.update_frames()

    def draw_workplace_menu(self):
        f1_master_tag = self.workspace_tag_1
        col_bg = self.ui.COL_GREEN_1
        col_text = self.ui.COL_GRAY_0
        col_button = self.ui.COL_GRAY_1
        font_family = self.ui.FONT_FAMILY_3
        self.ui.set_frame(
            master_tag='frame_0', tag=f1_master_tag,
            relx=0, rely=0,
            relwidth=0.35, relheight=0.4,
            background=col_bg)
        self.ui.clear_frame_content(f1_master_tag)
        
        
        self.ui.set_button(
            master_tag=f1_master_tag, tag="workspace_back", text="Back",
            font=(font_family, 10),
            command= self.open_main_page,
            relx=0.05, y=20, relwidth=0.4, height=25,
            background=col_button)
        
        self.ui.set_button(
            master_tag=f1_master_tag, tag="workspace_save_to", text="Save Changes",
            font=(font_family, 10),
            command= self.save_content,
            relx=0.4, y=80, relwidth=0.45, height=25,
            background=col_button)
        self.ui.set_scrolled_text(
            master_tag=f1_master_tag, tag="resume_content_path", text=f"resume/{self.content.id}.json",
            font=(font_family, 10),
            relx=0.05, y=60, relwidth=0.85, height=20,
            background=col_text)
        
        self.ui.set_button(
            master_tag=f1_master_tag, tag="workspace_save_pdf", text="Import pdf",
            font=(font_family, 10),
            command= self.import_pdf,
            relx=0.4, y=140, relwidth=0.45, height=25,
            background=col_button)
        self.ui.set_scrolled_text(
            master_tag=f1_master_tag, tag="resume_pdf_path", text=f"resume/{self.content.id}.pdf",
            font=(font_family, 10),
            relx=0.05, y=120, relwidth=0.85, height=20,
            background=col_text)
        
    def draw_workplace_displayer(self):
        f2_master_tag = self.workspace_tag_2
        col_bg = self.ui.COL_SKY_2
        self.ui.set_frame(
            master_tag='frame_0', tag=f2_master_tag,
            relx=0.35, rely=0,
            relwidth=0.65, relheight=0.4,
            background=col_bg,
            scroll='hv')
        self.ui.clear_frame_content(f2_master_tag)
        
    
    def draw_workplace_editor(self):
        f3_master_tag = self.workspace_tag_3
        col_bg = self.ui.COL_PALE_GREEN
        font_family = self.ui.FONT_FAMILY_3
        self.ui.set_frame(
            master_tag='frame_0', tag=f3_master_tag,
            relx=0, rely=0.4,
            relwidth=1, relheight=0.6,
            background=col_bg,
            scroll='hv')
        self.ui.clear_frame_content(f3_master_tag)
    
        self.ui.set_label(
            master_tag=f3_master_tag, tag="f3_main",
            text="Editor Workspace", font=(font_family, 20),
            relx=-0.05, y=-5, relwidth=1.1,
            background=self.ui.COL_SKY_1,
            borderwidth=0,relief='solid'
        )
        self.content.draw_workspace(
            root=self, ui=self.ui,
            master_tag=f3_master_tag, tag_pref=f"rc",
            coordinate=[50, 60],
            header_font=(font_family, 12), font=(font_family, 10),
            xpad=20, ypad=20,
            header_width=200, header_height=30,
            width=50, height=20,
            )
        
        
    def start_content_display(self):
        t = threading.Thread(target=self.content_display)
        t.start()
        self.ui.push_thread(t)

        
    def content_display(self, time_sep=5):
        while self.current_state == self.workspace_state:
            images = self.content.as_images()
            if self.ui.get_state == 'exit':
                break
            self.ui.load_images(self.workspace_tag_2, images, 1.1)
            time.sleep(time_sep)
        

    def import_pdf(self):
        path = self.ui.read_text(self.ui.get_widget(self.workspace_tag_1, "resume_pdf_path"))
        self.content.to_pdf(path)
        print(f"Import as {path}.")

    def save_content(self):
        path = self.ui.read_text(self.ui.get_widget(self.workspace_tag_1, "resume_content_path"))
        self.content.save(path)
        print(f"Saved Resume content to {path}.")



