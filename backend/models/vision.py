import base64
from vertexai.preview.vision_models import ImageGenerationModel
from vertexai.vision_models import Image

from logger.logging import Logger

# Create logger object
logger = Logger(__name__)


class ImageModel:
    """Image Model Class"""

    def __init__(
        self,
        model: str,
    ) -> None:
        # Image models
        self.imagen = ImageGenerationModel.from_pretrained(model)

    def generate_image(
        self, prompt: str, number_of_images: int, negative_prompt: str = None
    ):
        """Image generation with Imagen
        Parameters:
            prompt: str
            number_of_images: int = 1
        Returns:
            List of images with:
                id: image id
                images_base64_string (str): Image as base64 string
                image_size (int, int): Size of the image
                images_parameters (dict): Parameters used with the model
        """
        try:
            imagen_responses = self.imagen.generate_images(
                prompt=prompt,
                number_of_images=number_of_images,
                negative_prompt=negative_prompt,
            )
        except Exception as e:
            logger.error(f"Exception Occurred: {str(e)}.")

        else:
            generated_images = []
            i = 0
            for image in imagen_responses:
                generated_images.append(
                    {
                        "id": i,
                        "images_base64_string": image._as_base64_string(),
                        "image_size": image._size,
                        "images_parameters": image.generation_parameters,
                    }
                )
                i = i + 1

        return generated_images

    def edit_image(
        self,
        prompt: str,
        base_image_base64: str,
        mask_base64: str = None,
        number_of_images: int = 1,
        negative_prompt: str = None,
    ):
        """Image editing with Imagen
        Parameters:
            prompt: str
            base_image_base64: str
            mask_base64: str | None = None
            number_of_images: int = 1
            negative_prompt: str = None
        Returns:
            List of images with:
                id: imageid
                images_base64_string (str): Image as base64 string
                image_size (int, int): Size of the image
                images_parameters (dict): Parameters used with the model
        """
        if not mask_base64:
            mask = None
        else:
            mask = Image(image_bytes=base64.b64decode(mask_base64))

        try:
            imagen_responses = self.imagen.edit_image(
                prompt=prompt,
                base_image=Image(image_bytes=base64.b64decode(base_image_base64)),
                mask=mask,
                number_of_images=number_of_images,
                negative_prompt=negative_prompt,
            )
        except Exception as e:
            logger.error(f"Exception Occurred: {str(e)}.")
        else:
            generated_images = []
            i = 0
            for image in imagen_responses:
                generated_images.append(
                    {
                        "id": i,
                        "images_base64_string": image._as_base64_string(),
                        "image_size": image._size,
                        "images_parameters": image.generation_parameters,
                    }
                )
                i = i + 1

        return generated_images
