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

    # Works with images, how to make it work with url
    if "CANVAS_SIZE" in os.environ:
	    CANVAS_SIZE=int(os.environ["CANVAS_SIZE"])
    else:
        CANVAS_SIZE=""

    if CANVAS_SIZE:
	    print(f"Using custom canvas size of { CANVAS_SIZE }")
	    result = reader.readtext(url,canvas_size=CANVAS_SIZE,detail=0,paragraph=True)
    else:
	    print("Using default canvas size of 2560")
	    result = reader.readtext(url,detail=0,paragraph=True)

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
