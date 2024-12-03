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
    "NeoGriever's Multimask - Write": "NGs_Multimask_Write",
    "NeoGriever's Multimask - Read": "NGs_Multimask_Read",
    "NeoGriever's Conditioning - Better CLIP Text Encoder": "NGs_BetterCLIPTextEncode",
    "NeoGriever's Resolutions - Resolution Provider": "NGs_ResolutionProvider",
    "NeoGriever's TextBoxes - Simple": "NGs_TextBox_SIMPLE",
    "NeoGriever's TextBoxes - Join": "NGs_TextBox_JOIN",
    "NeoGriever's TextBoxes - x2": "NGs_TextBox_x2",
    "NeoGriever's TextBoxes - x3": "NGs_TextBox_x3",
    "NeoGriever's Sliders - INT": "NGs_Sliders_INT",
    "NeoGriever's Sliders - FLOAT": "NGs_Sliders_FLOAT",
    "NeoGriever's Sliders - STEPPER": "NGs_Sliders_PERCENTAGECUT",
}
