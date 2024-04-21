# OCR Recognizer 

EasyOCR service using Flask that serves as a web endpoint that ingests the
URL or filepath and returns the JSON output.

### How is this different from Frigate OCR Recognizer

This is a simple web endpoint. [Frigate ocr recognizer](https://github.com/atv2016/frigate_ocr_recognizer) is a fork from [Frigate plate
recognizer](https://github.com/ljmerza/frigate_plate_recognizer) and more tightly integrates with Frigate using MQTT to exchange
messages and set sublabels in Frigate.

I find it pretty useful when i quickly need to scrape some text from somewhere that i can't get anyway else.

### Usage
Once you have it running you simply do:
```
<your-ipaddres:<yourport>/snapshot.jpeg <or url>
```
And you will get the recognized text back in JSON format, which you can ingest
and index as a list in Homeassistant for example. EasyOCR parameters are 
currently set to paragraph but you can remove that to fit your needs.

### Building
This is only needed if you are re-building your own image because you changed the source.
```
sudo docker build -t <docker namespace>/ocr_recognizer:v1.0.0-yourtag . --no-cache
```
If using semantic versioning, or do:
```
sudo docker build -t <docker namespace>/ocr_recognizer . --no-cache
```
To get the latest tag assigned by docker. Note that it is not recommended to use the latest tag but rather a version tag as per the first example if you don't want things to break unexpectedly.

Optional: 
If you want to upload to docker public registry using a semantic tag (or leave it out to get the latest tag).
```
sudo docker build -t <docker namespace>/ocr_recognizer:v1.0.0-yourtag . --no-cache
sudo docker login
sudo docker push <docker namespace/ocr_recognizer:v1.0.0-yourtag
```
### Running
You can use docker run to run your own image you just build in the previous step:
```
sudo docker run -e TZ=Europe/London -p 7777:7777/tcp -it --gpus all -e NVIDIA_DRIVER_CAPABILITIES=all --privileged -v ./:/config --rm ocr_recognizer:v1.0.0-yourtag (or latest)
```
Or run it from the docker registry by prefacing it with the namespace from docker (if you build your own image make sure to do that as well, e.g. ```-t <docker_namespace```, otherwise docker push might give you problems).

```bash
sudo docker run -e TZ=Europe/London -p 7777:7777/tcp -it --gpus all -e NVIDIA_DRIVER_CAPABILITIES=all --privileged -v ./:/config --rm
ocr_recognizer atv2016/ocr_recognizer:v1.0.0-yourtag (or latest)
```
or just use the docker-compose supplied:

```yml
services:
  ocr_recognizer:
    image: atv2016/ocr_recognizer:latest
    ports:
      - "7777:7777"
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
    privileged: true
    container_name: ocr_recognizer
    volumes:
      - ./:/config
    restart: unless-stopped
    environment:
      - TZ=Europe/London
      - NVIDIA_DRIVER_CAPABILITIES=all
```
And execute:
```
sudo docker-compose up -d
```
<ins>Environment variables</ins>:

CANVAS_SIZE: 1000<br>
IMAGE_SPLIT: 1

IMAGE_SPLIT is specific to ocr_recognizer and my use case but might help you for easier OCR recognition. It will split the image in equal parts left and right using ImageMagick.

[Docker repository](https://hub.docker.com/r/atv2016/ocr_recognizer)

### Automation

Here's an automation that consists of 4 steps, using Homeassistant:

Say you wanted to get the latest school menu which your children's school sometimes publishes but the links are not always consistent.

1. Run this docker container.
2. Setup a scrape in HA to the url that your school publishes (in my case the image is always named differently) so i have to scrape the href attribute in the url. Go to your favorite web inspector, find the link you need, copy the select path, and set the attribute to href. This way you will <ins>always</ins> get the image file the href is linking to.
3. Setup a rest command in HA in your configuration.yaml that you can use on demand and store the return data in a response variable. Restart Homeassistant and you should see the new service.

Something like this should do:
```
rest_command:
  get_school_menu:
    url: "192.168.50.34:7777/{{ states('sensor.web_scrape_your_school_menu_link') }}"
    method: GET
    content_type:  'application/json; charset=utf-8'
```
5. Setup the automation where you use the service of the rest command you just created, and then index the response_variable to get the data you want. Read out the days school menu on TTS for example and bask in the glory of another automation well done (which no doubt will break soon enough).

### EasyOCR optimization

You can give a variety of options to EasyOCR, and you can test them out by using the easy.py script that is included in the repo. Look on the [JadedAI](https://github.com/JaidedAI/EasyOCR) website for the full API reference. You can adjust batch size, scale, margin, canvas and a whole lot more. That said, i found the default to work the best for my needs in the end.

Open easy.py and update:
```
result = reader.readtext(sys.argv[1], canvas_size=1000,detail=0)
```
To whatever parameters you want to add to the call. Save the file, and then run it like so:

```
python3 easy.py <filepath (can be http)>
```
And it will return what it found. It is very bare bones so there is no error handling or anything. But it serves as a quick way to test if an image works with your parameters.

### Copyright
[EasyOCR](https://github.com/JaidedAI/EasyOCR) is copyright EasyOCR and [JadedAI](https://jaded.ai) and comes with a Apache 2.0 license, which is included in this repository as custom. All files in this repository are also released under that same license, again as per custom.
