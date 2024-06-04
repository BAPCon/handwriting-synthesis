import numpy as np
from handwriting_synthesis import Hand

hand = None

def write_text(text):
    global hand
    if hand is None:
        hand = Hand()
    lines = text.split("\n")
    biases = [.75]
    styles = [7 for i in lines]

    hand.write(
        filename='img/give_up.svg',
        lines=lines,
        biases=biases,
        styles=styles,
    )

from PIL import Image

write_text("Give up")
