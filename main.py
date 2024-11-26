from src.resume_builder import *
from src.ui import *

if __name__ == "__main__":
    ui = GraphicalUserInterface("DreamCraft", 900, 600)
    rb = ResumeBuilder(ui)
    rb.proc()