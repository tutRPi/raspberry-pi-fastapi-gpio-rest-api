from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel
from fastapi import Depends, FastAPI, HTTPException, status
import RPi.GPIO as GPIO
import secrets

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

app = FastAPI()
security = HTTPBasic()


class GpioStatusResponse(BaseModel):
    gpio: int
    on: bool


class SetGPIO(BaseModel):
    on: bool


def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, "admin")
    correct_password = secrets.compare_digest(credentials.password, "passw0rd")
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


@app.get("/read/{gpio}", response_model=GpioStatusResponse)
def read_root(gpio: int, username: str = Depends(get_current_username)):
    GPIO.setup(gpio, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    return GpioStatusResponse(gpio=gpio, on=GPIO.input(gpio))


@app.patch("/set/{gpio}", response_model=GpioStatusResponse)
def read_item(gpio: int, value: SetGPIO, username: str = Depends(get_current_username)):
    if value.on:
        GPIO.setup(gpio, GPIO.OUT, initial=GPIO.HIGH)
    else:
        GPIO.setup(gpio, GPIO.OUT, initial=GPIO.LOW)
    return GpioStatusResponse(gpio=gpio, on=value.on)
