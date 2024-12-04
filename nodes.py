from .ng_multimask import *
from .ng_conditioning import *
from .ng_resolution import *
from .ng_textboxes import *
from .ng_sliders import *
from .ng_string import *
from .ng_other import *

NODE_CLASS_MAPPINGS = {
    "NGs_Multimask_Write": NGs_Multimask_Write,
    "NGs_Multimask_Read": NGs_Multimask_Read,

    "NGs_BetterCLIPTextEncode": NGs_BetterCLIPTextEncode,

    "NGs_ResolutionProvider": NGs_ResolutionProvider,

    "NGs_TextBox_SIMPLE": NGs_TextBox_SIMPLE,
    "NGs_TextBox_JOIN": NGs_TextBox_JOIN,
    "NGs_TextBox_x2": NGs_TextBox_x2,
    "NGs_TextBox_x3": NGs_TextBox_x3,

    "NGs_Sliders_INT": NGs_Sliders_INT,
    "NGs_Sliders_FLOAT": NGs_Sliders_FLOAT,
    "NGs_Sliders_PERCENTAGECUT": NGs_Sliders_PERCENTAGECUT,

    "NGs_String_Operator": NGs_String_Operator,
    "NGs_String_Squisher": NGs_String_Squisher,
    "NGs_Text_Cut_String": NGs_Text_Cut_String,

    "NGs_Create_Solid_Color": NGs_Create_Solid_Color,
    "NGs_Fill_with_Color": NGs_Fill_with_Color,
    "NGs_Checkerboard_Generator": NGs_Checkerboard_Generator,
    "NGs_Image_Progress_Bar": NGs_Image_Progress_Bar,
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "NGs_Multimask_Write": "NGs Multimask - Write",
    "NGs_Multimask_Read": "NGs Multimask - Read",

    "NGs_BetterCLIPTextEncode": "NGs Conditioning - Better CLIP Text Encoder",

    "NGs_ResolutionProvider": "NGs Resolutions - Resolution Provider",

    "NGs_TextBox_SIMPLE": "NGs TextBoxes - Simple",
    "NGs_TextBox_JOIN": "NGs TextBoxes - Join",
    "NGs_TextBox_x2": "NGs TextBoxes - x2",
    "NGs_TextBox_x3": "NGs TextBoxes - x3",

    "NGs_Sliders_INT": "NGs Sliders - INT",
    "NGs_Sliders_FLOAT": "NGs Sliders - FLOAT",
    "NGs_Sliders_PERCENTAGECUT": "NGs Sliders - STEPPER",

    "NGs_String_Operator": "NGs String - String Tool",
    "NGs_String_Squisher": "NGs String - String Squisher",
    "NGs_Text_Cut_String": "NGs String - String Cutter",

    "NGs_Create_Solid_Color": "NGs Image - Create Solid Color",
    "NGs_Fill_with_Color": "NGs Image - Fill with Color",
    "NGs_Checkerboard_Generator": "NGs Image - Checkerboard Generator",
    "NGs_Image_Progress_Bar": "NGs Image - Image Progress Bar",
}
