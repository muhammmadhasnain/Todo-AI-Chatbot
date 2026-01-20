"""
Test script to verify database connection for Better Auth
"""
import os
import sqlite3
from pathlib import Path

def test_database_connection():
    """Test if database connection works (supports both SQLite and PostgreSQL)"""
    print("Testing database connection...")

    # Get the database URL from environment
    db_url = os.getenv("NEON_DATABASE_URL") or os.getenv("DATABASE_URL")
    print(f"Database URL from environment: {db_url}")

    if not db_url:
        print("[ERROR] No database URL found in environment variables")
        return False

    # Check if it's a PostgreSQL connection
    if db_url.startswith("postgresql://") or db_url.startswith("postgres://"):
        print("Detected PostgreSQL database, testing connection...")
        return test_postgresql_connection(db_url)
    # Check if it's a SQLite connection
    elif db_url.startswith("file:") or db_url.startswith("sqlite:") or db_url.endswith(".db"):
        print("Detected SQLite database, testing connection...")
        return test_sqlite_connection_internal(db_url)
    else:
        # Assume it's SQLite if it doesn't look like PostgreSQL
        print("Assuming SQLite database, testing connection...")
        return test_sqlite_connection_internal(db_url)


def test_sqlite_connection_internal(db_url):
    """Internal function to test SQLite database connection"""
    # Parse SQLite file path from URL
    if db_url.startswith("file:"):
        db_path = db_url[5:]  # Remove "file:" prefix
    elif db_url.startswith("sqlite:"):
        db_path = db_url[7:]  # Remove "sqlite:" prefix
    else:
        db_path = db_url

    print(f"Parsed database path: {db_path}")

    try:
        # Create directory if it doesn't exist
        db_file = Path(db_path)
        db_file.parent.mkdir(parents=True, exist_ok=True)

        # Test connection
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Create a simple test table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS test_table (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL
            )
        """)

        # Insert and retrieve test data
        cursor.execute("INSERT INTO test_table (name) VALUES (?)", ("test",))
        conn.commit()

        cursor.execute("SELECT name FROM test_table WHERE name = ?", ("test",))
        result = cursor.fetchone()

        if result and result[0] == "test":
            print("[OK] SQLite database connection test PASSED")
        else:
            print("[ERROR] SQLite database connection test FAILED")

        # Clean up test data
        cursor.execute("DELETE FROM test_table WHERE name = ?", ("test",))
        conn.commit()

        conn.close()
        print("[OK] SQLite database connection test completed successfully")
        return True

    except Exception as e:
        print(f"[ERROR] SQLite database connection test FAILED: {str(e)}")
        return False


def test_postgresql_connection(db_url):
    """Test PostgreSQL database connection"""
    try:
        # Import psycopg2 for PostgreSQL connection
        import psycopg2
        from urllib.parse import urlparse

        # Parse the PostgreSQL URL
        parsed_url = urlparse(db_url)
        print(f"Connecting to PostgreSQL database: {parsed_url.hostname}:{parsed_url.port}/{parsed_url.path}")

        # Connect to the database
        conn = psycopg2.connect(
            host=parsed_url.hostname,
            port=parsed_url.port,
            database=parsed_url.path.lstrip('/'),
            user=parsed_url.username,
            password=parsed_url.password
        )

        # Test the connection
        cursor = conn.cursor()

        # Execute a simple query
        cursor.execute("SELECT version();")
        result = cursor.fetchone()
        print(f"PostgreSQL version: {result[0] if result else 'Unknown'}")

        # Test with a simple table operation
        cursor.execute("""
            CREATE TEMPORARY TABLE test_table (
                id SERIAL PRIMARY KEY,
                name VARCHAR(50) NOT NULL
            );
        """)

        cursor.execute("INSERT INTO test_table (name) VALUES (%s);", ("test",))
        cursor.execute("SELECT name FROM test_table WHERE name = %s;", ("test",))
        result = cursor.fetchone()

        if result and result[0] == "test":
            print("[OK] PostgreSQL database connection test PASSED")
        else:
            print("[ERROR] PostgreSQL database connection test FAILED")
            return False

        conn.close()
        print("[OK] PostgreSQL database connection test completed successfully")
        return True

    except ImportError:
        print("[ERROR] psycopg2 is not installed. Install it with: pip install psycopg2")
        return False
    except Exception as e:
        print(f"[ERROR] PostgreSQL database connection test FAILED: {str(e)}")
        return False

def test_environment_variables():
    """Test if required environment variables are set"""
    print("\nTesting environment variables...")

    required_vars = [
        "BETTER_AUTH_SECRET",
        "DATABASE_URL",
        "BETTER_AUTH_URL"
    ]

    frontend_vars = [
        "NEXT_PUBLIC_BETTER_AUTH_URL",
        "NEXT_PUBLIC_API_BASE_URL",
        "NEXT_PUBLIC_GOOGLE_CLIENT_ID"
    ]

    backend_vars = [
        "BETTER_AUTH_URL",
        "BETTER_AUTH_SECRET"
    ]

    all_vars = required_vars + frontend_vars + backend_vars

    missing_vars = []
    for var in all_vars:
        if not os.getenv(var):
            missing_vars.append(var)

    if missing_vars:
        print(f"X Missing environment variables: {missing_vars}")
        return False
    else:
        print("[OK] All required environment variables are set")
        return True

if __name__ == "__main__":
    print("Environment and Database Connection Test")
    print("=" * 50)

    env_ok = test_environment_variables()
    db_ok = test_database_connection()

    print("\n" + "=" * 50)
    if env_ok and db_ok:
        print("[OK] All tests PASSED! Environment is properly configured.")
        print("\nYou can now start the frontend and backend servers.")
    else:
        print("[ERROR] Some tests FAILED! Please check the configuration.")
        print("Make sure all environment variables are set correctly.")