from create_tables import *

cr.execute("SELECT * FROM users WHERE firstName= 'ziko'")
data = cr.fetchall()
print(data)
