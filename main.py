# Ocr recognizer

# EasyOCR service using Flask that serves as a web endpoint that ingests the URL or filepath and returns the JSON output.

from flask import Flask
from flask import jsonify
import easyocr
import torch
import gc
import requests
import os

# Do gc and memory cleanup as Pytorch is memory intensive
gc.collect()
torch.cuda.ipc_collect()
torch.cuda.empty_cache()
torch.cuda.reset_peak_memory_stats()
torch.cuda.reset_accumulated_memory_stats()

reader = easyocr.Reader(['en'],gpu=True) 

app = Flask(__name__)

@app.route("/<path:url>")

def image(url):
    global reader

    # Add ImageMagick options for specific use cases
    if "IMAGE_SPLIT" in os.environ:
        IMAGE_SPLIT=int(os.environ["IMAGE_SPLIT"])
    else:
        IMAGE_SPLIT=""    

    if IMAGE_SPLIT:
            print(f"Using convert to segment image",flush=True)
            img_data= requests.get(url).content
            with open('image.jpg','wb') as handler:
                handler.write(img_data)
            os.system('convert -crop 50%x100% image.jpg output.jpg')
            url='output-0.jpg'
            url_2='output-1.jpg'

    else:
            print(f"Using unmodified image for OCR",flush=True)


    # Works with images, how to make it work with url
    if "CANVAS_SIZE" in os.environ:
            CANVAS_SIZE=int(os.environ["CANVAS_SIZE"])
    else:
        CANVAS_SIZE=""

    if CANVAS_SIZE:
            print(f"Using custom canvas size of { CANVAS_SIZE }",flush=True)
            result = reader.readtext(url,canvas_size=CANVAS_SIZE,detail=0,paragraph=True)
            
            if IMAGE_SPLIT:
                result += reader.readtext(url_2,canvas_size=CANVAS_SIZE,detail=0,paragraph=True)
    else:
            print("Using default canvas size of 2560",flush=True)
            result = reader.readtext(url,detail=0,paragraph=True)
            
            if IMAGE_SPLIT:
                result += reader.readtext(url_2,detail=0,paragraph=True)

    #return jsonify(result)

    # Do gc and memory cleanup as Pytorch is memory intensive
    gc.collect()
    torch.cuda.ipc_collect()
    torch.cuda.empty_cache()
    torch.cuda.reset_peak_memory_stats()
    torch.cuda.reset_accumulated_memory_stats()

    #del(reader)

    return jsonify(result)

# Use environment variable here from docker compose
app.run(host="0.0.0.0",port=7777)
