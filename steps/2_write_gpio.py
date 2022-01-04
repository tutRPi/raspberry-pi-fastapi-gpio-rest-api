from fastapi import FastAPI
from pydantic import BaseModel
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

app = FastAPI()

class SetGPIO(BaseModel):
    on: bool

@app.get("/read/{gpio}")
def read_root(gpio: int):
    GPIO.setup(gpio, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    return {"gpio": gpio, "on": GPIO.input(gpio)}


@app.patch("/set/{gpio}")
def read_item(gpio: int, value: SetGPIO):
    if value.on:
        GPIO.setup(gpio, GPIO.OUT, initial=GPIO.HIGH)
    else:
        GPIO.setup(gpio, GPIO.OUT, initial=GPIO.LOW)
    return {"gpio": gpio, "on": value.on}