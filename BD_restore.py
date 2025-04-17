import sqlite3

# Conexión al archivo .db (reemplaza con la ruta de tu archivo si está en otra carpeta)
conn = sqlite3.connect('db/data.db')
cursor = conn.cursor()

# Elimina filas con id >= 7 (ajusta "comments" según corresponda)
cursor.execute("DELETE FROM comments WHERE id >= 7")
cursor.execute("DELETE FROM companies WHERE id >= 3")

# Guarda los cambios y cierra la conexión
conn.commit()
conn.close()

print("Filas eliminadas correctamente.")