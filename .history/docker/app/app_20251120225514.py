from fastapi import FastAPI

print ("Iniciando servidor web")

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Servidor corriendo en docker con FastAPI"}

@app.get("/status")
def status():
    return {"status": "ok"}