from PIL import Image
from src.core.image_generator import ImageGenerator

def test_image_generator_can_generate_image():
    image_generator = ImageGenerator()
    image = image_generator.generate_image(name="Hucci", fate="大吉")
    assert isinstance(image, Image.Image)