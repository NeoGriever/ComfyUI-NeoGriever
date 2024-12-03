import torch
import numpy as np
from PIL import Image
from nodes import MAX_RESOLUTION


class NGs_Multimask_Write:

    def __init__(self):
        pass

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("Multimask Image",)

    FUNCTION = "apply_channel_mask"
    CATEGORY = "NeoGriever/Multimask"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "width": ("INT", {
                    "default": 512,
                    "min": 8,
                    "max": MAX_RESOLUTION,
                    "step": 8
                }),
                "height": ("INT", {
                    "default": 512,
                    "min": 8,
                    "max": MAX_RESOLUTION,
                    "step": 8
                }),
                "channel": (["red", "green", "blue"], {"default": "red"}),
                "level": ([1, 2, 4, 8, 16, 32, 64, 128], {"default": 1}),
            },
            "optional": {
                "image": ("IMAGE", {"default": None}),
                "mask": ("MASK", {"default": None}),
            }
        }

    def numpy2pil(self, image: np.ndarray, mode=None):
        return Image.fromarray(np.clip(255.0 * image, 0, 255).astype(np.uint8), mode)

    def tensor2pil(self, image: torch.Tensor, mode=None):
        return self.numpy2pil(image.cpu().numpy().squeeze(), mode=mode)

    def apply_channel_mask(self, width, height, channel, level, mask=None, image=None):
        # Bestimmen des Farbkanals und Festlegen des Farbwerts für Schwarz
        channel_index = {"red": 0, "green": 1, "blue": 2}[channel]

        # Bild erstellen, falls keines übergeben wurde
        if image is None:
            r = torch.full([1, height, width, 1], 0.0)
            g = torch.full([1, height, width, 1], 0.0)
            b = torch.full([1, height, width, 1], 0.0)
            a = torch.full([1, height, width, 1], 1.0)
            image = torch.cat((r, g, b, a), dim=-1)
        else:
            width = image.shape[2]
            height = image.shape[1]

        if mask is not None:
            mask = mask.expand(1, height, width)
            for y in range(height):
                for x in range(width):
                    if mask[0, y, x] > 0:
                        current_value = int(image[0, y, x, channel_index].item() * 255)
                        new_value = current_value | level
                        new_value = min(new_value, 255)
                        image[0, y, x, channel_index] = new_value / 255.0

        return (image,)


class NGs_Multimask_Read:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "channel": (["red", "green", "blue"], {"default": "red"}),
                "level": ([1, 2, 4, 8, 16, 32, 64, 128], {"default": 1}),
            }
        }

    RETURN_TYPES = ("MASK",)
    RETURN_NAMES = ("Mask",)

    FUNCTION = "extract_channel_mask"
    CATEGORY = "NeoGriever/Multimask"

    def extract_channel_mask(self, image, channel, level):
        channel_index = {"red": 0, "green": 1, "blue": 2}[channel]
        channel_bit = 1 << (level.bit_length() - 1)
        height, width = image.shape[1], image.shape[2]
        mask = torch.zeros((1, height, width))
        for y in range(height):
            for x in range(width):
                channel_value = int(image[0, y, x, channel_index].item() * 255)
                if (channel_value & channel_bit) == channel_bit:
                    mask[0, y, x] = 1.0

        return (mask,)
