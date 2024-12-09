import requests
from PIL import Image
import io
from ng_other import tensor2pil


class NGs_Discord_Webhook:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE", {"forceInput": True}),
                "webhook_url": ("STRING", {"multiline": False}),
            },
            "optional": {
                "add_background": (
                "BOOLEAN", {"default": False, "label_on": "Add Background", "label_off": "No Background"}),
                "background_color": ("STRING", {"default": "#000000", "multiline": False}),
            }
        }

    RETURN_TYPES = ("IMAGE", "STRING", "STRING",)
    RETURN_NAMES = ("image", "msg_id", "discord_image_url",)
    OUTPUT_IS_LIST = (True, True, True,)
    FUNCTION = "send_to_discord"
    CATEGORY = "NeoGriever/Communication"
    OUTPUT_NODE = True

    @staticmethod
    def hex_to_rgb(hex_color):
        """Convert a hex color string (#RRGGBB) to an (R, G, B) tuple."""
        hex_color = hex_color.lstrip("#")
        if len(hex_color) != 6:
            return (0, 0, 0)
        try:
            return tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))
        except ValueError:
            return (0, 0, 0)

    def send_to_discord(self, image, webhook_url, add_background=False,
                        background_color="#000000"):
        msg_ids = []
        discord_image_urls = []

        def send_payload(images):
            payload = {}
            response = requests.post(webhook_url, data={"payload_json": str(payload)}, files=files)
            if response.status_code not in (200,):
                print(response.json())
                return
            response_data = response.json()
            msg_ids.append(response_data.get("id"))
            attachments = response_data.get("attachments", [])
            discord_image_urls.extend([attachment["url"] for attachment in attachments])

        files = {}
        amount_files = 0
        for (idx, img) in enumerate(image):
            if amount_files == 10:
                send_payload(files)
                amount_files = 0
                files = {}

            pil_image = tensor2pil(img)
            if add_background:
                rgb_color = self.hex_to_rgb(background_color or "#000000")
                bg_image = Image.new("RGB", pil_image.size, rgb_color)
                bg_image.paste(pil_image, (0, 0), pil_image if pil_image.mode == "RGBA" else None)
                pil_image = bg_image
            byte_stream = io.BytesIO()
            pil_image.save(byte_stream, format="PNG")
            byte_stream.seek(0)
            files[f"file{idx}"] = (f"image{idx}.png", byte_stream, "image/png")
            amount_files += 1

        send_payload(files)

        return (image, msg_ids, discord_image_urls,)
