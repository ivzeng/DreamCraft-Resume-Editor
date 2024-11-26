from src.resume_builder import *
from src.ui import *

if __name__ == "__main__":
    ui = GraphicalUserInterface("DreamJobCraft", 900, 600)
    rb = ResumeBuilder(ui)
    rb.proc()