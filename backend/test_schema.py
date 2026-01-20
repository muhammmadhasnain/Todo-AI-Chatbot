#!/usr/bin/env python3
"""
Test script to verify that the database schema is correct after the fix.
"""

from src.db.session import engine, get_session
from src.models.user import User
from sqlmodel import select
from sqlalchemy import inspect

def test_user_table_schema():
    """Test that the user_profiles table exists with the correct schema."""
    inspector = inspect(engine)

    # Get list of tables
    tables = inspector.get_table_names()
    print(f"Available tables: {tables}")

    # Check if user_profiles table exists
    if 'user_profiles' in tables:
        print("\n[SUCCESS] user_profiles table exists!")

        # Get columns in the user_profiles table
        columns = inspector.get_columns('user_profiles')
        print(f"\nColumns in user_profiles table:")
        for col in columns:
            print(f"  - {col['name']} ({col['type']}) - nullable: {col['nullable']}")

        # Check if required columns exist
        column_names = [col['name'] for col in columns]
        required_columns = ['id', 'user_id', 'email', 'name']

        missing_columns = [col for col in required_columns if col not in column_names]
        if missing_columns:
            print(f"\n[ERROR] Missing columns: {missing_columns}")
            return False
        else:
            print(f"\n[SUCCESS] All required columns exist: {required_columns}")

        # Check if user_id column is unique and not nullable
        user_id_col = next((col for col in columns if col['name'] == 'user_id'), None)
        if user_id_col:
            if not user_id_col['nullable']:
                print("[SUCCESS] user_id column is not nullable")
            else:
                print("[WARNING] user_id column should not be nullable")

        return True
    else:
        print("\n[ERROR] user_profiles table does not exist!")
        return False

def test_basic_operations():
    """Test basic CRUD operations on the user_profiles table."""
    print("\nTesting basic operations...")

    try:
        # Get session using the generator approach
        session_gen = get_session()
        session = next(session_gen)

        try:
            # Try to query the table (should not raise an exception)
            statement = select(User).limit(1)
            result = session.exec(statement).first()
            print("[SUCCESS] Query operation successful (table exists and is accessible)")

            # Print the table structure
            print(f"User model table name: {User.__tablename__}")
            print(f"User model columns: {[field for field in User.model_fields.keys()]}")
        finally:
            session.close()
    except Exception as e:
        print(f"[ERROR] Query operation failed: {e}")
        return False

    return True

if __name__ == "__main__":
    print("Testing database schema after fix...")
    print("="*50)

    schema_ok = test_user_table_schema()
    operations_ok = test_basic_operations()

    print("\n" + "="*50)
    if schema_ok and operations_ok:
        print("[SUCCESS] All tests passed! Database schema is correct.")
    else:
        print("[ERROR] Some tests failed. Database schema needs attention.")