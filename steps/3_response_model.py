from fastapi import FastAPI
from pydantic import BaseModel
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

app = FastAPI()


class GpioStatusResponse(BaseModel):
    gpio: int
    on: bool


class SetGPIO(BaseModel):
    on: bool


@app.get("/read/{gpio}", response_model=GpioStatusResponse)
def read_root(gpio: int):
    GPIO.setup(gpio, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    return GpioStatusResponse(gpio=gpio, on=GPIO.input(gpio))


@app.patch("/set/{gpio}", response_model=GpioStatusResponse)
def read_item(gpio: int, value: SetGPIO):
    if value.on:
        GPIO.setup(gpio, GPIO.OUT, initial=GPIO.HIGH)
    else:
        GPIO.setup(gpio, GPIO.OUT, initial=GPIO.LOW)
    return GpioStatusResponse(gpio=gpio, on=value.on)
