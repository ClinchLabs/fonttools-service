# 📝 fonttools as a service
A Flask wrapper arround Fonttools. Everyone that ever worked with subsetting knows the pain. Fonttools seems to be the best tool to work with subsetting.
At first I wanted to create a C++ addon for node and briding python but the amount of hassle that comes with it is just to much (might do it one day). 

An example request will look like this
```json
{
    "text": "this is a text that needs to be subsetted",
    "font": "data:;base64,AAEAAAATAQAABAAwRFNJR54SRB0AAzucAAAVdEdERUYAJgOvAAM3fAAAAB5HUE9TCzcPNwADN5wAAAA4R1NVQg4rPbcAAzfUAAADxk9TLzKhPp7JAAABuAAAAGBjbWFwKasvaAAAELQAAAQaY3Z0IA9NGKQAAB2QAAAAomZwZ21+a+VF2k6RQPCf7zsfJ0pWrDr9qJRqfPecwX97k2BOG8QrV5WUyxbhmmcz0SspE8jsvrxZsQOkKZnsHYiZJId3D5vKFPvU1ElMdA7IPS5vIMkDzejlD9AhObNWGdX7rL2sqTi9sNUMo9ljrbCVtGhYw+LXKf+RpMcAAA=="
}
```
logging is done with logentries, you can rename the `settings.example.ini` to `settings.ini` and have your logging sent to logentries.

```
[logentries]
key=your_key
```
The `/health` endpoints gives a few stats 
```
{
  "hostname": "falcon.local",
  "memory": {
    "free": "1856 MB",
    "total": "8192 MB"
  },
  "uptime": "0 days"
}
```
I included a Dockerfile which is very basic, make sure you change the exposed ports if you want to run on another port. 
```bash
FROM python:2

ADD . /app

WORKDIR /app

RUN pip install -r requirements.txt

EXPOSE 9097

CMD [ "python", "app.py" ]
```

## todo
* add more mimetype removal
* add proper mimetype to woff
* health endpoint 
