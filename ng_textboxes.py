class NGs_TextBox_SIMPLE:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "text_1": ("STRING", {"multiline": True, "dynamicPrompts": True}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text_1",)
    FUNCTION = "hand_over"

    CATEGORY = "NeoGriever/TextBoxes"

    def hand_over(self, text_1):
        return (text_1,)


class NGs_TextBox_JOIN:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "text_1": ("STRING", {"multiline": True, "dynamicPrompts": True}),
                "divider": ("STRING", {"default": "\n"})
            },
            "optional": {
                "text": ("STRING", {"forceInput": True}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text_1",)
    FUNCTION = "hand_over"

    CATEGORY = "NeoGriever/TextBoxes"

    def hand_over(self, text_1, divider, text):
        return (text_1 + divider + text,)


class NGs_TextBox_x2:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "text_1": ("STRING", {"multiline": True, "dynamicPrompts": True}),
                "text_2": ("STRING", {"multiline": True, "dynamicPrompts": True}),
            }
        }

    RETURN_TYPES = ("STRING", "STRING",)
    RETURN_NAMES = ("text_1", "text_2",)
    FUNCTION = "hand_over"
    CATEGORY = "NeoGriever/TextBoxes"

    def hand_over(self, text_1, text_2):
        return (text_1, text_2,)


class NGs_TextBox_x3:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "text_1": ("STRING", {"multiline": True, "dynamicPrompts": True}),
                "text_2": ("STRING", {"multiline": True, "dynamicPrompts": True}),
                "text_3": ("STRING", {"multiline": True, "dynamicPrompts": True}),
            }
        }

    RETURN_TYPES = ("STRING", "STRING", "STRING",)
    RETURN_NAMES = ("text_1", "text_2", "text_3",)
    FUNCTION = "hand_over"
    CATEGORY = "NeoGriever/TextBoxes"

    def hand_over(self, text_1, text_2, text_3):
        return (text_1, text_2, text_3,)
