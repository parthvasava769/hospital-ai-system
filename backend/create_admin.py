from app.database import SessionLocal
from app.models.user import User

db = SessionLocal()

admin = User(
    name="Admin",                     
    email="vasavakokila017@gmail.com",          
    phone="9081615829",               
    password="parth347",
    role="admin"
)

db.add(admin)
db.commit()
db.close()

print("Admin created")