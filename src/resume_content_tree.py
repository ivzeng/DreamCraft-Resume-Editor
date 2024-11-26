"""
File: component_classes.py

Description:
    This module contains a series of Python classes that represent different components
in an HTML page, a Markdown page, or a similar text structure. Each class provides
methods to modify or decotrate the corresponding text structure, create widgets and
handle events for UI, and covert the content to markdown or HTML format.

Classes:
    ContentGraphNode
        Element
            TextElement
            URLElement
            HLine

        Itemization
            Sequence
            TextLine
                Header
            InlineList
            UnorderList
            Tabular

        Decorator
            StyledFont
            BoxMargin

"""


import sys
import tkinter as tk
from typing import Callable
from functools import partial
from .ui import GraphicalUserInterface


class ContentTreeNode:
    '''
    Base class for tree nodes.
    '''
    DECORATORS = ['StyledFont', 'BoxMargin']

    def __init__(self, content: dict = None, parent = None) -> None:
        self.parent:ContentTreeNode = parent
        self.status = content.get("status", 1)
        self.info = content.get("info", self.class_name)
        self.temp = dict()
        self.decorator_type = []

    def __str__(self) -> str:
        return f"ContentGraphNode()"
    
    @property
    def class_name(self):
        return self.__class__.__name__

    @property
    def as_dict(self):
        return {
            "type": self.class_name,
            "status": 1,
            "info": self.info
        }

    @property
    def as_html(self) -> str:
        pass

    @property
    def as_markdown(self) -> str:
        pass
            
    def getattr(self, name:str):
        return getattr(self, name)

    def setattr(self, name:str, value:any):
        return setattr(self, name, value)

    def draw_editor(
            self,
            root,
            ui: GraphicalUserInterface,
            master_tag:str,
            tag_pref: str = "rc",
            coordinate: list = [0, 0],
            header_font: tuple = None,
            font:tuple = None,
            xpad = 20,
            ypad = 20, 
            header_width = 200,
            header_height = 30, 
            width = 50,
            height = 20,
            **args):
        pass

    def refresh_editor(
            self,
            root,
            ui: GraphicalUserInterface,
            master_tag
    ):
        ui.clear_frame_content(master_tag)
        root.draw_workplace_editor()
        ui.update_frame_geometry(master_tag)
    

    def draw_header(
            self,
            ui: GraphicalUserInterface,
            master_tag: str,
            header_tag: str,
            font: tuple = None,
            coordinate: list = [0, 0],
            width=200,
            height=30,
            **args
        ):
        # draws the header widgets in ui.
        st_info = self.draw_text(
            ui=ui, master_tag=master_tag, tag=header_tag,
            text=self.info, font=font,
            coordinate=coordinate,
            width=width, height=height, **args)
        
        st_info_class = self.draw_label(
            ui=ui, master_tag=master_tag, tag=f"{header_tag}_class_name",
            text=self.class_name, font=font,
            coordinate=[coordinate[0]+width+5, coordinate[1]],
            width=width/1.5, height=height/1.8, **args)
        
        self.bind_modified_text(ui=ui, widget=st_info, attr_name='info')
        
        return st_info, st_info_class

    def draw_decorators_config(
            self,
            root,
            ui: GraphicalUserInterface,
            master_tag: str,
            dc_tag: str,
            font: tuple = None,
            coordinate: list = [0, 0],
            width=100,
            height=15,
            **args
    ):
        # draws relevant widgets for decortor attr editing.
        #   Only used by non decorator classes.
        decorated = self.get_decorated_structure()
        decorated_name = [d.class_name for d in decorated]

        for dt in self.decorator_type:
            tag = f'{dc_tag}_{dt}'
            if dt in decorated_name:
                idx = decorated_name.index(dt)
                decorated[idx].draw_config(
                    root=root, ui=ui,
                    master_tag=master_tag, tag=tag,
                    font=font, coordinate=coordinate,
                    width=width*2, height=height,
                    **args
                )
            else:
                self.draw_update_master_button(
                    root=root, ui=ui, master_tag=master_tag, tag=f"{tag}_add",
                    command=partial(lambda dt: self.decorated(get_content_tree({"type": dt})), dt),
                    text=f"Add {dt}", font=font,
                    coordinate=coordinate,
                    width=width*2, height=height,
                    **args
                )
                coordinate[1] += height+5
        return decorated[-1]
    
    def draw_attr_editor(
            self,
            ui: GraphicalUserInterface,
            master_tag: str,
            tag: str,
            attrs = [],
            font: tuple = None,
            coordinate: list = [0, 0],
            line_width = 2,
            label_width = 100,
            label_height = 30,
            text_width = 200,
            text_height = 60,
            button_width = 15,
            button_height = 15,
            button_pady=2.5,
            **args):
        # draws the widgets for editing the 
        init_x = coordinate[0]
        step_count = 0
        step_height = max(label_height, text_height, button_height)
        for attr_name in attrs:
            attr_val = self.getattr(attr_name)
            attr_tag = f"{tag}_{attr_name}"
            if isinstance(attr_val, str):
                self.draw_str_editor(
                    ui=ui, master_tag=master_tag, tag=attr_tag,
                    attr_name=attr_name, font=font,
                    coordinate=coordinate,
                    label_width=label_width, label_height=label_height,
                    text_width=text_width, text_height=text_height,
                    **args
                )
                step_count += 2
            else:
                self.draw_binary_button(
                    ui=ui, master_tag=master_tag, attr_tag=attr_tag,
                    attr_name=attr_name, text = attr_name, coordinate=coordinate,
                    width=button_width, height=button_height, pady=button_pady,
                    **args
                )
                step_count += 1
            coordinate[0] += 5
            if step_count >= line_width:
                step_count = 0
                coordinate[0] = init_x
                coordinate[1] += step_height+5
        
        coordinate[0] = init_x
        if step_count != 0:
            coordinate[1] += step_height+5

    def draw_str_editor(
            self,
            ui: GraphicalUserInterface,
            master_tag: str,
            tag: str,
            attr_name: str,
            update_fn: Callable=None,
            label_text: str = None,
            font: tuple = None,
            coordinate: list = [0, 0],
            label_width=100,
            label_height=30,
            text_width=200,
            text_height=60,
            **args
    ):
        if label_text is None:
            label_text = f"{attr_name}:"
        st_label = self.draw_label(
            ui=ui, master_tag=master_tag, tag=f'{tag}_label',
            text=label_text, font=font,
            coordinate=coordinate,
            width=label_width, height=label_height,
            **args)
        coordinate[0] += label_width+5

        st = self.draw_text(
            ui=ui, master_tag=master_tag, tag=tag,
            text=self.getattr(attr_name), font=font,
            coordinate=coordinate,
            width=text_width, height=text_height,
            **args
        )
        coordinate[0] += text_width

        if update_fn is None:
            def update(event):
                self.setattr(attr_name, ui.read_text(st))
            update_fn = update
        self.bind_modified_text(ui, st, attr_name, update_fn)
        return st_label, st
    
    def draw_binary_button(
            self,
            ui:GraphicalUserInterface,
            master_tag: str,
            attr_tag: str,
            attr_name: str,
            trigger_fn: Callable = None,
            target = None,
            text: str = '',
            font: tuple = None,
            colors=['white', 'green'],
            coordinate=[0,0],
            width=15,
            height=15,
            pady=2.5,
            **args
        ):
        args.pop('background', None)
        cb_tag = f"{attr_tag}_cb"
        if target is None:
            target = self
        if trigger_fn is None:
            def set_attr():
                new_attr = 1-target.getattr(attr_name)
                target.setattr(attr_name, new_attr)
                cb.configure(background=colors[new_attr])
            trigger_fn = set_attr
        cb = self.draw_button(
            ui=ui, master_tag=master_tag, tag=cb_tag,
            text=text, font=font, command=trigger_fn,
            coordinate=[coordinate[0], coordinate[1]+pady], width=width, height=height,
            background=colors[target.getattr(attr_name)],
            borderwidth=2, relief='sunken',
            **args
        )
        coordinate[0] += width
        return cb
    
    def draw_update_master_button(
            self,
            root,
            ui: GraphicalUserInterface,
            master_tag:str,
            tag:str,
            command: Callable,
            text:str = '',
            font:tuple = None,
            coordinate: list = [0,0],
            width = 50,
            height = 20,
            **args
    ):
        
        def update_frame():
            command()
            self.refresh_editor(root, ui, master_tag)
        return self.draw_button(
            ui=ui,
            master_tag=master_tag, tag=tag,
            command=update_frame,
            text=text, font=font,
            coordinate=coordinate,
            width=width, height=height,
            **args
        )
        
    def draw_expand_button(
            self,
            root,
            ui: GraphicalUserInterface,
            master_tag:str,
            tag: str,
            text:str, font:tuple,
            coordinate: list,
            width = 50, height = 20,
            **args
    ):  
        def set_expand():
            self.temp['expand']=True

        return self.draw_update_master_button(
            root=root, ui=ui,
            master_tag=master_tag, tag=f"{tag}_expand",
            command=set_expand,
            text=text, font=font,
            coordinate=coordinate,
            width=width, height=height,
            **args
        )
    
    def draw_collapse_button(
            self,
            root,
            ui: GraphicalUserInterface,
            master_tag:str,
            tag: str,
            text:str,
            font:tuple,
            coordinate: list,
            width = 50, height = 20,
            **args
    ):
        def set_expand():
            self.temp['expand']=False

        return self.draw_update_master_button(
            root=root, ui=ui,
            master_tag=master_tag, tag=f"{tag}_collapse",
            command=set_expand,
            text=text, font=font,
            coordinate=coordinate,
            width=width, height=height,
            **args
        )
    
    
    def bind_modified_text(
            self,
            ui: GraphicalUserInterface,
            widget: tk.Text,
            attr_name: str,
            update_fn = None,
            ):
        # binds the event handler function update_fn that will be called
        #   on a modificaiton event on widget.

        if update_fn is None:
            update_fn = lambda event: self.setattr(attr_name, ui.read_text(widget))
        def update(event):
            widget.edit_modified(False)
            update_fn(event)

        widget.bind("<<Modified>>", update)
        widget.edit_modified(False)

    def draw_label(
            self,
            ui: GraphicalUserInterface,
            master_tag:str,
            tag: str,
            text:str = '',
            font: tuple = None,
            coordinate: list = [0, 0],
            width = 50,
            height = 20,
            **args
    ):
        return ui.set_label(
            master_tag=master_tag, tag=tag,
            text=text, font=font,
            x=coordinate[0], y=coordinate[1],
            width=width, height=height,
            **args)
        
    def draw_text(
            self,
            ui: GraphicalUserInterface,
            master_tag:str,
            tag: str,
            text: str = '',
            font:tuple = None,
            coordinate: list = [0,0],
            width = 50,
            height = 20,
            **args
    ):
        return ui.set_scrolled_text(
            master_tag=master_tag, tag=tag,
            text=text, font=font,
            x=coordinate[0], y=coordinate[1],
            width=width, height=height,
            **args)
    
    def draw_button(
            self,
            ui: GraphicalUserInterface,
            master_tag:str, tag: str,
            command: Callable,
            text: str = '',
            font:tuple = None,
            coordinate: list = [0, 0],
            width = 50,
            height = 20,
            **args
    ):
        return ui.set_button(
            master_tag=master_tag, tag=tag,
            text=text, font=font,
            command=command,
            x=coordinate[0], y=coordinate[1],
            width=width, height=height,
            **args
        )


    def draw_menu_button(
            self,
            ui: GraphicalUserInterface,
            master_tag:str,
            tag: str,
            menu_graph: list,
            text: str = '',
            font:tuple = None,
            coordinate: list = [0, 0],
            width = 50,
            height = 20,
            **args
    ):
        return ui.set_menu_button(
            master_tag=master_tag, tag=tag, text=text, font=font,
            command_graph=menu_graph, x=coordinate[0], y=coordinate[1],
            width=width, height=height,
            **args
        )


    def decorated(self, decorator):
        decorated = self.get_decorated_structure()
        decorated_name = [d.class_name for d in decorated]
        if decorator.class_name not in decorated_name:
            decorator.setattr('parent', self.parent)
            decorator.set_component(self)
            if not decorator.parent is None:
                decorator.parent.replace(self, decorator)
            return decorator

        idx = decorated_name.index(decorator.class_name)
        replacing_decorator = decorated[idx]
        decorated[idx] = decorator
        decorator.set_component(replacing_decorator.component)
        replacing_decorator.parent_replace(decorator)
        return decorated[-1]
    
    def get_decorated_structure(self):
        cur = self.get_bottom_component()
        structure = [cur]
        cur = cur.parent
        while not cur is None and cur.class_name in self.DECORATORS:
            structure.append(cur)
            cur = cur.parent
        return structure

    def get_bottom_component(self):
        cur = self
        while cur.class_name in self.DECORATORS:
            cur = cur.component
        return cur

    
    def replace(self, component1, component2):
        pass

    def pop(self):
        pass

    def pre_order(self):
        pass



class Element(ContentTreeNode):
    '''
    Base class for elements (tree leaves).
    '''

    def __init__(self, content: dict = None, parent = None) -> None:
        super().__init__(content, parent)

    def __str__(self) -> str:
        return f"Element(status={self.status})"
    
    def pre_order(self):
        return [self]


    
class HLine(Element):
    '''
    Represents a horizontal Line.

    content's key:
        None
    '''
    def __init__(self, content: dict = dict(), parent = None) -> None:
        super().__init__(content, parent)

    def  __str__(self):
        return f'HLine(status={self.status})'
    
    @property
    def as_dict(self):
        return super().as_dict
    
    @property
    def as_html(self):
        if self.status == 0:
            return ""
        return f'<hr style="margin-left:-20px;margin-right:40px;">'
    
    @property
    def as_markdown(self):
        if self.status == 0:
            return ""
        return '---'
    
    @property
    def display_color(self):
        return [GraphicalUserInterface.COL_GRAY_0,
                GraphicalUserInterface.COL_YELLOW_0]

    def draw_editor(
            self,
            root,
            ui: GraphicalUserInterface,
            master_tag:str,
            tag_pref: str = "rc",
            coordinate: list = [0, 0],
            header_font: tuple = None,
            font:tuple = None,
            xpad = 20,
            ypad = 20, 
            header_width = 200,
            header_height = 30, 
            width = 50,
            height = 20,
            **args):
        
        head_tag = f"{tag_pref}_head"
        dc_tag = f"{tag_pref}_dc"
        col_header = self.display_color[0]
        col_decorators = self.display_color[1]

        self.draw_label(
            ui=ui, master_tag=master_tag, tag=head_tag,
            text=self.class_name, font=header_font,
            coordinate=[coordinate[0], coordinate[1]],
            width=header_width, height=header_height,
            background=col_header,
            **args)
        coordinate[1] += header_height+5
        coordinate[0] += xpad/2

        self.draw_decorators_config(
            root=root, ui=ui, master_tag=master_tag, dc_tag=dc_tag, font=font,
            coordinate=coordinate,width=width, height=height,
            background=col_decorators,
            **args
        )

        coordinate[0] -= xpad/2
        coordinate[1] += ypad
    


class TextElement(Element):
    '''
    Represents a text.

    content's key:
        "value"
    '''
    def __init__(self, content: dict = dict(), parent = None) -> None:
        super().__init__(content, parent)
        self.value: str = content.get("value", "")
        self.decorator_type = ["StyledFont"]

    def  __str__(self):
        return f'TextElement("{self.value}", status={self.status})'
    
    @property
    def as_dict(self):
        return super().as_dict | {
            "value": self.value,
        }
    
    @property
    def as_html(self):
        if self.status == 0:
            return ""
        return self.value
    
    @property
    def as_markdown(self):
        if self.status == 0:
            return ""
        return self.as_html
    
    def to_url(self, url):
        # create a url element
        if self.status == 0:
            return ""
        return URLElement({"value": self.value, "url": url}, self.parent)
    
    @property
    def display_color(self):
        return [GraphicalUserInterface.COL_GREEN_1,
                GraphicalUserInterface.COL_GREEN_0,
                GraphicalUserInterface.COL_PALE_GREEN]
    
    def draw_editor(
            self,
            root,
            ui: GraphicalUserInterface,
            master_tag:str,
            tag_pref: str = "rc",
            coordinate: list = [0, 0],
            header_font: tuple = None,
            font:tuple = None,
            xpad = 20,
            ypad = 20, 
            header_width = 200,
            header_height = 30, 
            width = 50,
            height = 20,
            **args):
        
        header_tag = f"{tag_pref}_head"
        dc_tag = f"{tag_pref}_dc"
        col_header = self.display_color[0]
        col_decorators = self.display_color[1]
        col_texts = self.display_color[2]

        st_info, st_info_class = self.draw_header(
            ui=ui,
            master_tag=master_tag, header_tag=header_tag,
            font=header_font, coordinate=coordinate,
            width=header_width, height=header_height,
            background=col_header,
            **args
        )
        coordinate[1] += header_height+5

        self.draw_decorators_config(
            root=root, ui=ui, master_tag=master_tag, dc_tag=dc_tag,
            font=font, coordinate=coordinate, width=width, height=height,
            background=col_decorators,
            **args
        )

        coordinate[0] += xpad/2
        self.draw_attr_editor(
            ui=ui, master_tag=master_tag, tag=tag_pref,
            attrs=['value'], font=font,
            coordinate=coordinate,
            label_width=width, label_height=height,
            text_width=width*10, text_height=height*3,
            background=col_texts,
            **args
        )
        coordinate[0] -= xpad/2
        coordinate[1] += ypad

    

class URLElement(Element):
    '''
    Represents a url and a text.

    content's keys:
        "value"
        "url"
    '''
    def __init__(self, content: dict = dict(), parent = None) -> None:
        super().__init__(content, parent)
        self.value: str = content.get("value", "")
        self.url: str = content.get("url", "")
        self.decorator_type = ["StyledFont"]

    def __str__(self):
        return f'URLItem("{self.value}", "{self.url}", status={self.status})'
    
    @property
    def as_dict(self):
        return super().as_dict | {
            "value": self.value,
            "url": self.url,
        }
    
    @property
    def as_html(self):
        if self.status == 0:
            return ""
        return f'<a href="{self.url}">{self.value}</a>'

    @property
    def as_markdown(self):
        if self.status == 0:
            return ""
        return self.as_html
    
    @property
    def display_color(self):
        return [GraphicalUserInterface.COL_YELLOW_0,
                GraphicalUserInterface.COL_GREEN_0,
                GraphicalUserInterface.COL_PALE_GREEN]

    def draw_editor(
            self,
            root,
            ui: GraphicalUserInterface,
            master_tag:str,
            tag_pref: str = "rc",
            coordinate: list = [0, 0],
            header_font: tuple = None,
            font:tuple = None,
            xpad = 20,
            ypad = 20, 
            header_width = 200,
            header_height = 30, 
            width = 50,
            height = 20,
            **args):
        
        header_tag = f"{tag_pref}_head"
        dc_tag = f"{tag_pref}_dc"
        col_header = self.display_color[0]
        col_decorators = self.display_color[1]
        col_texts = self.display_color[2]

        self.draw_header(
            ui=ui,
            master_tag=master_tag, header_tag=header_tag,
            font=header_font, coordinate=coordinate,
            width=header_width, height=header_height,
            background=col_header,
            **args
        )
        coordinate[1] += header_height+5

        self.draw_decorators_config(
            root=root, ui=ui, master_tag=master_tag, dc_tag=dc_tag, font=font,
            coordinate=coordinate, width=width, height=height,
            background=col_decorators,
            **args
        )

        coordinate[0] += xpad/2
        self.draw_attr_editor(
            ui=ui, master_tag=master_tag, tag=tag_pref,
            attrs=['value', 'url'], font=font,
            coordinate=coordinate,
            label_width=width, label_height=height,
            text_width=width*10, text_height=height*3,
            background=col_texts,
            **args
        )
        coordinate[0] -= xpad/2
        coordinate[1] += ypad
    

class Itemization(ContentTreeNode):
    '''
    Base class, represents a list of nodes.

    content's key:
        "components"
    '''
    def __init__(self, content: dict = dict(), parent = None) -> None:
        super().__init__(content, parent)
        self.components: list[ContentTreeNode] = [
            get_content_tree(CGLeaf) for CGLeaf in content.get("components", list())
            ]
        for component in self.components:
            component.setattr('parent',self)
        self.decorator_type = ["StyledFont", "BoxMargin"]
        self.attrs = []
        self.insert_type = []
        
    def __str__(self):
        return f"Itemization([{self.components_str}, status={self.status}])"
    
    @property
    def as_dict(self):
        return super().as_dict | {
            "components": [component.as_dict for component in self.components],
        }
    
    @property
    def as_html(self):
        if self.status == 0:
            return ""
        return f"{''.join(component.as_html for component in self.components)}"

    @property
    def as_markdown(self):
        if self.status == 0:
            return ""
        return f"{''.join(component.as_markdown for component in self.components)}"
    
    @property
    def components_str(self):
        return ', '.join(component.__str__() for component in self.components)
    
    @property
    def display_color(self):
        return [GraphicalUserInterface.COL_BLUE_1,
                GraphicalUserInterface.COL_PURPLE_0,
                GraphicalUserInterface.COL_BLUE_0,
                GraphicalUserInterface.COL_SKY_1,
                GraphicalUserInterface.COL_BLUE_0]
                
    
    def draw_editor(
            self,
            root,
            ui: GraphicalUserInterface,
            master_tag:str,
            tag_pref: str = "rc",
            coordinate: list = [0, 0],
            header_font: tuple = None,
            font:tuple = None,
            xpad = 20,
            ypad = 20, 
            header_width = 200,
            header_height = 30, 
            width = 50,
            height = 20,
            **args):
        def update_info(event):
            self.setattr('info', ui.read_text(st_info))
            if self.temp.get('expand', False):
                self.draw_collapse_button(
                    root=root, ui=ui,
                    master_tag=master_tag, tag=header_tag,
                    text=f"Collapse {self.info}", font=font,
                    coordinate=end_coordinate,
                    width=header_width*2, height=header_height/1.5, **args)
        def remove_item(idx:int, name:str):
            answer = ui.pop_mb_question(
                title=f"Remove {name}",
                message=f'This action will completely remove {name} and its contents. Are you sure?')
            if answer == 'yes':
                self.pop(idx)

        def insert_item_refresh(structure_type):
            self.insert(get_content_tree({'type': structure_type}))
            self.refresh_editor(root=root, ui=ui, master_tag=master_tag)
            
        
        header_tag = f"{tag_pref}_head"
        init_x = coordinate[0]
        init_y = coordinate[1]
        bwidth = header_height/2
        col_header = self.display_color[0]
        col_decorators = self.display_color[1]
        col_texts = self.display_color[2]
        col_buttons_1 = self.display_color[3]
        col_buttons_2 = self.display_color[4]
    

        st_info, st_info_class = self.draw_header(
            ui=ui, master_tag=master_tag, header_tag=header_tag,
            font=header_font, coordinate=coordinate,
            width=header_width, height=header_height,
            background=col_header,
            **args
        )

        self.bind_modified_text(ui=ui, widget=st_info, attr_name='info', update_fn=update_info)
        coordinate[1] += header_height/0.9+5

        
        if not self.temp.get('expand', False):
            self.draw_expand_button(
                root=root, ui=ui, master_tag=master_tag, tag=header_tag,
                text='Expand', font=font,
                coordinate=[init_x+header_width+5+bwidth*1.2, init_y+header_height/1.8],
                width=header_width/1.5-bwidth*1.2, height=header_height/1.8,
                background=col_buttons_1,
                **args
            )
            return
        coordinate[0] += xpad

        dc_tag = f"{tag_pref}_dc"
        self.draw_decorators_config(
            root=root, ui=ui, master_tag=master_tag, dc_tag=dc_tag, font=font,
            coordinate=coordinate, width=width, height=height,
            background=col_decorators,
            **args
        )
        coordinate[0] += xpad

        self.draw_attr_editor(
            ui=ui, master_tag=master_tag, tag=tag_pref,
            attrs=self.attrs, font= font, coordinate=coordinate,
            line_width=2, label_width=width*2, label_height=height,
            text_width=width*2, text_height=height,
            button_width=width*2, button_height=height, button_pady=0,
            background=col_texts,
            **args
        )

        coordinate[0] += xpad


        for i, component in enumerate(self.components):
            component_tag = f"{tag_pref}_{i}"
            self.draw_binary_button(
                ui=ui, master_tag=master_tag, attr_tag=f"{component_tag}_cb",
                attr_name='status', target=component.get_bottom_component(),
                coordinate=[coordinate[0]-bwidth*2-5, coordinate[1]],
                width=bwidth, height=bwidth, pady=0,
                **args
            )
            self.draw_update_master_button(
                root=root, ui=ui, master_tag=master_tag, tag=f"{component_tag}_remove",
                command=partial(remove_item, i, component.class_name),
                text='X', font=font,
                coordinate=[coordinate[0]-bwidth*2-5, coordinate[1]+bwidth],
                width=bwidth, height=bwidth, background=ui.COL_RED_3,
                **args
            )

            if i >= 1:
                self.draw_update_master_button(
                    root=root, ui=ui, master_tag=master_tag, tag=f"{component_tag}_shift_up",
                    command=partial(self.swap, i, i-1),
                    text='▲', font=font,
                    coordinate=[coordinate[0]-bwidth-5, coordinate[1]],
                    width=bwidth, height=bwidth,
                    background=col_buttons_2,
                    **args
                )

            if i < len(self.components)-1:
                self.draw_update_master_button(
                    root=root, ui=ui, master_tag=master_tag, tag=f"{component_tag}_shift_down",
                    command=partial(self.swap, i, i+1),
                    text='▼', font=font,
                    coordinate=[coordinate[0]-bwidth-5, coordinate[1]+bwidth],
                    width=bwidth, height=bwidth,
                    background=col_buttons_1,
                    **args
                )

            self.draw_update_master_button(
                root=root, ui=ui, master_tag=master_tag, tag=f"{component_tag}_clone",
                command=partial(self.insert_clone, i),
                text='⇉', font=font,
                coordinate=[coordinate[0]+header_width+5, coordinate[1]+header_height/1.8],
                width=bwidth*1.2, height=bwidth*1.2,
                background=col_buttons_1,
                **args
            )

            component.draw_editor(
                root=root, ui=ui,
                master_tag=master_tag, tag_pref=component_tag,
                coordinate=coordinate,
                header_font=header_font, font=font,
                xpad=xpad, ypad=ypad,
                header_width=header_width, header_height=header_height,
                width=width, height=height,
                **args
            )

        self.draw_menu_button(
            ui=ui, master_tag=master_tag, tag=f"{tag_pref}_insert",
            menu_graph= [[structure_name,
                          partial(insert_item_refresh,
                                  structure_name)] for structure_name in self.insert_type],
            text='Insert Structure', coordinate=coordinate,
            width=width*5, height=height,
            background=col_buttons_2,
            **args
        )
        coordinate[1] += height+5

        coordinate[0] -= xpad*3
        end_coordinate = [coordinate[0], coordinate[1]]

        self.draw_collapse_button(
            root=root, ui=ui,
            master_tag=master_tag, tag=header_tag,
            text=f"Collapse {self.info}", font=header_font,
            coordinate=end_coordinate,
            width=header_width*2, height=header_height/1.5,
            background=col_header,
            **args)

        coordinate[1] += header_height/1.5 + ypad

        self.draw_label(
            ui=ui, master_tag=master_tag, tag=f'{tag_pref}_spanning_line',
            coordinate=[init_x, init_y],
            width=2, height=end_coordinate[1]-init_y,
            background=col_header,
            **args
        )


    def insert(self, component: ContentTreeNode, idx: int|None = None):
        # inserts a component to self.components at idx.
        #   Insert to the back if idx is None.
        if idx is None:
            self.components.append(component)
        else:
            self.components.insert(idx, component)
        component.setattr('parent',self)
    
    def insert_clone(self, idx: int):
        # inserts a copy of component self.components[idx] to idx.
        #   Insert to the back if idx is None.
        clone = get_content_tree(self.components[idx].as_dict)
        self.components.insert(idx, clone)
    
    def remove(self, component: ContentTreeNode, reset_parent = True):
        self.components.remove(component)
        if reset_parent:
            component.setattr('parent',None)
    
    def pop(self, idx: int, reset_parent = True):
        component = self.components.pop(idx)
        if reset_parent:
            component.setattr('parent',None)
        return component

    def replace(self, component1: ContentTreeNode, component2: ContentTreeNode):
        idx = self.components.index(component1)
        self.pop(idx, reset_parent=False)
        self.insert(component2, idx)
    
    def swap(self, idx1, idx2):
        # swaps self.components[idx1] and self.components[idx2]
        self.components[idx1], self.components[idx2] = \
            self.components[idx2], self.components[idx1]
    
    def pre_order(self):
        po = [self]
        for component in self.components:
            po += component.pre_order()
        return po


class Sequence(Itemization):
    '''
    Represents a list of line(s).

    content's key:
        "components"
    '''

    def __init__(self, content: dict = dict(), parent = None) -> None:
        super().__init__(content, parent)
        self.insert_type = ['HLine', 'Sequence', 'Header', 'TextLine', 'UnorderedList']

    def __str__(self):
        return f"Sequence([{self.components_str}, status={self.getattr('status')}])"


    @property
    def as_html(self):
        if self.getattr('status') == 0:
            return ""
        return f"{'\n'.join(component.as_html for component in self.components)}"


    @property
    def as_markdown(self):
        if self.status == 0:
            return ""
        return f"{'\n'.join(component.as_markdown for component in self.components
                            if component.getattr('status')==1)}"



class TextLine(Itemization):
    '''
    Represents a line containing a sequence of text.

    content's key:
        "components"
    '''
    def __init__(self, content: dict = dict(), parent = None) -> None:
        super().__init__(content, parent)
        self.insert_type = ['TextElement', 'URLElement', 'InlineList']
    
    def __str__(self):
        return f"TextLine([{self.components_str}, status={self.status}])"
    
    @property
    def as_html(self):
        if self.status == 0:
            return ""
        return super().as_html

    @property
    def as_markdown(self):
        if self.status == 0:
            return ""
        return super().as_markdown
    
    
    @property
    def display_color(self):
        return [GraphicalUserInterface.COL_SKY_1,
                GraphicalUserInterface.COL_GREEN_0,
                GraphicalUserInterface.COL_SKY_0,
                GraphicalUserInterface.COL_SKY_0,
                GraphicalUserInterface.COL_SKY_1]


class Header(TextLine):
    '''
    Represents a header.

    content's keys:
        "components"
        "level"
    '''
    def __init__(self, content: dict = dict(), parent = None) -> None:
        super().__init__(content, parent)
        self.level = str(content.get("level", '1'))
        self.attrs = ['level']
        self.insert_type = ['TextElement', 'URLElement', 'InlineList']
    
    def __str__(self):
        return f"Header([{self.components_str}], level={self.level}, status={self.status})"
    
    @property
    def as_dict(self):
        return super().as_dict | {
            "level": self.level,
        }
    
    @property
    def as_html(self):
        if self.status == 0:
            return ""
        return f"<h{self.level}>{super().as_html}</h{self.level}>"

    @property
    def as_markdown(self):
        if self.status == 0:
            return ""
        return f"\n\n{"#"*int(self.level)} {super().as_markdown}\n"
    
    @property
    def display_color(self):
        return [GraphicalUserInterface.COL_SKY_2,
                GraphicalUserInterface.COL_GREEN_0,
                GraphicalUserInterface.COL_SKY_0,
                GraphicalUserInterface.COL_SKY_1,
                GraphicalUserInterface.COL_SKY_2]
    

class InlineList(Itemization):
    '''
    Represents a list of node(s) (separated by comma).

    content's keys:
        "components"
    '''
    def __init__(self, content: dict = dict(), parent = None) -> None:
        super().__init__(content, parent)
        self.insert_type = ['TextElement', 'URLElement']


    def __str__(self):
        return f"InlineList([{self.components_str}, status={self.status}])"
    
    @property
    def as_html(self):
        if self.status == 0:
            return ""
        return f"{', '.join(component.as_html for component in self.components)}"

    @property
    def as_markdown(self):
        if self.status == 0:
            return ""
        return f"{', '.join(component.as_markdown for component in self.components)}"

    @property
    def display_color(self):
        return [GraphicalUserInterface.COL_GREEN_2,
                GraphicalUserInterface.COL_YELLOW_0,
                GraphicalUserInterface.COL_GREEN_0,
                GraphicalUserInterface.COL_GREEN_1,
                GraphicalUserInterface.COL_GREEN_0]

class UnorderedList(Itemization):
    '''
    Represents a list of node(s) (in separated lines).

    content's key:
        "components"
    '''

    def __init__(self, content: dict = dict(), parent = None) -> None:
        super().__init__(content, parent)
        self.insert_type = ['Header', 'TextLine', 'InlineList']

    def __str__(self):
        return f"UnorderedList([{self.components_str}, status={self.status}])"
    
    @property
    def as_html(self):
        if self.status == 0:
            return ""
        body = "".join(f"<li>{component.as_html}</li>" 
                       for component in self.components
                       if component.get_bottom_component().getattr('status')==1)
        return f"<ul>{body}</ul>"

    @property
    def as_markdown(self):
        if self.status == 0:
            return ""
        body = "".join(f"<li>{component.as_markdown}</li>"
                       for component in self.components
                       if component.get_bottom_component().getattr('status')==1)
        return f"<ul>{body}</ul>"
    
    @property
    def display_color(self):
        return [GraphicalUserInterface.COL_SKY_2,
                GraphicalUserInterface.COL_YELLOW_0,
                GraphicalUserInterface.COL_SKY_0,
                GraphicalUserInterface.COL_SKY_1,
                GraphicalUserInterface.COL_SKY_0]

class Tabular(Itemization):
    '''
    Represents a list of ContentTreeNodes in tabular format

    content's keys:
        "components"
        "table_width"
    '''
    def __init__(self, content: dict = dict(), parent = None) -> None:
        super().__init__(content, parent)
        self.table_width = str(content.get("table_width", '1'))
        self.attrs = ['table_width']
        self.insert_type = ['TextElement', 'URLElement']

    
    def __str__(self):
        return f"Tabular([{self.components_str}], table_width={self.table_width}, status={self.status})"
    
    @property
    def as_dict(self):
        return super().as_dict | {
            "table_width": self.table_width,
        }
    
    @property
    def width(self):
        try:
            return int(self.table_width)
        except Exception:
            return 3

    
    @property
    def as_html(self):
        if self.status == 0:
            return ""
        cmpn_len = len(self.components)
        html = '<table style="width:100%;border-collapse:collapse;text-align:left;table-layout: fixed;">'
        width = self.width
        for i in range(0, cmpn_len, width):
            row = self.components[i:i+width]
            inner = ''.join(f'<td>{component.as_html}</td>' for component in row if
                            component.get_bottom_component().getattr('status')==1)
            html += f"<tr>{inner}</tr>"
        html += '</table>'
        return html
    
    @property
    def as_markdown(self):
        if self.status == 0:
            return ""
        cmpn_len = len(self.components)
        md = '<table>'
        width = self.width
        for i in range(0, cmpn_len, width):
            row = self.components[i:i+width]
            inner = ''.join(f'<td>{component.as_markdown}</td>' for component in row)
            md += f"<tr>{inner}</tr>"
        md += '</table>\n'
        return md 
    
    @property
    def display_color(self):
        return [GraphicalUserInterface.COL_SKY_2,
                GraphicalUserInterface.COL_YELLOW_0,
                GraphicalUserInterface.COL_SKY_0,
                GraphicalUserInterface.COL_SKY_1,
                GraphicalUserInterface.COL_SKY_0]


class Decorator(ContentTreeNode):
    '''
    Base class of Decorators (similar to the Decorator class in the decoration pattern)

    content's key:
        "component"
    '''
    def __init__(self, content: dict = dict(), parent = None) -> None:
        super().__init__(content, parent)
        self.set_component(
            get_content_tree(content.get("component", TextElement().as_dict)
            ))
        self.attrs = list()
        self.decorator_type = []

    def __str__(self) -> str:
        return f"Decorator({self.component.__str__()}, status={self.status})"
    
    @property
    def class_name(self):
        return self.__class__.__name__

    @property
    def as_dict(self):
        return super().as_dict | {
            "component": self.component.as_dict,
        }

    @property
    def as_html(self):
        content_html = self.component.as_html
        if self.status == 0:
            return content_html
        return f'<span style="{self.get_style()}">{content_html}</span>'

    @property
    def as_markdown(self):
        return self.component.as_markdown

    

    def draw_editor(
            self,
            root,
            ui: GraphicalUserInterface,
            master_tag:str,
            tag_pref: str = "rc",
            coordinate: list = [0, 0],
            header_font: tuple = None,
            font:tuple = None,
            xpad = 20,
            ypad = 20, 
            header_width = 200,
            header_height = 30, 
            width = 50,
            height = 20,
            **args):
        self.component.draw_editor(
            root=root, ui=ui,
            master_tag=master_tag, tag_pref=f"{tag_pref}_1",
            coordinate=coordinate,
            header_font=header_font, font=font,
            xpad=xpad, ypad=ypad,
            header_width=header_width, header_height=header_height,
            width=width, height=height,
            **args
        )

    def draw_config(
            self,
            root,
            ui: GraphicalUserInterface,
            master_tag: str,
            tag: str,
            font: tuple = None,
            coordinate: list = [0, 0],
            width=100,
            height=15,
            **args
    ):
        name = self.class_name
        tag = f'{tag}_{name}'
        bwidth = height*0.5
        init_x = coordinate[0]
        self.draw_binary_button(
            ui=ui, master_tag=master_tag, attr_tag=tag,
            attr_name='status', colors=['white', 'green'],
            font=font, coordinate=[coordinate[0]-bwidth-5, coordinate[1]],
            width=bwidth, height=bwidth,
            pady=(height*1.2-bwidth)/2,
            **args
        )

        self.draw_label(
            ui=ui, master_tag=master_tag, tag=tag,
            text=name, font=font,
            coordinate=coordinate,
            width=width,height=height*1.2,
            **args)
        coordinate[0] += width

        if not self.temp.get('expand', False):
            self.draw_expand_button(
                root=root, ui=ui, master_tag=master_tag, tag=tag,
                text='Expand', font=font,
                coordinate=coordinate,
                width=width, height=height,
                **args
            )
            coordinate[0] = init_x
            coordinate[1] += height*1.2+5
            return
        
        self.draw_collapse_button(
                root=root, ui=ui, master_tag=master_tag, tag=tag,
                text='Collapse', font=font,
                coordinate=coordinate,
                width=width, height=height,
                **args
        )
        
        coordinate[0] = init_x+width/2
        coordinate[1] += height*1.2+5

        self.draw_attr_editor(
            ui=ui, master_tag=master_tag, tag=tag, attrs=self.attrs,
            font=font, coordinate=coordinate,
            line_width=4,
            label_width=width, label_height=height,
            text_width=width, text_height=height,
            button_width=width, button_height=height, button_pady=0,
            **args
        )
        coordinate[0] = init_x

    def set_component(self, component: ContentTreeNode):
        self.component = component
        self.component.setattr('parent',self)
    
    def get_style(self):
        return ""
    
    def replace(self, component1: ContentTreeNode, component2: ContentTreeNode):
        if component1 == self.component:
            self.component = component2
            self.component.setattr('parent',self)
    
    def parent_replace(self, component):
        if not self.parent is None:
            self.parent.replace(self, component)

    def pop(self):
        return self.component
    
    def pop_self(self):
        self.component.parent = self.parent
        if not self.parent is None:
            self.parent.replace(self, self.component)
        return self.component

    def pre_order(self):
        return [self] + self.component.pre_order()


class StyledFont(Decorator):
    '''
    Font decorator.

    content's key:
        "component"
        "font_size"
        "font_family"
        "bold",
        ""

    '''
    def __init__(self, content: dict = dict(), parent = None) -> None:
        super().__init__(content, parent)
        self.font_size: str = content.get('font_size', '1em')
        self.font_family: str = content.get("font_family", 'Montserrat')
        self.bold: int = content.get("bold", 0)
        self.italic: int = content.get("italic", 0)
        self.underline: int = content.get("underline", 0)
        self.attrs = ['font_size', 'font_family','bold', 'italic', 'underline']


    def  __str__(self):
        return f'StyledFont({self.component.__str__()}, ' + \
            f'font_size={self.font_size}, font_family: {self.font_family}, ' + \
            f'style={self.get_font_style()}, status={self.status})'
    
    @property
    def as_dict(self):
        return super().as_dict | {
            "font_size": self.font_size,
            "font_family": self.font_family,
            "bold": self.bold,
            "italic": self.italic,
            "underline": self.underline,
        }
    
    @property
    def as_html(self):
        return super().as_html
    
    @property
    def as_markdown(self):
        if self.status == 0:
            return self.component.as_markdown
        body = super().as_markdown
        styles = self.get_font_style()
        return f'<span style="{styles}">{body}</span>'

    def get_style(self):
        return f"font: {self.font_size} {self.font_family};" + self.get_font_style()
    
    def get_font_style(self):
        styles = ""
        if self.bold == 1:
            styles += "font-weight: bold;"
        if self.italic == 1:
            styles += "font-style: italic;"
        if self.underline == 1:
            styles += "text-decoration-line: underline;"
        return styles



class BoxMargin(Decorator):
    '''
    Margin Decorator.

    content's keys:
        "components"
        "margin_n"
        "margin_e"
        "margin_s"
        "margin_w"
    '''
    def __init__(self, content: dict = dict(), parent = None) -> None:
        super().__init__(content, parent)
        self.margin_n = content.get("margin_n", "0px")
        self.margin_e = content.get("margin_e", "0px")
        self.margin_s = content.get("margin_s", "0px")
        self.margin_w = content.get("margin_w", "0px")
        self.attrs = ["margin_n", "margin_e", "margin_s", "margin_w"]

    def  __str__(self):
        return f'BoxMargin({self.component}, style={self.get_style()}, status={self.status})'
    
    @property
    def as_dict(self):
        return super().as_dict | {
            "margin_n": self.margin_n,
            "margin_e": self.margin_e,
            "margin_s": self.margin_s,
            "margin_w": self.margin_w,
        }
    
    @property
    def as_html(self):
        content_html = self.component.as_html
        if self.status == 0:
            return content_html
        return f'<div style="{self.get_style()}">{content_html}</div>'

    
    @property
    def as_markdown(self):
        content_md = self.component.as_markdown
        if self.status == 0:
            return content_md
        lines = content_md.split('\n')
        return '\n'.join(f'> {line}' for line in lines)

    def get_style(self):
        return f'margin: {self.margin_n} {self.margin_e} {self.margin_s} {self.margin_w};'



'''
Functions that generate ContentTreeNodes
'''
def get_content_tree(content: dict|None) -> ContentTreeNode:
    if content is None:
        return None
    return getattr(sys.modules[__name__], content["type"])(content)



def create_text_sequence(value: str):
    # creates a basic text Sequence.
    return TextLine({"components": [{"type": "TextElement", "value": f"{value}"}]})


def create_header(value:str, level:int):
    # creates a basic Header.
    return Header({
        "components": [{"type": "TextElement", "value": f"{value}"}],
        "level": level
    })


def create_pair(key: str, element: str|tuple[str, str]|None = None):
    # creates a key-value pair (key: value).
    pair = TextLine({"info": f"{key}"})
    key_element = StyledFont({
        "bold": 1
    })
    key_element.set_component(TextElement({"value": f"{key}: "}))
    pair.insert(key_element)
    if not element is None:
        if isinstance(element, str):
            pair.insert(TextElement({"value": f"{element}"}))
        else:
            pair.insert(URLElement({"value": f"{element[0]}", "url": f"{element[1]}"}))
    return pair


def create_key_list_pair(key: str, inline_list: list[str]):
    # create a key-value pair (key: value), where the value is an inline list.
    pair = create_pair(key)
    value = InlineList()
    for element in inline_list:
        value.insert(TextElement({"value": f"{element}"}))
    pair.insert(value)
    return pair


def create_bold_tabular(elements: list[str|tuple[str, str]], width = 3):
    # creates a bold tabular texts and urls
    tabular_row_content = Tabular({"table_width": width})
    for element in elements:
        fs = StyledFont({'bold': 1})
        if isinstance(element, str):
            tabular_row_content.insert(
                TextElement(
                    {"value": f"{element}"}
                ).decorated(fs)
            )
        else:
            tabular_row_content.insert(
                URLElement(
                    {"value": f"{element[0]}", "url": f"{element[1]}"}
                ).decorated(fs)
            )
    return tabular_row_content
