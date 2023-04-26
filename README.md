# Installation

Install ImageMagick and libraries:
```
sudo apt-get install libjpeg-dev libpng-dev libtiff-dev libfreetype6-dev liblcms2-dev libwebp-dev libharfbuzz-dev libfribidi-dev libxcb1-dev
sudo apt-get install default-libmysqlclient-dev build-essential
sudo apt install imagemagick
```

...and comment the line with strict security policies of ImageMagick in `/etc/ImageMagick-6/policy.xml`:
```
<!--<policy domain="path" rights="none" pattern="@*"/>-->
```

```
pip install -U wheel pip -Ur requirements.txt
```


```
python3 src/app.py
```

