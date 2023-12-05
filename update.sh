#!/bin/bash

# get urls from twiiit.com. they do most of the work for filtering out ratelimited/dead instances

uni_url=$(curl https://twiiit.com/unicouniuni3 -s -L -I -o /dev/null -w '%{url_effective}')
alfie_url=$(curl https://twiiit.com/goodboyalfie -s -L -I -o /dev/null -w '%{url_effective}')

# save images for 2 minutes, then automatically cancel. prefix with nitter: to use an instance that isn't in the gallery-dl list
timeout 120s gallery-dl "nitter:$uni_url"
# less time because it's an inactive account
timeout 45s gallery-dl "nitter:$alfie_url"

# remove any partially downloaded files and move the new files
rm gallery-dl/*/unicouniuni3/*.part
rm gallery-dl/*/goodboyalfie/*.part
mv gallery-dl/*/unicouniuni3/* uni/
mv gallery-dl/*/goodboyalfie/* alfie/

rm -rf gallery-dl

git pull
git commit -am "[automated] update images"
git push -u
