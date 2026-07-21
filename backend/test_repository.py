from app.database.repositories import UserRepository
from app.database.session import SessionLocal


def main():
    db = SessionLocal()

    try:
        repo = UserRepository(db)

        user = repo.get_by_username("abhinay")

        if user is None:
            user = repo.create_user(
                username="abhinay",
                email="abhinay@example.com",
                full_name="Abhinay Kumar",
            )
            print("✅ User created:")
        else:
            print("ℹ️ User already exists:")

        print(user)

        print("\n📋 All Users:")

        for u in repo.get_all():
            print(u)

    finally:
        db.close()


if __name__ == "__main__":
    main()