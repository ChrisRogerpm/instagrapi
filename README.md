# Installation

Install ImageMagick library:
```
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

