# database.py
import sqlite3

DATABASE_NAME = 'bot_data.db'

def connect_db():
    """Veritabanı bağlantısını kurar."""
    conn = None
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        conn.row_factory = sqlite3.Row # Sütun isimleriyle verilere erişmek için
        return conn
    except sqlite3.Error as e:
        # Normalde burada loglama veya hata bildirimi olurdu
        print(e)
        return None

def init_db():
    """Veritabanı tablolarını oluşturur (eğer yoksa)."""
    conn = connect_db()
    if conn:
        try:
            cursor = conn.cursor()
            # Kullanıcılar Tablosu: user_id, dil, kayıt tarihi, ban durumu
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    lang TEXT DEFAULT 'tr',
                    reg_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                    is_banned BOOLEAN DEFAULT FALSE
                )
            """)
            # Ürünler Tablosu: Ürün adı, fiyatı, stok durumu (veritabanındaki key sayısına göre belirlenebilir), açıklama
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS products (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE NOT NULL,
                    price REAL NOT NULL,
                    description TEXT
                )
            """)
            # Keys Tablosu: Key string'i, hangi ürüne ait olduğu, durumu (aktif/kullanıldı), kime satıldığı, kullanım tarihi
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS keys (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    key_string TEXT UNIQUE NOT NULL,
                    product_id INTEGER NOT NULL,
                    status TEXT DEFAULT 'active', -- 'active', 'used'
                    used_by_user_id INTEGER,
                    used_date DATETIME,
                    FOREIGN KEY (product_id) REFERENCES products(id),
                    FOREIGN KEY (used_by_user_id) REFERENCES users(user_id)
                )
            """)
            # Hediye Kodları Tablosu: Kod string'i, hangi ürünü verdiği, kullanım limiti, kaç kere kullanıldığı
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS gift_codes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    code_string TEXT UNIQUE NOT NULL,
                    product_id INTEGER NOT NULL,
                    usage_limit INTEGER DEFAULT 1, -- -1 for unlimited
                    used_count INTEGER DEFAULT 0,
                    is_active BOOLEAN DEFAULT TRUE,
                    FOREIGN KEY (product_id) REFERENCES products(id)
                )
            """)
             # Satışlar Tablosu: Satış ID, kullanıcı ID, ürün ID, key ID, miktar, tarih, durum (bekliyor/tamamlandı/iptal)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS sales (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    product_id INTEGER NOT NULL,
                    key_id INTEGER, -- Eğer bir key atandıysa
                    amount REAL NOT NULL,
                    sale_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                    status TEXT DEFAULT 'pending', -- 'pending', 'completed', 'cancelled'
                    FOREIGN KEY (user_id) REFERENCES users(user_id),
                    FOREIGN KEY (product_id) REFERENCES products(id),
                    FOREIGN KEY (key_id) REFERENCES keys(id)
                )
            """)

            conn.commit()
            print("Veritabanı tabloları kontrol edildi/oluşturuldu.")
        except sqlite3.Error as e:
            print(e) # Hata durumunda bilgi ver
        finally:
            conn.close()

# --- Kullanıcı Fonksiyonları ---
def add_user(user_id, lang='tr'):
    conn = connect_db()
    if conn:
        try:
            cursor = conn.cursor()
            # Kullanıcı zaten var mı diye kontrol et
            cursor.execute("SELECT user_id FROM users WHERE user_id = ?", (user_id,))
            if cursor.fetchone() is None:
                cursor.execute("INSERT INTO users (user_id, lang) VALUES (?, ?)", (user_id, lang))
                conn.commit()
                print(f"Kullanıcı {user_id} eklendi.")
        except sqlite3.Error as e:
            print(e)
        finally:
            conn.close()

def get_user_lang(user_id):
    conn = connect_db()
    lang = None
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT lang FROM users WHERE user_id = ?", (user_id,))
            row = cursor.fetchone()
            if row:
                lang = row['lang']
        except sqlite3.Error as e:
            print(e)
        finally:
            conn.close()
    return lang

def set_user_lang(user_id, lang):
    conn = connect_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("UPDATE users SET lang = ? WHERE user_id = ?", (lang, user_id))
            conn.commit()
        except sqlite3.Error as e:
            print(e)
        finally:
            conn.close()

def is_user_banned(user_id):
    conn = connect_db()
    banned = False
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT is_banned FROM users WHERE user_id = ?", (user_id,))
            row = cursor.fetchone()
            if row:
                banned = bool(row['is_banned'])
        except sqlite3.Error as e:
            print(e)
        finally:
            conn.close()
    return banned

def set_user_ban_status(user_id, status):
    conn = connect_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("UPDATE users SET is_banned = ? WHERE user_id = ?", (status, user_id))
            conn.commit()
        except sqlite3.Error as e:
            print(e)
        finally:
            conn.close()

def get_all_user_ids():
    conn = connect_db()
    user_ids = []
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT user_id FROM users")
            rows = cursor.fetchall()
            user_ids = [row['user_id'] for row in rows]
        except sqlite3.Error as e:
            print(e)
        finally:
            conn.close()
    return user_ids

# --- Ürün Fonksiyonları ---
def add_product(name, price, description=None):
    conn = connect_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO products (name, price, description) VALUES (?, ?, ?)", (name, price, description))
            conn.commit()
            return cursor.lastrowid
        except sqlite3.IntegrityError: # Ürün adı zaten varsa
             print(f"Hata: '{name}' adında bir ürün zaten var.")
             return None
        except sqlite3.Error as e:
            print(e)
            return None
        finally:
            conn.close()

def get_product_by_name(name):
    conn = connect_db()
    product = None
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM products WHERE name = ?", (name,))
            product = cursor.fetchone()
        except sqlite3.Error as e:
            print(e)
        finally:
            conn.close()
    return product # None veya sqlite3.Row objesi döner

def get_product_by_id(product_id):
    conn = connect_db()
    product = None
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM products WHERE id = ?", (product_id,))
            product = cursor.fetchone()
        except sqlite3.Error as e:
            print(e)
        finally:
            conn.close()
    return product # None veya sqlite3.Row objesi döner


def get_all_products():
    conn = connect_db()
    products = []
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM products")
            products = cursor.fetchall()
        except sqlite3.Error as e:
            print(e)
        finally:
            conn.close()
    return products # Liste veya boş liste döner

# --- Key Fonksiyonları ---
def add_key(product_name, key_string):
    conn = connect_db()
    if conn:
        try:
            cursor = conn.cursor()
            # Önce ürünün varlığını ve ID'sini bul
            product = get_product_by_name(product_name)
            if not product:
                print(f"Hata: '{product_name}' adında bir ürün bulunamadı.")
                return False

            cursor.execute("INSERT INTO keys (key_string, product_id) VALUES (?, ?)", (key_string, product['id']))
            conn.commit()
            print(f"'{product_name}' ürünü için key eklendi: {key_string}")
            return True
        except sqlite3.IntegrityError:
             print(f"Hata: Bu key ({key_string}) zaten veritabanında var.")
             return False
        except sqlite3.Error as e:
            print(e)
            return False
        finally:
            conn.close()

def get_available_key(product_id):
    conn = connect_db()
    key = None
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM keys WHERE product_id = ? AND status = 'active' LIMIT 1", (product_id,))
            key = cursor.fetchone()
        except sqlite3.Error as e:
            print(e)
        finally:
            conn.close()
    return key # None veya sqlite3.Row objesi döner

def mark_key_used(key_id, user_id):
    conn = connect_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE keys
                SET status = 'used', used_by_user_id = ?, used_date = CURRENT_TIMESTAMP
                WHERE id = ? AND status = 'active'
            """, (user_id, key_id))
            conn.commit()
            return cursor.rowcount > 0 # İşlem başarılı olduysa True döner
        except sqlite3.Error as e:
            print(e)
            return False
        finally:
            conn.close()

def count_keys_by_product(product_id, status='active'):
    conn = connect_db()
    count = 0
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM keys WHERE product_id = ? AND status = ?", (product_id, status))
            count = cursor.fetchone()[0]
        except sqlite3.Error as e:
            print(e)
        finally:
            conn.close()
    return count

def list_keys_by_product(product_name):
    conn = connect_db()
    keys = []
    if conn:
        try:
            cursor = conn.cursor()
             # Önce ürünün varlığını ve ID'sini bul
            product = get_product_by_name(product_name)
            if not product:
                print(f"Hata: '{product_name}' adında bir ürün bulunamadı.")
                return []

            cursor.execute("SELECT * FROM keys WHERE product_id = ?", (product['id'],))
            keys = cursor.fetchall()
        except sqlite3.Error as e:
            print(e)
        finally:
            conn.close()
    return keys # Liste veya boş liste döner

def delete_key_by_string(key_string):
    conn = connect_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM keys WHERE key_string = ?", (key_string,))
            conn.commit()
            return cursor.rowcount > 0 # Silme başarılı olduysa True döner
        except sqlite3.Error as e:
            print(e)
            return False
        finally:
            conn.close()

# --- Hediye Kodu Fonksiyonları ---
def add_gift_code(code_string, product_name, usage_limit=1):
    conn = connect_db()
    if conn:
        try:
            cursor = conn.cursor()
            # Önce ürünün varlığını ve ID'sini bul
            product = get_product_by_name(product_name)
            if not product:
                print(f"Hata: '{product_name}' adında bir ürün bulunamadı.")
                return False

            cursor.execute("INSERT INTO gift_codes (code_string, product_id, usage_limit) VALUES (?, ?, ?)",
                           (code_string, product['id'], usage_limit))
            conn.commit()
            print(f"Hediye kodu eklendi: {code_string} ('{product_name}' ürünü için, Limit: {usage_limit})")
            return True
        except sqlite3.IntegrityError:
             print(f"Hata: Bu hediye kodu ({code_string}) zaten veritabanında var.")
             return False
        except sqlite3.Error as e:
            print(e)
            return False
        finally:
            conn.close()

def get_gift_code_info(code_string):
    conn = connect_db()
    code_info = None
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM gift_codes WHERE code_string = ? AND is_active = TRUE", (code_string,))
            code_info = cursor.fetchone()
        except sqlite3.Error as e:
            print(e)
        finally:
            conn.close()
    return code_info # None veya sqlite3.Row objesi döner

def use_gift_code(code_id):
    conn = connect_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT usage_limit, used_count FROM gift_codes WHERE id = ?", (code_id,))
            code = cursor.fetchone()

            if code and (code['usage_limit'] == -1 or code['used_count'] < code['usage_limit']):
                new_used_count = code['used_count'] + 1
                is_active = True if code['usage_limit'] == -1 or new_used_count < code['usage_limit'] else False

                cursor.execute("UPDATE gift_codes SET used_count = ?, is_active = ? WHERE id = ?",
                               (new_used_count, is_active, code_id))
                conn.commit()
                return True # Kullanım başarılı
            else:
                return False # Kullanım limitine ulaşıldı veya kod aktif değil
        except sqlite3.Error as e:
            print(e)
            return False
        finally:
            conn.close()

# --- Satış Fonksiyonları ---
# Not: Bu fonksiyonlar temel satış kaydı içindir. Tam bir ödeme akışı daha karmaşık olabilir.
def add_sale(user_id, product_id, amount, key_id=None, status='completed'):
    conn = connect_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO sales (user_id, product_id, amount, key_id, status)
                VALUES (?, ?, ?, ?, ?)
            """, (user_id, product_id, amount, key_id, status))
            conn.commit()
            return cursor.lastrowid
        except sqlite3.Error as e:
            print(e)
            return None
        finally:
            conn.close()

# --- İstatistik Fonksiyonları ---
def get_stats():
    conn = connect_db()
    stats = {
        'total_users': 0,
        'total_sales_count': 0,
        'total_keys': 0,
        'active_keys': 0,
        'used_keys': 0,
        'products_stock': {} # Ürün adına göre aktif key sayısı
    }
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM users")
            stats['total_users'] = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM sales WHERE status = 'completed'")
            stats['total_sales_count'] = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM keys")
            stats['total_keys'] = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM keys WHERE status = 'active'")
            stats['active_keys'] = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM keys WHERE status = 'used'")
            stats['used_keys'] = cursor.fetchone()[0]

            # Her ürün için aktif key sayısını al
            cursor.execute("""
                SELECT p.name, COUNT(k.id) as active_count
                FROM products p
                LEFT JOIN keys k ON p.id = k.product_id AND k.status = 'active'
                GROUP BY p.name
            """)
            product_stocks = cursor.fetchall()
            for row in product_stocks:
                 stats['products_stock'][row['name']] = row['active_count']

        except sqlite3.Error as e:
            print(e)
        finally:
            conn.close()
    return stats


# Bot başlatılırken veritabanını başlat
if __name__ == '__main__':
    # Bu blok sadece database.py doğrudan çalıştırıldığında çalışır
    init_db()
    print("Veritabanı başlatma tamamlandı.")
    # Örnek ürün ekleme (İsterseniz botun ilk çalıştırmasında da ekleyebilirsiniz)
    # add_product("King Mod", 25.0, "King Mod açıklaması")
    # add_product("Shield", 25.0, "Shield açıklaması")
    # add_product("Zolo", 25.0, "Zolo açıklaması")
    # add_product("Khan", 25.0, "Khan açıklaması")
    # add_product("Soi7", 25.0, "Soi7 açıklaması")
    # Örnek key ekleme
    # add_key("King Mod", "KING-ABC-123")
    # Örnek hediye kodu ekleme (tek kullanımlık)
    # add_gift_code("FREEBIE", "King Mod", usage_limit=1)
  
