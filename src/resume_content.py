"""
File: component_classes.py

Description:
    This module contains a wrapper class of ContentTreeNode. It cantains functions to
load/save the resume content, produce Markdown/HTML conversion of the ContentTreeNode,
and import the pdf.
"""



import asyncio
from playwright.async_api import async_playwright
import os
import os.path as osp
import json
import pymupdf
from PIL import Image

from .ui import *
from .resume_content_tree import *



class ResumeContent:
    def __init__(self, resume_id = "resume_0") -> None:
        self.id = resume_id
        self.content = self.load()
    
    def __str__(self) -> str:
        return f"Resume id: {self.id}\n\n{self.content.__str__()}"
    
    @property
    def content_path(self):
        return f"resume/{self.id}"
    
    @property
    def as_dict(self) -> dict:
        # returns the dictionary of the class contents
        return {"content": self.content.as_dict}
    
    @property
    def as_markdown(self) -> dict:
        # returns the dictionary of the class contents
        return self.content.as_markdown
    
    @property
    def as_html(self) -> dict:
        # returns the dictionary of the class contents
        header = '''
<!DOCTYPE html><html><head><title>My Resume</title>
    <style>
        body {
            height: 612px;
            width: 791px;
            margin-left: 50px;
            margin-right: 50px;
        }
    </style></head>
    '''
        return f"{header}<body>{self.content.as_html}</body>"
    
    def to_pdf(self, path:str = None):
        # import the pdf version of the resume
        asyncio.run(self.import_pdf(path))
    
    async def import_pdf(self, path: str = None) -> None:
        async with async_playwright() as p:
            if path is None:
                path = f"{self.content_path}.pdf"
            browser = await p.chromium.launch()
            page = await browser.new_page()
            await page.set_content(self.as_html)
            await page.pdf(path=path)
            await browser.close()
    

    def as_images(self) -> list:
        path = 'temp/temp.pdf'
        self.to_pdf(path)
        content_pdf = pymupdf.open(path)
        images = list()
        for page in content_pdf:
            pix = page.get_pixmap()
            image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            images.append(image)
        return images

    
    def load(self, path = None):
        if path is None:
            path = f"{self.content_path}.json"
        if not osp.exists(path):
            os.makedirs(os.path.dirname(path), exist_ok=True)
            return self.create_template()
        with open(path, 'r') as f:
            return get_content_tree(json.loads(f.read()))
    
    def save(self, path = None):
        if path is None:
            path = f"{self.content_path}.json"
        if not osp.exists(path):
            os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w') as f:
            f.write(json.dumps(self.content.as_dict, indent=4))


    def create_template(self) -> ContentTreeNode:
        content = Sequence({"info": "Resume"})
        content.insert(self.basic_info_template())
        content.insert(self.education_section_template())
        content.insert(self.sample_section_template("Experience"))
        content.insert(self.sample_section_template("Projects"))
        content.insert(self.skill_template())
        return content.decorated(
            StyledFont({"font_family": "Montserrat", "font_size": "1em"})
            ).decorated(
                BoxMargin({
                    "margin_n": "20px",
                    "margin_s": "20px",
                    "margin_e": "20px",
                    "margin_w": "20px",
            }))


    def parse(self, content: dict) -> ContentTreeNode:
        return get_content_tree(content)

    
    def basic_info_template(self) -> Sequence:
        name = create_header("[Your Name]", 1)
        name.setattr("info", "Name")
        title = create_header("[Your Title]", 2).decorated(
            BoxMargin({"margin_n": "-20px", "margin_w": "10px"}))
        title.setattr("info", "title")

        info = Tabular({"info": "Details", "table_width": 3})
        info.insert(create_pair("Address", "[Your Address]"))
        info.insert(create_pair("Phone", "[Your Phone Number]"))
        info.insert(create_pair("Email", "[Your Email]"))
        info.insert(
            create_pair(
                "LinkedIn", 
                ("[Your LinkedIn Profile]", "[Your LinkedIn Profile Link]")))
        info.insert(
            create_pair(
                "Github", 
                ("[Your Github Profile]", "[Your Github Profile Link]")))

        basic_info = Sequence({"info": "Basic Info"})
        basic_info.insert(name)
        basic_info.insert(title)
        basic_info.insert(info.decorated(
            BoxMargin({"margin_n": "-20px", "margin_w": "20px"})))
        return basic_info
    

    def education_section_template(self):

        education_info = Sequence({"info": "Education Sample(s)"})
        education_info.insert(self.education_sample_template())

        education = self.section_header_template("Education")
        education.insert(education_info.decorated(
            BoxMargin({"margin_n": "-5px", "margin_w": "10px",})
        ))
        return education
    
    
    def education_sample_template(self):
        header = create_bold_tabular(["[School Location]", "[School Name]", "[Period]"])
        header.setattr("info", "General Info")
        details = UnorderedList({"info": "Details"})
        details.insert(
            create_key_list_pair(
                "Major",["[Major 1]", "[Major 2]", "..."]))
        details.insert(
            create_key_list_pair(
                "Certificate (Minor)", ["[Minor 1]", "[Minor 2]", "..."]))
        details.insert(
            create_key_list_pair(
                "Relevant Coursework",
                ["[Course A]", "[Course B]", "[Course C]", "[Course D]" "..."]))
        sample = Sequence({"info": "Education Sample"})
        sample.insert(header)
        sample.insert(details.decorated(
            BoxMargin({"margin_n": "-15px", "margin_w": "0px", "margin_s": "-10px",})
        ))
        return sample

    
    def sample_section_template(self, section_name: str):
        samples = Sequence({"info": "Samples"})
        samples.insert(self.sample_template())
        samples.insert(self.sample_template())

        section = self.section_header_template(section_name)
        section.insert(samples.decorated(
            BoxMargin({"margin_n": "-5px", "margin_w": "10px"})))
        return section
    
    def sample_template(self):
        header = create_bold_tabular(
            ["[Project Name/Title]", "[Company]", "[Period]", ("[Link to Project]", "https://github.com/ivzeng")]
        )
        header.setattr("info", "General Info")
        details = UnorderedList({"info": "Details"})
        details.insert(create_text_sequence("[description 1]"))
        details.insert(create_text_sequence("[description 2]"))
        details.insert(create_key_list_pair(
            "Utilized", ["Tool 1", "Tool 2", "Skill 1",  "Skill 2", "..."]
        ))
        sample = Sequence({"info": "Sample"})
        sample.insert(header)
        sample.insert(details.decorated(
            BoxMargin({"margin_n": "-15px", "margin_w": "0px", "margin_s": "-10px",})
        ))
        return sample

    
    def skill_template(self):
        details = UnorderedList({"info": "Skill Categories"})
        details.insert(create_key_list_pair(
            "Technical Skills", 
            ["Programming Languages", "Frameworks/Libraries", "Databases", "Tools"]))
        details.insert(create_key_list_pair(
            "Analytical Skills",
            ["Optimization", "algorithms", "Data Analysis"]))
        details.insert(create_key_list_pair(
            "Soft Skills",
            ["Teamwork", "Problem Solving", "Time Management"]))
        
        skills = self.section_header_template("Skills")
        skills.insert(details.decorated(
            BoxMargin({"margin_n": "-15px", "margin_w": "0px", "margin_s": "-10px",})
        ))

        return skills
    
    def section_header_template(self, section_name:str):
        header_title = create_header(section_name, 2).decorated(
            StyledFont({"font_family": "Montserrat"})
        )
        header = Sequence({"info": section_name})
        header.insert(header_title)
        header.insert(HLine().decorated(BoxMargin(
            {"margin_n": "-20px",}
        )))
        return header
    
    def draw_workspace(
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
        self.content.draw_editor(
            root=root, ui=ui,
            master_tag=master_tag, tag_pref=tag_pref,
            coordinate=coordinate,
            header_font=header_font, font=font,
            xpad=xpad, ypad=ypad,
            header_width=header_width, header_height=header_height,
            width=width, height=height,
            **args)


if __name__ == "__main__":
    rc = ResumeContent()
    print(rc.as_dict)
    #print(rc.as_markdown)
    #print(rc.as_html)
    #with open("test.md", 'w') as f:
    #    f.write(rc.as_markdown)
    #with open("test.html", 'w') as f:
    #    f.write(rc.as_html)
    rc.to_pdf("test.pdf")
    rc.save(f"{rc.content_path}.json")