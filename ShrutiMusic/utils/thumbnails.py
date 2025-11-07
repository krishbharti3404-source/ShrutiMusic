import asyncio
import aiohttp
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont, ImageFilter

# Font paths
FONT_REGULAR_PATH = "ShrutiMusic/assets/font2.ttf"
FONT_BOLD_PATH = "ShrutiMusic/assets/font3.ttf"

async def generate_thumbnail(thumbnail_url: str, title: str, singer: str, music: str, views: str = "70,000,000+", duration: str = "3:19"):
    """
    Generate a 'Samay Samjhayega'-style thumbnail with blurred background,
    rounded card, title, and credits.
    """

    async with aiohttp.ClientSession() as session:
        async with session.get(thumbnail_url) as response:
            image_data = await response.read()

    base = Image.open(BytesIO(image_data)).convert("RGB")
    base = base.resize((1280, 720))
    blur_bg = base.filter(ImageFilter.GaussianBlur(20))

    # Overlay gradient
    overlay = Image.new("RGBA", blur_bg.size, (0, 0, 0, 120))
    blur_bg = Image.alpha_composite(blur_bg.convert("RGBA"), overlay)

    # Center card
    draw = ImageDraw.Draw(blur_bg)
    card_x1, card_y1 = 200, 150
    card_x2, card_y2 = 1080, 570
    card_color = (255, 255, 255, 25)

    # Rounded rectangle (card)
    radius = 40
    card = Image.new("RGBA", (card_x2 - card_x1, card_y2 - card_y1), (255, 255, 255, 20))
    mask = Image.new("L", card.size, 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.rounded_rectangle([(0, 0), card.size], radius=radius, fill=255)
    blur_bg.paste(card, (card_x1, card_y1), mask)

    # Text setup
    font_bold = ImageFont.truetype(FONT_BOLD_PATH, 80)
    font_regular = ImageFont.truetype(FONT_REGULAR_PATH, 45)
    font_small = ImageFont.truetype(FONT_REGULAR_PATH, 35)

    # Draw text
    draw.text((230, 170), f"{views} VIEWS", font=font_small, fill=(255, 255, 255, 230))
    draw.text((250, 300), title.upper(), font=font_bold, fill=(255, 255, 255, 255))
    draw.text((250, 400), f"Singer: {singer}", font=font_regular, fill=(220, 220, 220, 255))
    draw.text((250, 460), f"Music: {music}", font=font_regular, fill=(220, 220, 220, 255))
    draw.text((1000, 520), duration, font=font_small, fill=(255, 255, 255, 255))

    # Save
    final = blur_bg.convert("RGB")
    final.save("thumb_result.jpg", "JPEG")
    print("✅ Thumbnail generated: thumb_result.jpg")

# Example usage (for local test)
# asyncio.run(generate_thumbnail(
#     "https://i.ytimg.com/vi/abcd1234/hqdefault.jpg",
#     title="Samay Samjhayega",
#     singer="Raghav Chaitanya",
#     music="Amit Trivedi"
# ))
