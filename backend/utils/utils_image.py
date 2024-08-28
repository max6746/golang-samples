# Image Helper Utilities

from PIL import Image
import base64
from io import BytesIO


class Mask:
    """Utility for handling Image Masking"""

    def generate_mask(
        self,
        height: int,
        width: int,
        mask_start_x: int,
        mask_end_x: int,
        mask_start_y: int,
        mask_end_y: int,
    ):
        """Generate Image Mask

        Args:
            height (int): hieght of mask
            width (int): widht of mask
            mask_start_x (int): x start coordinate
            mask_end_x (int): x end coordinate
            mask_start_y (int): y start coordinate
            mask_end_y (int): y end coordinate

        Returns:
            _type_: base64 masked image
        """
        img = Image.new(mode="RGB", size=(width, height))

        for i in range(mask_start_x, mask_end_x):
            for j in range(mask_start_y, mask_end_y):
                value = (255, 255, 255)
                img.putpixel((i, j), value)

        buffered = BytesIO()
        img.save(buffered, format="JPEG")
        img_str = base64.b64encode(buffered.getvalue())

        return str(img_str, encoding="utf-8")
