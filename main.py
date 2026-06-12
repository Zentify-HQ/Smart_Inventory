import os
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

# Import fungsi dari file lain (database.py dan algorithms.py)
from database import get_db_connection 
from algorithms import custom_hash, merge_sort, binary_search, build_category_tree, PeminjamanQueue

app = FastAPI(title="Sistem Katalog Pintar")

# --- KONFIGURASI PATH ---
# Mendapatkan lokasi direktori tempat file main.py berada
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Setup folder untuk Templates dan Static files menggunakan absolute path
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")

# --- ROOT (Menampilkan HTML) ---
@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")

# --- MODELS ---
class User(BaseModel):
    username: str
    password: str

# Inisialisasi Queue (Antrean)
queue_manager = PeminjamanQueue()

# --- ENDPOINTS ---

# 1. HASHING (Register)
@app.post("/register")
def register(user: User):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password_hash) VALUES (%s, %s)", 
                       (user.username, custom_hash(user.password)))
        conn.commit()
        return {"message": "User berhasil didaftarkan"}
    except Exception as e:
        raise HTTPException(status_code=400, detail="Username sudah ada")
    finally:
        cursor.close(); conn.close()

# 2. LOGIN
@app.post("/login")
def login(user: User):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT password_hash FROM users WHERE username = %s", (user.username,))
        result = cursor.fetchone()
        
        if result and result['password_hash'] == custom_hash(user.password):
            return {"message": "Login berhasil!", "username": user.username}
        else:
            raise HTTPException(status_code=401, detail="Username atau Password salah")
    finally:
        cursor.close(); conn.close()

# 3. TREE (Katalog Kategori)
@app.get("/categories/tree")
def get_categories_tree():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM categories")
    data = cursor.fetchall()
    cursor.close(); conn.close()
    return build_category_tree(data)

# 4. MERGE SORT (Mengurutkan Item)
@app.get("/items/sorted")
def get_sorted_items():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM items")
    data = cursor.fetchall()
    cursor.close(); conn.close()
    return merge_sort(data)

# 5. BINARY SEARCH (Cari Item dengan ID)
@app.get("/items/search/{item_id}")
def search_item(item_id: int):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM items ORDER BY id ASC") 
    data = cursor.fetchall()
    cursor.close(); conn.close()
    
    result = binary_search(data, item_id)
    if not result: raise HTTPException(status_code=404, detail="Data tidak ditemukan")
    return result

# 6. QUEUE (Antrean Peminjaman)
@app.post("/items/queue")
def add_to_queue(item_id: int):
    queue_manager.enqueue(item_id)
    return {"message": "Item ditambahkan ke antrean", "queue_length": len(queue_manager.queue)}

@app.get("/items/queue/process")
def process_queue():
    item = queue_manager.dequeue()
    if not item: return {"message": "Antrean kosong"}
    return {"item_diproses": item}from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

# Import fungsi dari file lain (database.py dan algorithms.py)
from database import get_db_connection 
from algorithms import custom_hash, merge_sort, binary_search, build_category_tree, PeminjamanQueue

app = FastAPI(title="Sistem Katalog Pintar")

# Setup folder untuk Templates dan Static files
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# --- ROOT (Menampilkan HTML) ---
@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")

# --- MODELS ---
class User(BaseModel):
    username: str
    password: str

# Inisialisasi Queue (Antrean)
queue_manager = PeminjamanQueue()

# --- ENDPOINTS ---

# 1. HASHING (Register)
@app.post("/register")
def register(user: User):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password_hash) VALUES (%s, %s)", 
                       (user.username, custom_hash(user.password)))
        conn.commit()
        return {"message": "User berhasil didaftarkan"}
    except Exception as e:
        raise HTTPException(status_code=400, detail="Username sudah ada")
    finally:
        cursor.close(); conn.close()

# 2. LOGIN
@app.post("/login")
def login(user: User):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT password_hash FROM users WHERE username = %s", (user.username,))
        result = cursor.fetchone()
        
        if result and result['password_hash'] == custom_hash(user.password):
            return {"message": "Login berhasil!", "username": user.username}
        else:
            raise HTTPException(status_code=401, detail="Username atau Password salah")
    finally:
        cursor.close(); conn.close()

# 3. TREE (Katalog Kategori)
@app.get("/categories/tree")
def get_categories_tree():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM categories")
    data = cursor.fetchall()
    cursor.close(); conn.close()
    return build_category_tree(data)

# 4. MERGE SORT (Mengurutkan Item)
@app.get("/items/sorted")
def get_sorted_items():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM items")
    data = cursor.fetchall()
    cursor.close(); conn.close()
    return merge_sort(data)

# 5. BINARY SEARCH (Cari Item dengan ID)
@app.get("/items/search/{item_id}")
def search_item(item_id: int):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM items ORDER BY id ASC") 
    data = cursor.fetchall()
    cursor.close(); conn.close()
    
    result = binary_search(data, item_id)
    if not result: raise HTTPException(status_code=404, detail="Data tidak ditemukan")
    return result

# 6. QUEUE (Antrean Peminjaman)
@app.post("/items/queue")
def add_to_queue(item_id: int):
    queue_manager.enqueue(item_id)
    return {"message": "Item ditambahkan ke antrean", "queue_length": len(queue_manager.queue)}

@app.get("/items/queue/process")
def process_queue():
    item = queue_manager.dequeue()
    if not item: return {"message": "Antrean kosong"}
    return {"item_diproses": item}
