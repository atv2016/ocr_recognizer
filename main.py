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
    result = reader.readtext(url,canvas_size=1000,detail=0,paragraph=True)
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
app.run(os.getenv("HOST",os.getenv("PORT")