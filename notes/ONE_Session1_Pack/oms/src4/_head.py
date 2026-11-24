import re, copy, zipfile, shutil, os, datetime as dt
from docx import Document
from docx.shared import Pt, Inches, RGBColor, Emu
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.enum.style import WD_STYLE_TYPE
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.section import WD_SECTION
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from parts4 import WELCOME, GLANCE, WHY, HOWTO, PART_A, WORK, PART_B_INTRO, PART_C, PART_D, appendix_blocks
from elements import ELEMENTS
from register import ref, DOCS

IMG = "/home/claude/oms/img"; OUT = "/home/claude/oms/out"; os.makedirs(OUT, exist_ok=True)
INK, TEAL, FLARE, SAND, SKY, MUTE = "12232E", "0E5A6B", "F26B21", "F6F1E8", "A7D8E3", "5B6B73"
ELC = {1:"0B4F5E",2:"0F6B7A",3:"1E8796",4:"3AA3AE",5:"D9480F",6:"F26B21",7:"F5923E",8:"F8B26A",9:"3D5A80",10:"5C7BA6"}
GROUP = {1:"LEAD",2:"LEAD",3:"LEAD",4:"LEAD",5:"CONTROL",6:"CONTROL",7:"CONTROL",8:"CONTROL",9:"LEARN",10:"LEARN"}
HFONT, BFONT = "Segoe UI Semibold", "Calibri"
