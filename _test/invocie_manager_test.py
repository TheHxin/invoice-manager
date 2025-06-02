from fastapi import FastAPI
from models.invoice import *


app = FastAPI()

@app.post("/invoice")
def post_invoice(invoice : Invoice):
    return invoice