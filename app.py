from fastapi import FastAPI, Request, APIRouter
from fastapi.responses import JSONResponse
import requests

app = FastAPI()
router = APIRouter()


@app.get("/api/hello")
async def hello(request: Request, visitor_name: str = "Guest"):
    client_ip = get_client_ip(request)
    location_data = get_location_data(client_ip)
    temperature = get_temperature(location_data["latitude"], location_data["longitude"])

    response_data = {
        "client_ip": client_ip,
        "location": location_data["city"],
        "greeting": f"Hello, {visitor_name}!, the temperature is {temperature} degrees Celsius in {location_data['city']}",
    }

    return JSONResponse(response_data)


def get_client_ip(request: Request):
    x_forwarded_for = request.headers.get("X-Forwarded-For")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.client.host
    return ip


def get_location_data(ip):
    response = requests.get(f"https://ipapi.co/{ip}/json/")
    data = response.json()
    return {
        "city": data.get("city", "Unknown"),
        "latitude": data.get("latitude"),
        "longitude": data.get("longitude"),
    }


def get_temperature(lat, lon):
    api_key = "8f6f4587f0f37ace4506914e4f1f8da1"
    response = requests.get(
        f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&unit=metric&appid={api_key}"
    )
    data = response.json()
    print(data)
    return data["main"]["temp"]

router.add(app)


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app)