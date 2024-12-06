from nodes import MAX_RESOLUTION
import torch
import numpy as np
import random
from PIL import Image, ImageDraw


# Tensor to PIL
def tensor2pil(image):
    return Image.fromarray(np.clip(255. * image.cpu().numpy().squeeze(), 0, 255).astype(np.uint8))


# Convert PIL to Tensor
def pil2tensor(image):
    return torch.from_numpy(np.array(image).astype(np.float32) / 255.0).unsqueeze(0)


class NGs_Create_Solid_Color:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "width": ("INT", {"default": 512, "min": 1, "max": MAX_RESOLUTION}),
                "height": ("INT", {"default": 512, "min": 1, "max": MAX_RESOLUTION}),
                "red": ("INT", {"default": 255, "min": 0, "max": 255, "step": 1, "display": "slider"}),
                "green": ("INT", {"default": 255, "min": 0, "max": 255, "step": 1, "display": "slider"}),
                "blue": ("INT", {"default": 255, "min": 0, "max": 255, "step": 1, "display": "slider"}),
                "alpha": ("INT", {"default": 255, "min": 0, "max": 255, "step": 1, "display": "slider"}),
                "mode": (["RGB", "RGBA"], {"default": "RGB"})
            }
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("Solid Color Image",)
    FUNCTION = "generate_solid_color"
    CATEGORY = "Images"

    def generate_solid_color(self, width, height, red, green, blue, alpha, mode):
        import torch

        # Erstelle das Bild basierend auf dem Modus
        if mode == "RGB":
            image = torch.full([1, height, width, 3], 0.0)
            image[..., 0] = red / 255.0  # Red
            image[..., 1] = green / 255.0  # Green
            image[..., 2] = blue / 255.0  # Blue
        else:  # RGBA
            image = torch.full([1, height, width, 4], 0.0)
            image[..., 0] = red / 255.0  # Red
            image[..., 1] = green / 255.0  # Green
            image[..., 2] = blue / 255.0  # Blue
            image[..., 3] = alpha / 255.0  # Alpha

        return (image,)


class NGs_Fill_with_Color:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "red": ("INT", {"default": 255, "min": 0, "max": 255, "step": 1, "display": "slider"}),
                "green": ("INT", {"default": 255, "min": 0, "max": 255, "step": 1, "display": "slider"}),
                "blue": ("INT", {"default": 255, "min": 0, "max": 255, "step": 1, "display": "slider"}),
                "alpha": ("INT", {"default": 255, "min": 0, "max": 255, "step": 1, "display": "slider"}),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("Filled Image",)
    FUNCTION = "fill_with_color"
    CATEGORY = "Images"

    def fill_with_color(self, image, red, green, blue, alpha):
        import torch

        # Lese Breite und Höhe des Bildes
        height, width = image.shape[1], image.shape[2]
        has_alpha = image.shape[-1] == 4  # Prüfe, ob das Bild einen Alphakanal hat

        # Erstelle ein neues Bild basierend auf den Bilddimensionen und dem Alphakanal
        if has_alpha:  # RGBA
            filled_image = torch.full([1, height, width, 4], 0.0)
            filled_image[..., 0] = red / 255.0  # Red
            filled_image[..., 1] = green / 255.0  # Green
            filled_image[..., 2] = blue / 255.0  # Blue
            filled_image[..., 3] = alpha / 255.0  # Alpha
        else:  # RGB
            filled_image = torch.full([1, height, width, 3], 0.0)
            filled_image[..., 0] = red / 255.0  # Red
            filled_image[..., 1] = green / 255.0  # Green
            filled_image[..., 2] = blue / 255.0  # Blue

        return (filled_image,)


class NGs_Checkerboard_Generator:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "width": ("INT", {"default": 512, "min": 1, "max": MAX_RESOLUTION}),
                "height": ("INT", {"default": 512, "min": 1, "max": MAX_RESOLUTION}),
                "tiles": ("INT", {"default": 32, "min": 2, "max": 512, "display": "slider"}),
                "color1": ("STRING", {"default": "#000000FF"}),
                "color2": ("STRING", {"default": "#FFFFFFFF"}),
                "mode": (["RGB", "RGBA"], {"default": "RGB"}),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("images",)
    FUNCTION = "generate_chessboard"
    CATEGORY = "Images"

    def generate_chessboard(self, width, height, tiles, color1, color2, mode):
        # Parse Farben
        color1 = self.parse_hex_color(color1)
        color2 = self.parse_hex_color(color2)

        # Limit Tiles auf die Breite des Bildes
        if tiles > width:
            tiles = width

        # Berechnung der Kästchengröße
        tile_width = width / tiles
        tile_height = tile_width

        # Erzeuge ein 2x2-Musterbild mit Pillow
        pattern_size = int(tile_width)
        pattern = Image.new("RGBA" if mode == "RGBA" else "RGB", (pattern_size * 2, pattern_size * 2))
        colors = [color1, color2]
        for y in range(2):
            for x in range(2):
                color = colors[(x + y) % 2]
                sub_tile = Image.new("RGBA" if mode == "RGBA" else "RGB", (pattern_size, pattern_size), color)
                pattern.paste(sub_tile, (x * pattern_size, y * pattern_size))

        # Skaliere das Musterbild auf die Zielgröße
        large_pattern = Image.new("RGBA" if mode == "RGBA" else "RGB", (width, height))
        for y in range(0, height, pattern_size * 2):
            for x in range(0, width, pattern_size * 2):
                large_pattern.paste(pattern, (x, y))

        # Konvertiere das Bild mit den vorhandenen Funktionen in einen Torch-Tensor
        return (pil2tensor(large_pattern),)

    @staticmethod
    def parse_hex_color(hex_color):
        """Konvertiert einen Hexadezimal-Farbwert in eine PIL-Farbe."""
        hex_color = hex_color.lstrip("#")
        if len(hex_color) == 6:  # Wenn kein Alpha-Wert angegeben ist
            hex_color += "FF"
        if len(hex_color) != 8:
            raise ValueError("Ungültiger Hexadezimal-Farbwert. Muss 6 oder 8 Zeichen lang sein.")
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        a = int(hex_color[6:8], 16)
        return (r, g, b, a)


class NGs_Image_Progress_Bar:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "width": ("INT", {"default": 512, "min": 64, "max": 4096}),
                "radius": ("INT", {"default": 8, "min": 4, "max": 64}),
                "inner_radius": ("INT", {"default": 6, "min": 2, "max": 62}),
                "line_width": ("INT", {"default": 8, "min": 4, "max": 64}),
                "line_inner_width": ("INT", {"default": 6, "min": 2, "max": 62}),
                "color_bar": ("STRING", {"default": "#000000FF"}),
                "color_inner_bar": ("STRING", {"default": "#00FF00FF"}),
                "max": ("INT", {"default": 7, "min": 2, "max": 256}),
                "value": ("INT", {"default": 3, "min": 0, "max": 256}),
                "smoothing": ("INT", {"default": 1, "min": 1, "max": 8, "display": "slider"}),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("images",)
    FUNCTION = "generate_progress_bar"
    CATEGORY = "NeoGriever/Images"

    def generate_progress_bar(self, width, radius, inner_radius, line_width, line_inner_width, color_bar,
                              color_inner_bar, max, value, smoothing):
        # Validierung von Werten
        if inner_radius > radius - 2:
            inner_radius = radius - 2
        if line_inner_width > line_width - 2:
            line_inner_width = line_width - 2
        if value > max:
            value = max

        # Skalieren aller Maße basierend auf dem Smoothing-Wert
        scaled_width = int(width * smoothing)
        scaled_radius = int(radius * smoothing)
        scaled_inner_radius = int(inner_radius * smoothing)
        scaled_line_width = int(line_width * smoothing)
        scaled_line_inner_width = int(line_inner_width * smoothing)
        scaled_margin = int(16 * smoothing)
        scaled_height = int((32 + 2 * radius) * smoothing)

        # Parse Farben
        color_bar = self.parse_hex_color(color_bar)
        color_inner_bar = self.parse_hex_color(color_inner_bar)

        # Interne Bildgröße initialisieren
        image = Image.new("RGBA", (scaled_width, scaled_height), (0, 0, 0, 0))  # Transparenter Hintergrund
        draw = ImageDraw.Draw(image)

        # Berechnung des verfügbaren Platzes (inkl. linker/rechter Rand)
        usable_width = scaled_width - 2 * scaled_margin
        step = usable_width / (max - 1) if max > 1 else usable_width
        y_center = scaled_height // 2

        # Zeichnen des äußeren Fortschrittsbalkens
        for i in range(max):
            x = int(scaled_margin + i * step)  # Skalierter Abstand zum linken Rand
            # Knotenpunkt
            draw.ellipse(
                [x - scaled_radius, y_center - scaled_radius, x + scaled_radius, y_center + scaled_radius],
                fill=color_bar,
            )
            # Linie
            if i < max - 1:
                x_next = int(scaled_margin + (i + 1) * step)
                draw.line(
                    [x + scaled_radius, y_center, x_next - scaled_radius, y_center],
                    fill=color_bar,
                    width=scaled_line_width,
                )

        # Zeichnen des inneren Fortschrittsbalkens
        for i in range(value):
            x = int(scaled_margin + i * step)
            # Knotenpunkt
            draw.ellipse(
                [x - scaled_inner_radius, y_center - scaled_inner_radius, x + scaled_inner_radius,
                 y_center + scaled_inner_radius],
                fill=color_inner_bar,
            )
            # Linie
            if i < value - 1:
                x_next = int(scaled_margin + (i + 1) * step)
                draw.line(
                    [x + scaled_inner_radius, y_center, x_next - scaled_inner_radius, y_center],
                    fill=color_inner_bar,
                    width=scaled_line_inner_width,
                )

        # Herunterskalieren auf die endgültige Größe mit bicubic Interpolation
        resized_image = image.resize((width, int((32 + 2 * radius))), Image.BICUBIC)

        # Konvertiere das Bild in einen Torch-Tensor
        return (pil2tensor(resized_image),)

    @staticmethod
    def parse_hex_color(hex_color):
        """Konvertiert einen Hexadezimal-Farbwert in ein (R, G, B, A)-Tuple."""
        hex_color = hex_color.lstrip("#")
        if len(hex_color) == 6:  # Kein Alpha-Wert angegeben
            hex_color += "FF"
        if len(hex_color) != 8:
            raise ValueError("Ungültiger Hexadezimal-Farbwert. Muss 6 oder 8 Zeichen lang sein.")
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        a = int(hex_color[6:8], 16)
        return (r, g, b, a)


class NGs_Tag_Source:
    SOURCES = [
        "brass", "bronze", "copper", "crystal", "gold", "iron",
        "leather", "obsidian", "steel", "wood", "aluminum", "bamboo",
        "bone", "clay", "concrete", "diamond", "fabric", "feather", "glass",
        "granite", "ivory", "jade", "limestone", "marble", "mica", "parchment",
        "plaster", "quartz", "resin", "rope", "rubber", "sandstone", "silk", "slate",
        "velvet", "wax", "wool", "burlap", "ceramic", "charcoal", "gravel", "hemp",
        "rattan", "resin", "sinew", "straw", "tin", "titanium", "wicker", "carbon_fiber",
        "bark", "blossom", "desert", "flower", "forest", "grass", "moss",
        "rock", "tree", "valley", "beach", "breeze", "canyon", "cliff",
        "coral", "dune", "fern", "fungus", "glacier", "grove", "hill", "island",
        "jungle", "lagoon", "lake", "meadow", "mountain", "ocean", "pine",
        "rainforest", "reef", "river", "savanna", "spring", "stream", "swamp",
        "tide", "waterfall", "whirlpool", "wind", "boulder", "prairie", "rose",
        "tulip", "daisy", "orchid", "lily", "sunflower", "marigold", "lavender",
        "cherry_blossom", "maple", "oak", "willow", "birch", "redwood", "cedar",
        "elm", "sycamore", "spruce", "palm", "cypress", "juniper", "holly", "yew",
        "hazel", "honeysuckle", "boxwood", "azalea", "rhododendron", "hawthorn",
        "elderberry", "forsythia", "lavender_bush",
        "adamantine", "aluminum", "bismuth", "brass", "bronze", "cobalt", "copper",
        "chromium", "electrum", "gold", "hematite", "iron", "lead", "mithril", "nickel",
        "obsidian_steel", "palladium", "platinum", "pyrite", "silver", "steel", "tin",
        "titanium", "tungsten", "zinc", "bauxite", "chromium_steel", "damascus_steel",
        "quicksilver", "stainless_steel", "tarnished_brass", "tarnished_silver",
        "iridescent_metal", "rainbow_titanium", "electrum_gold", "vibranium", "star_metal",
        "beveled", "blurred", "chiseled", "clear", "cracked", "crooked", "deformed",
        "distorted", "etched", "faceted", "frosted", "glossy", "grainy", "hazy",
        "lens", "matte", "mirror", "murky", "opaque", "pixelated", "polished",
        "prismatic", "reflective", "rippled", "rough", "scratched", "shattered",
        "shiny", "smooth", "spiky", "streaked", "tarnished", "translucent", "transparent",
        "warped", "wavy",
        "angular", "asymmetrical", "baroque", "blocky", "braided", "chiseled", "clean",
        "chunky", "curved", "decorative", "delicate", "detailed", "elegant", "engraved",
        "filigree", "flowing", "geometric", "gothic", "industrial", "intricate", "knotted",
        "lattice", "layered", "minimalistic", "modern", "modular", "natural", "ornate",
        "polished", "refined", "retro", "rough", "rustic", "sleek", "smooth", "spiky",
        "spiraled", "stained", "symmetrical", "tangled", "textured", "twisted", "vintage",
        "woven",
        "arcane", "aural", "bioelectric", "blaze", "charge", "cosmic", "current",
        "dark_energy", "electrical", "electromagnetic", "ether", "etheric", "flame",
        "flux", "force", "frequency", "glow", "heat", "infernal", "infrared", "kinetic",
        "light", "lightning", "magical", "magnetic", "momentum", "nuclear", "plasma",
        "pulse", "pyro", "radioactive", "radiant", "resonance", "shockwave", "solar",
        "spark", "static", "steam", "storm", "thermal", "tidal", "vibration", "voltage",
        "warp", "wave", "wind", "quantum_energy", "zero_point",
        "anointed", "aura", "beatific", "blessed", "celestial", "consecrated", "divine",
        "ethereal", "glorious", "hallowed", "halo", "holy", "illuminated", "immortal",
        "incandescent", "ineffable", "luminous", "miraculous", "numinous", "otherworldly",
        "radiant", "reverent", "sacred", "sanctified", "seraphic", "shimmering",
        "spiritual", "sublime", "transcendent", "twilight", "untouchable", "venerated",
        "abyssal", "accursed", "baneful", "blighted", "chaotic", "corrupt", "cursed",
        "damned", "dark", "demonic", "depraved", "desolate", "devilish", "diabolic",
        "doomed", "dreadful", "fallen", "fiendish", "forsaken", "grim", "hellish",
        "horrid", "infernal", "malevolent", "malignant", "ominous", "perverse", "profane",
        "shadowy", "sinister", "spiteful", "tainted", "tormented", "twisted", "unclean",
        "unholy", "vile", "wicked", "wrathful",
        "alchemy", "amulet", "artifact", "basilisk", "bastion", "behemoth", "chimera",
        "citadel", "crystal_ball", "cursed_blade", "dragon", "druid", "eldritch",
        "elemental", "enchantment", "fae", "faerie", "gargoyle", "giant", "goblin",
        "golem", "griffin", "gryphon", "horde", "hydra", "incantation", "knight",
        "kraken", "leviathan", "lore", "mage", "magic", "manticore", "necromancer",
        "obelisk", "ogre", "paladin", "phantasm", "phoenix", "portal", "rune",
        "sanctuary", "scepter", "sentinel", "sorcerer", "spell", "spellbook",
        "talisman", "totem", "tower", "unicorn", "vortex", "warlock", "wizard",
        "wyvern",
        "bristly", "bushy", "coarse", "curly", "dense", "downy", "feathery",
        "fine", "fluffy", "frizzy", "fuzzy", "glossy", "greasy", "long-haired",
        "luxurious", "matted", "oily", "patchy", "plush", "ragged", "rough",
        "ruffled", "satin", "scraggly", "shaggy", "short-haired", "silky", "sleek",
        "smooth", "soft", "spiky", "stringy", "sparse", "stiff", "tangled", "tufted",
        "velvety", "voluminous", "wavy", "whispy", "wild", "wiry", "woolly", "ziz-zagged"
    ]

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "seed": ("INT",),
                "insanity": ("INT", {"default": 0, "min": 0, "max": 100, "step": 1, "display": "slider"}),
                "dupes": ("BOOLEAN", {"default": False, "label_off": "Deny Dupes", "label_on": "Allow Dupes"}),
            }
        }

    RETURN_TYPES = ("STRING", "STRING",)
    RETURN_NAMES = ("Tags", "TagsList")
    OUTPUT_IS_LIST = (False, True,)
    FUNCTION = "generate_tag_source"
    CATEGORY = "NeoGriever/Tags"

    def generate_tag_source(self, seed, insanity, dupes):
        random.seed(seed)
        insanity_factor = 1 + (insanity / 100) * 1.5
        tags = []
        for i in range(int(10 * insanity_factor)):
            while True:
                tag = random.choice(self.SOURCES)
                if dupes or tag not in tags:
                    break
            tags.append(tag)
        tags_string = ", ".join(tags)
        return (tags_string, tags)
