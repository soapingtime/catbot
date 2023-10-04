import os
import random
from datetime import datetime
from wand.image import Image
from atproto import Client

max_size = 900 * 1024  # 900 KB in bytes

# checks image size and resizes if it's over 900 KB (bluesky's max size)

def resize_image(random_image):
    with Image(filename=random_image) as img:
        image_size = os.path.getsize(random_image)
        if image_size > max_size:
            img.compression_quality = 70
            img.save(filename=random_image)

def main():
    client = Client()
    client.login(os.environ['BSKY_HANDLE'], os.environ['BSKY_APP_PASSWORD'])

    folder_path = 'uni'
    image_files = os.listdir(folder_path)
    random_image = random.choice(image_files)
    random_image = os.path.join(folder_path, random_image)

    # if file name starts with 'excluded_', 'posted_' or ends with '.mp4', try again
    while random_image.startswith('uni/excluded_') or random_image.startswith('uni/posted_') or random_image.endswith('.mp4'):
        random_image = random.choice(image_files)
        random_image = os.path.join(folder_path, random_image)

    print('selected', random_image)

    if os.path.getsize(random_image) > max_size:
        resize_image(random_image)

    with open(random_image, 'rb') as f:
        img_data = f.read()

        # 4 percent chance to make the post say 'big boobs'
        random_int = random.randint(1, 1000)
        post_text = ''
        if random_int <= 40:
            post_text = 'big boobs'
        elif random_int == 10000:
            post_text = 'huge boobs. enormous boobs. gigantic bahonkadonks.'

        client.send_image(
            text=post_text, image=img_data, image_alt=f'photo of a cat, from twitter.com/unicouniuni3'
        )

    print('posted', random_image)

    # after successfully posting, rename the image to stop reposts
    new_image_name = os.path.join(folder_path, 'posted_' + os.path.basename(random_image))
    os.rename(random_image, new_image_name)

if __name__ == '__main__':
    main()
