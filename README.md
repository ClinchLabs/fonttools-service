# 📝 subset-service
A Flask wrapper arround Fonttools. Everyone that ever worked with subsetting knows the pain. Fonttools seems to be the best tool to work with subsetting.
At first I wanted to create a C++ addon for node and briding python but the amount of hassle that comes with it is just to much (might do it one day). 

An example request will look like this
```javascript
{
    "text": "this is a text that needs to be subsetted",
    "font": "data:;base64,AAEAAAATAQAABAAwRFNJR54SRB0AAzucAAAVdEdERUYAJgOvAAM3fAAAAB5HUE9TCzcPNwADN5wAAAA4R1NVQg4rPbcAAzfUAAADxk9TLzKhPp7JAAABuAAAAGBjbWFwKasvaAAAELQAAAQaY3Z0IA9NGKQAAB2QAAAAomZwZ21+a+VF2k6RQPCf7zsfJ0pWrDr9qJRqfPecwX97k2BOG8QrV5WUyxbhmmcz0SspE8jsvrxZsQOkKZnsHYiZJId3D5vKFPvU1ElMdA7IPS5vIMkDzejlD9AhObNWGdX7rL2sqTi9sNUMo9ljrbCVtGhYw+LXKf+RpMcAAA=="
}
```

I included a Dockerfile which is very basic, make sure you change the exposed ports if you want to run on another port. 
```docker
FROM python:2

ADD . /app

WORKDIR /app

RUN pip install -r requirements.txt

EXPOSE 9097

CMD [ "python", "server.py" ]
```
