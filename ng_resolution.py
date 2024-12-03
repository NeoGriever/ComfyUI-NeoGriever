MAX_RESOLUTION = 16384


class NGs_ResolutionProvider:
    RESOLUTION_PRESET_NAMES = [
        "◽ Custom",
        "☑️✨ 1:1 Square",
        "🖥️✨ 16:9 Widescreen",
        "📱✨ 9:16 Portrait",
        "🖥️ 9:7 Widescreen",
        "🖥️ 2:1 Widescreen",
        "🖥️ 3:1 Widescreen",
        "🖥️ 3:2 Widescreen",
        "🖥️ 20:9 Widescreen",
        "🖥️ 21:9 Widescreen",
        "🖥️ 31:9 Widescreen",
        "📱 7:9 Portrait",
        "📱 1:2 Portrait",
        "📱 1:3 Portrait",
        "📱 2:3 Portrait",
        "📱 9:20 Portrait",
        "📱 9:21 Portrait",
        "📱 9:31 Portrait",
    ]
    RESOLUTION_PRESETS = [
        {"w": -1, "h": -1},
        {"w": 1024, "h": 1024},
        {"w": 1366, "h": 768},
        {"w": 768, "h": 1366},
        {"w": 1152, "h": 896},
        {"w": 1428, "h": 714},
        {"w": 1749, "h": 583},
        {"w": 1216, "h": 832},
        {"w": 1260, "h": 567},
        {"w": 1536, "h": 640},
        {"w": 1873, "h": 544},
        {"w": 896, "h": 1152},
        {"w": 714, "h": 1428},
        {"w": 583, "h": 1749},
        {"w": 832, "h": 1216},
        {"w": 567, "h": 1260},
        {"w": 640, "h": 1536},
        {"w": 544, "h": 1874}
    ]

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "preset": (s.RESOLUTION_PRESET_NAMES, {"default": RESOLUTION_PRESET_NAMES[1]}),
                "width": ("INT", {"default": 1024, "min": 16, "max": MAX_RESOLUTION, "step": 1}),
                "height": ("INT", {"default": 1024, "min": 16, "max": MAX_RESOLUTION, "step": 1}),
                "scale": ("FLOAT", {"default": 1.0, "min": 0.25, "max": 4.0, "step": 0.25}),
                "fit8": ("BOOLEAN", {"default": True, "label_off": "No", "label_on": "Yes"}),
            }
        }

    RETURN_TYPES = ("INT", "INT",)
    FUNCTION = "get_resolution"

    CATEGORY = "NeoGriever/Resolutions"
    DESCRIPTION = """Did i really need a description for this?"""

    def get_resoltuion(self, preset, width, height, scale, fit8):
        if preset is not self.RESOLUTION_PRESET_NAMES[0]:
            preset = self.RESOLUTION_PRESETS[self.RESOLUTION_PRESET_NAMES.index(preset)]
            width = preset["w"]
            height = preset["h"]
        width = width * scale
        height = height * scale
        if fit8:
            width = (width + 7) // 8 * 8
            height = (height + 7) // 8 * 8
        return (width, height,)
