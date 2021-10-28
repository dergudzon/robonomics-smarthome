#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from config import KEYS
from fastapi import FastAPI, Form, Request
from fastapi.responses import PlainTextResponse, HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from substrateinterface import SubstrateInterface, Keypair
import nacl.secret
import base64


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def get_webpage(request: Request):
    result = "Eneter your string"
    return templates.TemplateResponse("form.html", {"request": request, 'result': result})
    
@app.post("/decoded")
async def str_decoding(request: Request, data: str = Form(...)):
    mnemonic = KEYS["seed"]
    kp = Keypair.create_from_mnemonic(mnemonic, ss58_format=32)
    seed = kp.seed_hex
    b = bytes(seed[0:32], "utf8")
    box = nacl.secret.SecretBox(b)
    try:
        decrypted = box.decrypt(base64.b64decode(data))
    except Exception as e:
        return f"error occured: {e}"
    return decrypted