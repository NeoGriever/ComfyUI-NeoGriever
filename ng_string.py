class NGs_String_Operator:
    MODES = ["Condense", "Trim", "Padding(<)", "Padding(-)", "Padding(>)", "Lower", "Upper"]

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "string": ("STRING", {"default": ""}),
                "mode": (cls.MODES, {"default": "Condense"})
            }
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "operate"
    CATEGORY = "NeoGriever/Text"

    def operate(self, string, mode):
        if mode == "Condense":
            # Entfernt doppelte Einträge und sortiert sie
            unique_words = {word.strip() for word in string.split(",") if word.strip()}
            return (", ".join(sorted(unique_words)),)
        elif mode == "Trim":
            # Entfernt Leerzeichen an den Rändern
            return (string.strip(),)
        elif mode == "Padding(<)":
            return (self.pad_string(string, "<"),)
        elif mode == "Padding(-)":
            return (self.pad_string(string, "-"),)
        elif mode == "Padding(>)":
            return (self.pad_string(string, ">"),)
        elif mode == "Lower":
            # Alles in Kleinbuchstaben
            return (string.lower(),)
        elif mode == "Upper":
            # Alles in Großbuchstaben
            return (string.upper(),)

    def pad_string(self, string, direction):
        length = len(string)
        target_length = (length + 15) // 16 * 16
        padding_size = target_length - length

        if direction == "<":
            # Füge Leerzeichen rechts hinzu
            return string + " " * padding_size
        elif direction == "-":
            # Zentriere den Text
            left_padding = padding_size // 2
            right_padding = padding_size - left_padding
            return " " * left_padding + string + " " * right_padding
        elif direction == ">":
            # Füge Leerzeichen links hinzu
            return " " * padding_size + string


class NGs_String_Squisher:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {"forceInput": True}),
                "maxlength": ("INT", {"default": 20, "min": 2, "max": 256, "step": 1, "display": "slider"}),
                "linebreak": (["custom", "LF", "TAB"], {"default": "LF"}),
            },
            "optional": {
                "custom_break": ("STRING", {"default": ";", "multiline": False}),
            }
        }

    RETURN_TYPES = ("STRING", "STRING",)
    RETURN_NAMES = ("formatted_text", "lines")
    OUTPUT_IS_LIST = (False, True,)
    FUNCTION = "squish"
    CATEGORY = "NeoGriever/Text"

    def squish(self, text, maxlength, linebreak, custom_break):
        # Bestimme das Trennzeichen
        if linebreak == "LF":
            break_char = "\n"
        elif linebreak == "TAB":
            break_char = "\t"
        elif linebreak == "custom":
            break_char = custom_break
        else:
            break_char = "\n"

        words = text.split()  # Splitte den Text anhand von Leerzeichen
        current_line = []
        lines = []
        current_length = 0

        for word in words:
            word_length = len(word)
            if current_length + word_length + (1 if current_line else 0) <= maxlength:
                # Füge das Wort zur aktuellen Zeile hinzu
                current_line.append(word)
                current_length += word_length + (1 if current_line else 0)
            else:
                # Schreibe die aktuelle Zeile ab und starte eine neue
                lines.append(" ".join(current_line))
                current_line = [word]
                current_length = word_length

        # Füge die letzte Zeile hinzu
        if current_line:
            lines.append(" ".join(current_line))

        # Formatiere den Text als String
        formatted_text = break_char.join(lines)
        return (formatted_text, lines,)


class NGs_Text_Cut_String:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {"multiline": True}),
                "maxlength": ("INT", {"default": 42, "min": 1, "max": 1024, "display": "slider"}),
                "cut_characters": ("STRING", {"default": ",.-", "multiline": False}),
                "trim": ("BOOLEAN", {"default": False, "label_on": "true", "label_off": "false"}),
                "clean": ("BOOLEAN", {"default": True, "label_on": "true", "label_off": "false"}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("Result",)
    FUNCTION = "cut_string"
    CATEGORY = "NeoGriever/Text"

    def cut_string(self, text, maxlength, cut_characters, trim, clean):
        # Falls trim aktiviert ist, entferne Leerzeichen vom Anfang und Ende des Textes
        if trim:
            text = text.strip()

        # Falls clean aktiviert ist, ersetze überflüssige Leerzeichen
        if clean:
            text = " ".join(text.split())

        # Wenn der Text kürzer ist als die maximale Länge, gibt ihn direkt zurück
        if len(text) <= maxlength:
            return (text,)

        # Initialisiere die Position für den Cut
        cut_position = maxlength

        # Finde den letzten sicheren Cut-Punkt, bevorzugt nach einem `cut_character`
        for i in range(maxlength - 1, -1, -1):
            if text[i] in cut_characters:
                # Wenn das Zeichen ein `cut_character` ist, schneide direkt danach ab
                cut_position = i + 1
                break
            elif text[i].isspace():
                # Wenn kein `cut_character` gefunden wird, schneide vor einem Leerzeichen ab
                cut_position = i
                break

        # Schneide den Text ab
        result = text[:cut_position]

        # Falls clean aktiviert ist, entferne abschließende Leerzeichen
        if clean:
            result = result.rstrip()

        return (result,)
