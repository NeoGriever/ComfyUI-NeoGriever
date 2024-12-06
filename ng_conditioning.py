import re
from nodes import CLIPTextEncode, ConditioningSetTimestepRange, ConditioningConcat


class NGs_Better_CLIP_Text_Encode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "clip": ("CLIP", {}),
                "text": ("STRING", {"multiline": True}),
                "usebetter": (
                "BOOLEAN", {"default": False, "label_on": "Better Text Encode", "label_off": "Text Encode"})
            }
        }

    RETURN_TYPES = ("CONDITIONING",)
    FUNCTION = "encode"
    CATEGORY = "NeoGriever/Conditioning"
    DESCRIPTION = """Guide:
                If usebetter is active:
                Each line represents a new concatenated prompt.
                You can put percentages on it with [0.0,1.0] like:
                - "[0.5,1.0]A photo of a cat and a dog."
                - this will only put the prompt at 50% to 100% of generation

                - "[0.5,0.75]A photo of a cat and a dog."
                - this will put the prompt at 50% to 75% of generation

                - "[,0.8]A photo of a cat and a dog."
                - this will put the prompt at 0% to 80% of generation

                - "[0.5]A photo of a cat and a dog."
                - this will put the prompt from 50% to 100% of generation

                Default is [0.0,1.0], which means full generation.
                """

    def encode(self, clip, text, usebetter):
        # Standard Instanzen der vorhandenen Klassen
        _clip_text_encode = CLIPTextEncode()
        _conditioning_set_timestep_range = ConditioningSetTimestepRange()
        _conditioning_concat = ConditioningConcat()

        if not usebetter:
            # Standard CLIP Text Encode
            return _clip_text_encode.encode(clip, text)

        # Zeilenweise Verarbeitung
        lines = text.splitlines() if "\n" in text else [text]
        lines = [line.strip() for line in lines if line.strip()]  # Entferne leere Zeilen
        if not lines:
            lines = [""]  # Füge eine leere Zeile hinzu, falls alle Zeilen leer sind

        temp_result = None
        for line in lines:
            # Standardmäßige Timing-Werte
            start, end = 0.0, 1.0

            # Timing-Vorgaben überprüfen
            timing_match = re.match(r'^\[\s*([0-9.]*\.?[0-9]*)\s*(?:,\s*([0-9.]*\.?[0-9]*))?\s*\](.*)', line)
            if timing_match:
                start = float(timing_match.group(1)) if timing_match.group(1) else 0.0
                end = float(timing_match.group(2)) if timing_match.group(2) else 1.0
                line = timing_match.group(3).strip()  # Entferne Timing-Angabe aus der Zeile

            # Text Encode für die Zeile
            result = _clip_text_encode.encode(clip, line)[0]

            # Setze Timing-Bereich
            result = _conditioning_set_timestep_range.set_range(result, start, end)[0]

            # Kombiniere Ergebnisse
            if temp_result is None:
                temp_result = result
            else:
                temp_result = _conditioning_concat.concat(temp_result, result)[0]

        return (temp_result,)
