import os
import random
from mastodon import Mastodon

# setup
mastodon = Mastodon(
    access_token = 'uni.token.secret',
    api_base_url = os.environ['MASTODON_INSTANCE']
)

folder_path = 'uni'
image_files = os.listdir(folder_path)
random_image = random.choice(image_files)
random_image = os.path.join(folder_path, random_image)

# if file name starts with 'excluded_', try again
while random_image.startswith('uni/excluded_'):
    random_image = random.choice(image_files)
    random_image = os.path.join(folder_path, random_image)

print('selected', random_image)

random_int = random.randint(1, 100)
post_text = ''
if random_int <= 7:
    post_text = 'big boobs'
elif random_int == 100:
    post_text = 'huge boobs. enormous boobs. gigantic bahonkadonks.'

media = mastodon.media_post(random_image)
mastodon.status_post(post_text, media_ids=media)
