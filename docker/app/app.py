from fastapi import FastAPI
import psycopg2

print ("Iniciando servidor web")

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Servidor corriendo en docker con FastAPI"}

@app.get("/status")
def status():
    return {"status": "ok"}

def get_db_connection():
    conn = psycopg2.connect(
        host="db",
        database="miapp",
        user="usuario",
        password="password123"
    )
    return conn

# formas de tomar las variables
# por ejemplo a través de variables de entorno
# os.environ.get('DB_HOST')


@app.get("/list_users")
def list_users():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, name, email FROM users;")
    users = cur.fetchall()
    cur.close()
    conn.close()
    return {"users": users}