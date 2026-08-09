import secrets

from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import User
from app.auth.hashing import hash_password


def seed():
    db: Session = SessionLocal()

    try:
        #Create admin user if it doesn't exist (Generated password will be printed to console)
        admin = db.query(User).filter(
            User.user_login == "admin"
        ).first()

        if admin is None :

            generated_password = secrets.token_urlsafe(12)

            admin = User(
                user_login="admin",
                name="Administrator",
                hashed_password=hash_password(generated_password),
                role="admin"
            )

            db.add(admin)
            db.commit()

            print("################################################################")
            print("¡¡¡¡ADMIN USER CREATED!!!! --> Login: admin")
            print(f"Generated password: {generated_password}")
            print("Save this password now — it will not be shown again.")
            print("################################################################")

        else:
            print("admin user already exists.")
            
        #Create ExposedAdmin user if it doesn't exist (Password is hardcoded for demonstration and test purposes)

        exposed_admin = db.query(User).filter(
            User.user_login == "ExposedAdmin"
        ).first()
        

        if exposed_admin is None:
        
            exposed_admin = User(
                user_login="ExpAdmin",
                name="ExposedAdministrator",
                hashed_password=hash_password("expadmin"),
                role="admin"
            )
        
            db.add(exposed_admin)
            db.commit()

            print("################################################################")
            print("exposed admin user created --> Login: ExpAdmin / Password: expadmin")
            print("################################################################")
            
        else:
            print("exposed admin user already exists.")


    finally:
        db.close()


if __name__ == "__main__":
    seed()