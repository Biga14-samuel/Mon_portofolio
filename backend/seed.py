import argparse

from app.auth import hash_password
from app.database import Base, engine


def main() -> None:
    parser = argparse.ArgumentParser(description="Seed initial data and generate bcrypt hashes.")
    parser.add_argument("--password", help="Generate a bcrypt hash for this password and exit.")
    parser.add_argument("--init-db", action="store_true", help="Create tables without inserting portfolio content.")
    args = parser.parse_args()

    if args.password:
        print(hash_password(args.password))
        return

    Base.metadata.create_all(bind=engine)
    if args.init_db:
        print("Database tables are ready. Add portfolio content from the admin interface.")


if __name__ == "__main__":
    main()
