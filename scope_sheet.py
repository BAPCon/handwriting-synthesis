import random
from PIL import Image
from cairosvg import svg2png
import io

from handwriting_synthesis.hand import Hand

hand = None

def handwrite(text: str):
    svg = _write_text(text)
    png = svg2png(bytestring=svg)
    img = Image.open(io.BytesIO(png))
    img = img.crop(img.getbbox())
    return img

def _write_text(text):
    global hand
    if hand is None:
        hand = Hand()
    lines = text.split("\n")
    biases = [.99 for i in lines]
    styles = [5 for i in lines]
    colors = ['red' for i in lines]
    return hand.write(
        lines=lines,
        biases=biases,
        styles=styles,
        stroke_colors=colors
    )

class ExteriorScopeSheet:
    def __init__(self, path: str = 'Exterior_Scope_Sheet.png', circles_path: str = 'Exterior_Scope_sheet_circles.png') -> None:
        self.scope_sheet = Image.open(path)
        self.circles = Image.open(circles_path)
        self.VALUES = {}
        self.LABELS = []
        _LABELS = open('labels_ext_ss_.txt','r').read().split("\n")
        _LABELS = [label.strip() for label in _LABELS]
        for x in range(self.scope_sheet.size[0]):
            for y in range(self.scope_sheet.size[1]):
                px = self.scope_sheet.getpixel((x, y))
                if px[0] > 200 and px[1] < 50 and px[2] < 50:
                    self.VALUES[_LABELS[len(self.VALUES)-1]] = {
                            'x': x,
                            'y': y,
                            'w': 308,
                            'h': 34,
                            'value': None
                        }
                    
    def set_value(self, label: str, value: str):
        if label in self.VALUES:
            self.VALUES[label]['value'] = value
        else:
            print(f"Label '{label}' not found.")
                    
    def finalize(self):
        for label in self.VALUES:
            x, y, w, h = self.VALUES[label]['x'], self.VALUES[label]['y'], self.VALUES[label]['w'], self.VALUES[label]['h']
            if self.VALUES[label]['value'] is not None:
                _circle = self.circles.crop((33, y, 308, y+34))
                self.scope_sheet.alpha_composite(_circle, (33, y))
                img = handwrite(self.VALUES[label]['value'])
                _x, _y = x, y
                _x += random.randint(0, 5)
                _y += random.randint(0, 5)
                if img.size[0] > w:
                    img = img.resize((w, int(img.size[1] * (w / img.size[0]))))
                if img.size[1] > h:
                    img = img.resize((int(img.size[0] * (h / img.size[1])), h))
                self.scope_sheet.alpha_composite(img, (_x, _y))
            else:
                img = handwrite("NA")
                _x, _y = x, y
                _x += random.randint(0, 5)
                _y += random.randint(0, 5)
                if img.size[0] > w:
                    img = img.resize((w, int(img.size[1] * (w / img.size[0]))))
                if img.size[1] > h:
                    img = img.resize((int(img.size[0] * (h / img.size[1])), h))
                self.scope_sheet.alpha_composite(img, (_x, _y))

