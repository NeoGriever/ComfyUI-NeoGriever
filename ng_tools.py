from ng_multimask import *
from ng_conditioning import *
from ng_resolution import *
from ng_textboxes import *
from ng_sliders import *

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
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "NGs Multimask - Write": "NGs_Multimask_Write",
    "NGs Multimask - Read": "NGs_Multimask_Read",
    "NGs Conditioning - Better CLIP Text Encoder": "NGs_BetterCLIPTextEncode",
    "NGs Resolutions - Resolution Provider": "NGs_ResolutionProvider",
    "NGs TextBoxes - Simple": "NGs_TextBox_SIMPLE",
    "NGs TextBoxes - Join": "NGs_TextBox_JOIN",
    "NGs TextBoxes - x2": "NGs_TextBox_x2",
    "NGs TextBoxes - x3": "NGs_TextBox_x3",
    "NGs Sliders - INT": "NGs_Sliders_INT",
    "NGs Sliders - FLOAT": "NGs_Sliders_FLOAT",
    "NGs Sliders - STEPPER": "NGs_Sliders_PERCENTAGECUT",
}
