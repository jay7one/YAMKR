import os
from PIL import Image

class PNGConverter:
    @classmethod
    def convert_to_rgba(cls, directory, target_size):
        # Iterate through files in the directory
        for filename in os.listdir(directory):
            if filename.endswith(".png"):
                # Open the image
                img_path = os.path.join(directory, filename)
                img = Image.open(img_path)

                # Crop the image to a square with width lower of height or width
                width, height = img.size
                size = min(width, height)
                left = (width - size) // 2
                top = (height - size) // 2
                right = (width + size) // 2
                bottom = (height + size) // 2
                img = img.crop((left, top, right, bottom))

                # Convert to RGBA
                img = img.convert("RGBA")

                # Create a new image with white as transparency color
                datas = img.getdata()
                newData = []
                for item in datas:
                    # Set transparency for white pixels
                    if item[0] == 255 and item[1] == 255 and item[2] == 255:
                        newData.append((255, 255, 255, 0))
                    else:
                        newData.append(item)

                img.putdata(newData)

                # Resize the image to the target size with Lanczos anti-aliasing
                img = img.resize(target_size, resample=Image.Resampling.LANCZOS)

                # Save the modified image
                img.save(os.path.join(directory, f"{os.path.splitext(filename)[0]}_{target_size[0]}x{target_size[1]}_rgba.png"), "PNG")

# Test the class method
if __name__ == "__main__":
    directory_path = "images"
    PNGConverter.convert_to_rgba(directory_path, (12, 12))  # Convert images to 12x12
    PNGConverter.convert_to_rgba(directory_path, (16, 16))  # Convert images to 16x16
