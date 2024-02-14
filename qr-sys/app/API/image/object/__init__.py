from PIL import Image, ImageDraw
from typing import ByteString
from io import BytesIO
import base64


class image:

    def open_bytes_image(self, image: bytes) -> Image:
        return Image.open(BytesIO(image))

    def resize_image(self, image: ByteString, width: int, height: int):
        img = self.open_bytes_image(image)

        w, h = img.size

        ratio = min(width / w, height / h)


        resized_img = img.resize((int(w * ratio), int(h * ratio)), Image.Resampling.LANCZOS)

        return resized_img


    def make_round(self, image: ByteString) -> Image:
        img = self.open_bytes_image(image) 

        mask = Image.new("L", img.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, img.size[0], img.size[1]), fill=255)

        rounded_image = img.copy()
        rounded_image.putalpha(mask)

        return rounded_image
    
    def str_to_base64(self, image: str) -> bytes:
        return base64.b64decode(image)

    def base64_to_str(self, data: bytes) -> str:
        return base64.b64encode(data).decode()

    def image_to_base64(self, image: Image, format: str = "PNG"):
        img = BytesIO()

        image.save(img, format)

        return img.getvalue() 

    def make_rounded_image(self, color: tuple, size: int):
        img = Image.new("RGB", (size, size), color=color)
        mask = Image.new("L", (size, size), 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, size, size), fill=255)
        img.putalpha(mask)
        return img
    
    def get_center_coordinates(self, ovrl: Image, back: Image) -> tuple[int]:
        w, h = back.size
        left = (w - ovrl.width) // 2
        top = (h - ovrl.height) // 2
        right = left + ovrl.width
        bottom = top + ovrl.height

        return (left, top, right, bottom)