from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
import psycopg2
from typing import Optional

print ("Iniciando servidor web")

app = FastAPI(redoc_url=None)

# Modelos Pydantic para validación
class UserCreate(BaseModel):
    name: str
    email: EmailStr

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    created_at: str

@app.get("/")
def home():
    return {"message": "Servidor corriendo en docker con FastAPI"}

@app.get("/status")
def status():
    return {"status": "ok"}

@app.get("/list_users")
def list_users():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, name, email, created_at FROM users ORDER BY id;")
    users = cur.fetchall()
    cur.close()
    conn.close()

    users_list = [
        {
            "id": user[0],
            "name": user[1],
            "email": user[2],
            "created_at": str(user[3])
        }
        for user in users
    ]
    return {"users": users_list}

@app.get("/users/{user_id}")
def get_user(user_id: int):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, name, email, created_at FROM users WHERE id = %s;", (user_id,))
    user = cur.fetchone()
    cur.close()
    conn.close()

    if user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    return {
        "id": user[0],
        "name": user[1],
        "email": user[2],
        "created_at": str(user[3])
    }

@app.post("/users", status_code=201)
def create_user(user: UserCreate):
    conn = get_db_connection()
    cur = conn.cursor()

    try:
        cur.execute(
            "INSERT INTO users (name, email) VALUES (%s, %s) RETURNING id, name, email, created_at;",
            (user.name, user.email)
        )
        new_user = cur.fetchone()
        conn.commit()

        return {
            "message": "Usuario creado exitosamente",
            "user": {
                "id": new_user[0],
                "name": new_user[1],
                "email": new_user[2],
                "created_at": str(new_user[3])
            }
        }
    except psycopg2.IntegrityError:
        conn.rollback()
        raise HTTPException(status_code=400, detail="El email ya existe")
    finally:
        cur.close()
        conn.close()

@app.put("/users/{user_id}")
def update_user(user_id: int, user: UserUpdate):
    if user.name is None and user.email is None:
        raise HTTPException(status_code=400, detail="Debe proporcionar al menos un campo para actualizar")

    conn = get_db_connection()
    cur = conn.cursor()

    # Verificar si el usuario existe
    cur.execute("SELECT id FROM users WHERE id = %s;", (user_id,))
    if cur.fetchone() is None:
        cur.close()
        conn.close()
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    # Construir query dinámicamente
    update_fields = []
    update_values = []

    if user.name is not None:
        update_fields.append("name = %s")
        update_values.append(user.name)

    if user.email is not None:
        update_fields.append("email = %s")
        update_values.append(user.email)

    update_values.append(user_id)

    try:
        query = f"UPDATE users SET {', '.join(update_fields)} WHERE id = %s RETURNING id, name, email, created_at;"
        cur.execute(query, update_values)
        updated_user = cur.fetchone()
        conn.commit()

        return {
            "message": "Usuario actualizado exitosamente",
            "user": {
                "id": updated_user[0],
                "name": updated_user[1],
                "email": updated_user[2],
                "created_at": str(updated_user[3])
            }
        }
    except psycopg2.IntegrityError:
        conn.rollback()
        raise HTTPException(status_code=400, detail="El email ya existe")
    finally:
        cur.close()
        conn.close()

@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT id FROM users WHERE id = %s;", (user_id,))
    if cur.fetchone() is None:
        cur.close()
        conn.close()
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    cur.execute("DELETE FROM users WHERE id = %s;", (user_id,))
    conn.commit()
    cur.close()
    conn.close()

    return {"message": "Usuario eliminado exitosamente"}

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


