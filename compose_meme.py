"""Draw the Post-the-Meme entry image with Pillow, from scratch.

Concept (locked): a bold text meme for AI-agent builders.
  Top:    I DON'T WORK / ANYMORE.
  Middle: a white ghost in sunglasses with a gold chain, holding a star.
  Bottom: MY AGENT DOES. / make.fun PAYS IT.

Everything is drawn programmatically: no downloaded or copied image is
used. Run: python3 compose_meme.py  ->  meme.png (1024x1024) + meme-480.png
"""

import math
import os

from PIL import Image, ImageDraw, ImageFont

SIZE = 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "meme.png")
PREVIEW = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "meme-480.png"
)

NAVY_TOP = (11, 16, 38)
NAVY_BOTTOM = (42, 14, 63)
WHITE = (255, 255, 255)
GOLD = (255, 211, 77)
GOLD_DEEP = (230, 165, 30)
INK = (12, 12, 20)


def load_bold(size: int) -> ImageFont.FreeTypeFont:
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for path in candidates:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def vertical_gradient(size: int) -> Image.Image:
    img = Image.new("RGB", (size, size), NAVY_TOP)
    top = ImageDraw.Draw(img)
    for y in range(size):
        t = y / max(1, size - 1)
        colour = tuple(
            round(NAVY_TOP[i] + (NAVY_BOTTOM[i] - NAVY_TOP[i]) * t)
            for i in range(3)
        )
        top.line([(0, y), (size, y)], fill=colour)
    return img


def centred_text(
    draw: ImageDraw.ImageDraw, cx: int, y: int, lines, font, fill
) -> int:
    """Draw centred lines starting at y; return the y just below the block."""
    for line in lines:
        box = draw.textbbox((0, 0), line, font=font)
        width = box[2] - box[0]
        draw.text((cx - width / 2, y), line, font=font, fill=fill)
        y += (box[3] - box[1]) + 8
    return y


def four_point_star(draw: ImageDraw.ImageDraw, cx: float, cy: float, r: float, fill):
    points = []
    for i in range(8):
        angle = math.pi / 2 + i * math.pi / 4
        rad = r if i % 2 == 0 else r * 0.28
        points.append((cx + rad * math.cos(angle), cy - rad * math.sin(angle)))
    draw.polygon(points, fill=fill)


def draw_ghost(draw: ImageDraw.ImageDraw):
    """White ghost with sunglasses, gold chain, holding a glowing star."""
    # Body: rounded-top rectangle with a wavy hem.
    left, top, right = 332, 400, 692
    hem_y = 740
    draw.rounded_rectangle([left, top, right, hem_y], radius=110, fill=WHITE)
    # Wavy hem: three white bumps below the rectangle's bottom edge.
    for bump_x in (377, 467, 557, 647):
        draw.ellipse(
            [bump_x - 45, hem_y - 30, bump_x + 45, hem_y + 45], fill=WHITE
        )
    # Eyes (behind the sunglasses, barely visible as dark ovals).
    for eye_x in (452, 572):
        draw.ellipse([eye_x - 26, 500 - 24, eye_x + 26, 500 + 24], fill=INK)
    # Sunglasses: two black lenses joined by a bridge, over the eyes.
    for lens_x in (452, 572):
        draw.rounded_rectangle(
            [lens_x - 52, 478, lens_x + 52, 540], radius=22, fill=INK
        )
    draw.rectangle([500, 502, 524, 514], fill=INK)
    # Gold chain: an arc of small circles across the chest.
    for step in range(13):
        t = step / 12
        chain_x = 380 + t * 264
        chain_y = 640 + 42 * math.sin(t * math.pi)
        draw.ellipse(
            [chain_x - 9, chain_y - 9, chain_x + 9, chain_y + 9], fill=GOLD
        )
    draw.ellipse([497, 668, 527, 698], fill=GOLD_DEEP)
    # Glowing star held up at the ghost's right side (soft halo first).
    glow_cx, glow_cy = 730, 470
    for glow_r, glow_alpha in ((150, 38), (110, 70)):
        draw.ellipse(
            [glow_cx - glow_r, glow_cy - glow_r, glow_cx + glow_r, glow_cy + glow_r],
            fill=(255, 211, 77, glow_alpha),
        )
    four_point_star(draw, glow_cx, glow_cy, 78, GOLD)


def main() -> None:
    img = vertical_gradient(SIZE)
    draw = ImageDraw.Draw(img, "RGBA")

    big = load_bold(96)
    mid = load_bold(78)
    centred_text(draw, SIZE // 2, 92, ["I DON'T WORK", "ANYMORE."], big, WHITE)
    draw_ghost(draw)
    centred_text(
        draw, SIZE // 2, 812, ["MY AGENT DOES.", "make.fun PAYS IT."], mid, GOLD
    )

    img.save(OUT, "PNG")
    img.resize((480, 480), Image.LANCZOS).save(PREVIEW, "PNG")
    print(f"wrote {OUT} ({os.path.getsize(OUT)} bytes)")
    print(f"wrote {PREVIEW} ({os.path.getsize(PREVIEW)} bytes)")


if __name__ == "__main__":
    main()
