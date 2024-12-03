class NGs_Sliders_INT:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "value": ("INT", {"default": 0, "min": 0, "max": 100, "display": "slider"}),
            },
        }

    RETURN_TYPES = ("INT",)
    RETURN_NAMES = ("value",)
    FUNCTION = "hand_over"
    CATEGORY = "NeoGriever/Sliders"

    def hand_over(self, value):
        return (value,)


class NGs_Sliders_FLOAT:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "value": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 1.0, "display": "slider"}),
            },
        }

    RETURN_TYPES = ("FLOAT",)
    RETURN_NAMES = ("value",)
    FUNCTION = "hand_over"
    CATEGORY = "NeoGriever/Sliders"

    def hand_over(self, value):
        return (value,)


class NGs_Sliders_PERCENTAGECUT:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "steps": ("INT", {"default": 50, "min": 1, "max": 10000, "display": "slider"}),
                "percentage": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 1.0, "display": "slider"}),
            },
        }

    RETURN_TYPES = ("INT", "INT",)
    RETURN_NAMES = ("steps",
                    "cut",)  # returns the steps itself and the result of steps * percentage (lowered (15.9 = 15 as example) as whole number (INT))
    FUNCTION = "hand_over"
    CATEGORY = "NeoGriever/Sliders"

    def hand_over(self, steps, percentage):
        cut = int(steps * percentage)
        return (steps, cut,)
