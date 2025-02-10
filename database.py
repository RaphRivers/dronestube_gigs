# Description: This module is used to load gigs from the database and create a database engine connection. 
# It uses the secure_encryption module to load the encrypted database connection string and decrypt it. 
# The database engine connection is created using the decrypted database connection string. 
# The load_gigs_from_db function is used to load gigs from the database gigs table and return them as a list of dictionaries. 
# If an error occurs, an empty list is returned. The database engine connection is created using the decrypted database connection string.
# The load_gigs_from_db function is used to load gigs from the database gigs table and return them as a list of dictionaries. 
# If an error occurs, an empty list is returned.   

# Load module to create db engine for connection.
import logging
from sqlalchemy import create_engine, text
from secure_encryption import load_encrypted_data, decrypt_string

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

try:
    # Load the encrypted database connection string
    encrypted_db_string = load_encrypted_data()

    # Ensure encrypted_db_string is not None and is in bytes format
    if not encrypted_db_string:
        logging.error("Encrypted database string is missing or empty.")
        raise SystemExit("Error: No encrypted database string found. Run `secure_encryption.py` first.")

    # Attempt to decrypt the database connection string
    try:
        db_connection_string = decrypt_string(encrypted_db_string)
        logging.info("Database connection string has been securely loaded.")
    except Exception as e:
        logging.error(f"Decryption failed: {e}")
        raise SystemExit("Error: Failed to decrypt the database connection string. Ensure the correct encryption key is set.")

    # Create database engine connection to database
    engine = create_engine(db_connection_string)  

except Exception as e:
    logging.error(f"Critical error loading database connection: {e}")
    raise SystemExit("Error: Database connection setup failed.")

# Define helper function to load gigs from database gigs table
def load_gigs_from_db():
    try:
        with engine.connect() as connection:  # Open connection to database
            result = connection.execute(text("SELECT * FROM gigs"))  # Execute SQL query
            gigs = []  # Create empty list to store gigs
            for row in result.all():  # Loop through database connection result
                gigs.append(dict(row._mapping))  # Convert database connection list result to dictionary
        return gigs  # Return gigs list
    except Exception as e:
        logging.error(f"Error loading gigs from database: {e}")
        return [] # Return empty list if error occurs
