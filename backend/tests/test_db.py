import psycopg2
from psycopg2 import OperationalError
import os

# Tomamos la URL de Render
DATABASE_URL = "postgresql://weather_user:ZeJAocUvQh8NbJ0VMALN6FyAnSRuV5nZ@dpg-d37irhmmcj7s73fmd61g-a.oregon-postgres.render.com/weather_db_192e"

try:
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute("SELECT NOW();")
    result = cur.fetchone()
    print("✅ Conexión OK, hora actual DB:", result[0])
    print("✅ Conexión OK, hora actual DB:", cur)
    cur.close()
    conn.close()
except OperationalError as e:
    print("❌ Error de conexión:", e)