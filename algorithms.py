import hashlib

# 1. HASHING (Untuk Keamanan Password)
def custom_hash(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

# 2. MERGE SORT (Untuk Mengurutkan Katalog)
def merge_sort(data: list) -> list:
    if len(data) <= 1:
        return data
    mid = len(data) // 2
    left = merge_sort(data[:mid])
    right = merge_sort(data[mid:])
    
    # Merge process
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i]['nama_barang'] < right[j]['nama_barang']:
            result.append(left[i]); i += 1
        else:
            result.append(right[j]); j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result

# 3. BINARY SEARCH (Untuk Pencarian Cepat)
def binary_search(data: list, keyword):
    low = 0
    high = len(data) - 1
    
    while low <= high:
        mid = (low + high) // 2
        
        # Cek apakah keyword adalah angka (ID) atau teks (Nama)
        if isinstance(keyword, int):
            # Mencari berdasarkan ID
            if data[mid]['id'] == keyword:
                return data[mid]
            elif data[mid]['id'] < keyword:
                low = mid + 1
            else:
                high = mid - 1
        else:
            # Mencari berdasarkan Nama (menggunakan .lower())
            target = keyword.lower()
            current = data[mid]['nama_barang'].lower()
            if current == target:
                return data[mid]
            elif current < target:
                low = mid + 1
            else:
                high = mid - 1
    return None
# 4. TREE (Untuk Struktur Kategori)
def build_category_tree(categories: list, parent_id=None):
    tree = []
    for cat in categories:
        if cat['parent_id'] == parent_id:
            children = build_category_tree(categories, cat['id'])
            cat['children'] = children
            tree.append(cat)
    return tree

# 5. QUEUE (Untuk Antrean Peminjaman)
class PeminjamanQueue:
    def __init__(self):
        self.queue = []
    
    def enqueue(self, item):
        self.queue.append(item)
    
    def dequeue(self):
        if len(self.queue) > 0:
            return self.queue.pop(0)
        return None
