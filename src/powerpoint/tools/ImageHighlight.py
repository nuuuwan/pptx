from PIL import Image, ImageDraw
from utils import Log

log = Log('ImageHighlight')


class ImageHighlight:
    def __init__(
        self, original_image_path: str, guide_image_path: str, dim: int
    ):
        self.original_image_path = original_image_path
        self.guide_image_path = guide_image_path
        self.dim = dim

    @staticmethod
    def get_fp(image_path: str, dim: int):
        im = Image.open(image_path)
        fp = []
        for i in range(0, im.size[0], dim):
            fp_i = []
            for j in range(0, im.size[1], dim):
                total_brightness = 0
                for di in range(dim):
                    for dj in range(dim):
                        pixel = im.getpixel((i + di, j + dj))
                        brightness = sum(pixel) / 3
                        total_brightness += brightness
                fp_ij = total_brightness / (dim * dim)
                fp_i.append(fp_ij)
            fp.append(fp_i)
        return fp

    def write(self, output_image_path: str):
        fp_original = self.get_fp(self.original_image_path, self.dim)
        fp_guide = self.get_fp(self.guide_image_path, self.dim)

        im = Image.open(self.original_image_path).convert("RGBA")
        overlay = Image.new("RGBA", im.size, (255, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)
        for i in range(0, im.size[0], self.dim):
            for j in range(0, im.size[1], self.dim):
                ki = i // self.dim
                kj = j // self.dim
                fp_ij_original = fp_original[ki][kj]
                fp_ij_guide = fp_guide[ki][kj]

                if abs(fp_ij_original - fp_ij_guide) < 0.1:
                    continue

                top_left = (ki * self.dim, kj * self.dim)
                bottom_right = ((ki + 1) * self.dim, (kj + 1) * self.dim)
                draw.rectangle(
                    [top_left, bottom_right],
                    outline=None,
                    fill=(20, 20, 20, 20),
                    width=2,
                )
        combined = Image.alpha_composite(im, overlay)
        combined.save(output_image_path)
        log.info(f'Wrote {output_image_path}')
