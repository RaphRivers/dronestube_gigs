import os
import logging
from cryptography.fernet import Fernet

# Configure logging (without exposing sensitive data)
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Path to the virtual environment's activation file
VENV_ACTIVATE_PATH = ".venv/bin/activate" if os.name != "nt" else ".venv\\Scripts\\activate.bat"

# Path to store encrypted data securely
ENCRYPTED_DATA_FILE = "secure_data.enc"

# Function to generate a key and store it in the virtual environment
def generate_key():
    key = Fernet.generate_key().decode()  # Generate a new encryption key
    os.environ["SECRET_KEY"] = key  # Set it in the environment for this session

    # Append the key to the virtual environment's activation file
    try:
        with open(VENV_ACTIVATE_PATH, "a") as f:
            f.write(f'\nexport SECRET_KEY="{key}"\n' if os.name != "nt" else f'\nset SECRET_KEY={key}\n')
        logging.info("Secret key has been generated and stored securely in the virtual environment.")
    except Exception as e:
        logging.error(f"Error storing key in virtual environment: {e}")

# Function to load the key from the environment variable
def load_key():
    key = os.getenv("SECRET_KEY")  # Fetch the key from the environment
    if key is None:
        raise ValueError("SECRET_KEY environment variable not found. Run the script to generate it first.")
    return key.encode()  # Convert to bytes

# Function to encrypt a string
def encrypt_string(string):
    key = load_key()  # Load the encryption key
    encoded_string = string.encode()  # Convert input string to bytes
    f = Fernet(key)  # Create a Fernet cipher object
    encrypted_string = f.encrypt(encoded_string)  # Encrypt the string
    return encrypted_string

# Function to decrypt a string
def decrypt_string(encrypted_string):
    key = load_key()  # Load the encryption key
    f = Fernet(key)  # Create a Fernet cipher object
    decrypted_string = f.decrypt(encrypted_string)  # Decrypt the string
    return decrypted_string.decode()  # Convert back to a normal string

# Function to store encrypted data securely in a file
def store_securely(encrypted_data):
    try:
        with open(ENCRYPTED_DATA_FILE, "wb") as file:
            file.write(encrypted_data)
        logging.info("Encrypted data has been securely stored.")
    except Exception as e:
        logging.error(f"Error storing encrypted data: {e}")

# Function to retrieve encrypted data from a file
def load_encrypted_data():
    try:
        with open(ENCRYPTED_DATA_FILE, "rb") as file:
            encrypted_data = file.read()
        logging.info("Encrypted data has been loaded securely.")
        return encrypted_data
    except FileNotFoundError:
        logging.error("No encrypted data found. Please encrypt and store data first.")
        return None

# Generate the key and store it in the virtual environment if not already set
if os.getenv("SECRET_KEY") is None:
    generate_key()

# Encrypt and store the database connection string securely if not already encrypted or empty
if not os.path.exists(ENCRYPTED_DATA_FILE) or os.stat(ENCRYPTED_DATA_FILE).st_size == 0:
    db_connection_string = input("Enter the database connection string: ").strip()
    if db_connection_string:
        encrypted_db_string = encrypt_string(db_connection_string)
        store_securely(encrypted_db_string)
    else:
        logging.error("Database connection string cannot be empty. Please enter a valid string.")
else:
    logging.info("Encrypted database connection string already exists. Delete 'secure_data.enc' if you want to re-enter it.")
