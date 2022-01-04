from fastapi import FastAPI
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

app = FastAPI()


@app.get("/read/{gpio}")
def read_root(gpio: int):
    GPIO.setup(gpio, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    return {"gpio": gpio, "on": GPIO.input(gpio)}
