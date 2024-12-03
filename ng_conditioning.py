import re
import node_helpers


class NGs_BetterCLIPTextEncode:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "clip": ("CLIP", {}),
                "text": ("STRING", {"multiline": True, "dynamicPrompts": True}),
                "betterGen": ("BOOLEAN", {"default": True, "label_off": "No", "label_on": "Yes"})
            }
        }

    RETURN_TYPES = ("CONDITIONING",)
    OUTPUT_TOOLTIPS = ("NeoGriever's Better CLIP Text Encoder",)
    FUNCTION = "encode"

    CATEGORY = "NeoGriever/Conditioning"
    DESCRIPTION = """Guide:
                If betterGen is active:
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
                
                Default is [0.0,1.0], wich means full generation. 
                """

    def encode(self, clip, text, betterGen):
        if not betterGen:
            tokens = clip.tokenize(text)
            output = clip.encode_from_tokens(tokens, return_pooled=True, return_dict=True)
            cond = output.pop("cond")
            return ([[cond, output]],)
        else:
            result = None
            for line in text.splitlines():
                start = 0.0
                end = 1.0
                prompt = line.strip()

                match = re.match(r'^\[\s*([0-9]*\.?[0-9]*)\s*(?:,\s*([0-9]*\.?[0-9]*))?\s*\](.*)', line)

                if match:
                    start = float(match.group(1)) if match.group(1) else 0.0
                    end = float(match.group(2)) if match.group(2) else 1.0
                    prompt = match.group(3).strip()

                tokens = clip.tokenize(prompt)
                output = clip.encode_from_tokens(tokens, return_pooled=True, return_dict=True)
                cond = output.pop("cond")

                cond = node_helpers.conditioning_set_values(cond, {"start_percent": start, "end_percent": end})

                if result is None:
                    result = [[cond, output]]
                    continue
                result = result + [[cond, output]]

        return (result,)
