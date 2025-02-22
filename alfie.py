import os
import random
from datetime import datetime
from wand.image import Image
from atproto import Client, models

max_size = 1000000 # 1 million bytes

def resize_image(random_image):
    with Image(filename=random_image) as img:
        image_size = os.path.getsize(random_image)
        if image_size > max_size:
            img.compression_quality = 80
            img.save(filename=random_image)

def post_image(client, img_data, alt_text, aspect_ratio):
    client.send_image(
        text="",
        image=img_data,
        image_alt=alt_text,
        image_aspect_ratio=aspect_ratio
    )

def main():
    client = Client()
    client.login(os.environ['BSKY_HANDLE'], os.environ['BSKY_APP_PASSWORD'])

    folder_path = 'alfie'
    image_files = os.listdir(folder_path)
    random_image = random.choice(image_files)
    random_image = os.path.join(folder_path, random_image)

    # if file name starts with 'excluded_', 'posted_' or ends with '.mp4', try again
    while random_image.startswith('alfie/excluded_') or random_image.startswith('alfie/posted_') or random_image.endswith('.mp4'):
        random_image = random.choice(image_files)
        random_image = os.path.join(folder_path, random_image)

    print('selected', random_image)

    # check image size
    if os.path.getsize(random_image) > max_size:
        resize_image(random_image)

    with open(random_image, 'rb') as f:
        img_data = f.read()

        with Image(filename=random_image) as img:
            w = img.width
            h = img.height
    
        aspect_ratio = models.AppBskyEmbedDefs.AspectRatio(height=h, width=w)

        twitter_status_number = random_image.split('/')[-1].split('_')[0]
        alt_text = f'photo of a cat, from x.com/goodboyalfie/status/{twitter_status_number}'

        post_image(client, img_data, alt_text, aspect_ratio)

    print('posted', random_image)

if __name__ == '__main__':
    main()
