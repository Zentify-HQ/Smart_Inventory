from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
# Kita tetap menggunakan database.py seperti struktur awalmu
from database import get_db_connection 
from algorithms import custom_hash, merge_sort, binary_search, build_category_tree, PeminjamanQueue

app = FastAPI(title="Sistem Katalog Pintar")
from fastapi.staticfiles import StaticFiles
@app.get("/")
def read_root():
    return {"message": "Selamat datang di Zentify Smart Inventory!"}

# Inisialisasi Queue (Antrean)
queue_manager = PeminjamanQueue()

# --- MODELS ---
class User(BaseModel):
    username: str
    password: str

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

@app.post("/login")
def login(user: User):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        # Ambil hash dari database berdasarkan username
        cursor.execute("SELECT password_hash FROM users WHERE username = %s", (user.username,))
        result = cursor.fetchone()
        
        # Bandingkan hash (input password di-hash dulu, lalu dicek dengan hash di DB)
        if result and result['password_hash'] == custom_hash(user.password):
            return {"message": "Login berhasil!", "username": user.username}
        else:
            raise HTTPException(status_code=401, detail="Username atau Password salah")
    finally:
        cursor.close(); conn.close()

# 2. TREE (Katalog Kategori)
@app.get("/categories/tree")
def get_categories_tree():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM categories")
    data = cursor.fetchall()
    cursor.close(); conn.close()
    return build_category_tree(data)

# 3. MERGE SORT (Mengurutkan Item)
@app.get("/items/sorted")
def get_sorted_items():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM items")
    data = cursor.fetchall()
    cursor.close(); conn.close()
    return merge_sort(data)

# 4. BINARY SEARCH (Cari Item dengan ID)
@app.get("/items/search/{item_id}")
def search_item(item_id: int):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    # Binary search membutuhkan data yang terurut
    cursor.execute("SELECT * FROM items ORDER BY id ASC") 
    data = cursor.fetchall()
    cursor.close(); conn.close()
    
    result = binary_search(data, item_id)
    if not result: raise HTTPException(status_code=404, detail="Data tidak ditemukan")
    return result

# 5. QUEUE (Antrean Peminjaman)
@app.post("/items/queue")
def add_to_queue(item_id: int):
    queue_manager.enqueue(item_id)
    return {"message": "Item ditambahkan ke antrean", "queue_length": len(queue_manager.queue)}

@app.get("/items/queue/process")
def process_queue():
    item = queue_manager.dequeue()
    if not item: return {"message": "Antrean kosong"}
    return {"item_diproses": item}

app.mount("/static", StaticFiles(directory="static"), name="static")
