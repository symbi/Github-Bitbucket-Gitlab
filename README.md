# Github-Bitbucket-Gitlab
## quick start
```
git clone git@github.com:symbi/Github-Bitbucket-Gitlab.git
cd Github-Bitbucket-Gitlab
docker-compose build
docker-compose up -d
```
## session 1
```
docker exec -it python3 python fetch.py https://www.google.com https://stackoverflow.com
ls app
```
### result
```
fetch.py               test
stackoverflow.com.html www.google.com.html
```

## session 2
```
docker exec -it python3 python fetch.py --metadata https://www.google.com https://stackoverflow.com
```
### result
```
site:  www.google.com
num_links:  17
images:  2
last_fetch:  Mon Dec 12 2022 08:50 UTC
site:  stackoverflow.com
num_links:  84
images:  18
last_fetch:  Mon Dec 12 2022 08:50 UTC
```

## Extra
```
docker exec -it python3 python fetch.py --download https://www.google.com https://stackoverflow.com
ls app/test
open app/test/www.google.com/www.google.com/index.html
```
### result
* be able to load the text, but not the image
* download the whole page content
```
docker exec -it python3 python fetch.py --metadata_download https://www.google.com https://stackoverflow.com
```
### result
```
site:  www.google.com
num_links:  19
images:  3
last_fetch:  Mon Dec 12 2022 08:56 UTC
site:  stackoverflow.com
num_links:  86
images:  18
last_fetch:  Mon Dec 12 2022 08:56 UTC
```
reason different from session2:
session2 not fetch with webdriver

## clean up
```
docker-compose down
```
### delete all the downloaded file
```
./clean.sh
```
