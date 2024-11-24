from getpass import getpass
import os
import subprocess
from dotenv import load_dotenv
from cryptography.fernet import Fernet

def generate_key():
    """Generate a key for encryption."""
    return Fernet.generate_key()

def encrypt_data(data, key):
    """Encrypt data using the provided key."""
    fernet = Fernet(key)
    return fernet.encrypt(data.encode()).decode()

def decrypt_data(data, key):
    """Decrypt data using the provided key."""
    fernet = Fernet(key)
    return fernet.decrypt(data.encode()).decode()

def check_env_credentials():
    """
    Check if .env file exists and has required OAuth credentials.
    Returns True if credentials exist, False otherwise.
    """
    if not os.path.exists(".env"):
        return False
        
    # Load existing environment variables
    load_dotenv()
    
    # Check if required credentials exist
    client_id = os.getenv('GOOGLE_CLIENT_ID')
    client_secret = os.getenv('GOOGLE_CLIENT_SECRET')
    db_uri = os.getenv('SQLALCHEMY_DATABASE_URI')
    sender_email = os.getenv('SENDER_EMAIL')
    sender_password = os.getenv('SENDER_PASSWORD')
    
    if client_id and client_secret and db_uri and sender_email and sender_password:
        print("[INFO] Required credentials already exist in .env file.")
        return True
    return False

def create_env_file(client_id, client_secret, sender_email, sender_password, encryption_key):

    """Creates a .env file to store Google OAuth credentials."""
    # Get the absolute path to the instance folder
    instance_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'instance'))
    
    # Create instance directory if it doesn't exist
    os.makedirs(instance_path, exist_ok=True)
    
    # Define database path
    db_path = os.path.join(instance_path, 'slash.db')
    
    encrypted_client_secret = encrypt_data(client_secret, encryption_key)
    
    env_content = f"""# Environment variables for Slash
GOOGLE_CLIENT_ID={client_id}

GOOGLE_CLIENT_SECRET={encrypted_client_secret}
SENDER_EMAIL={sender_email}
SENDER_PASSWORD={sender_password}

SQLALCHEMY_DATABASE_URI=sqlite:///{db_path}
SQLALCHEMY_TRACK_MODIFICATIONS=False
"""
    with open(".env", "w") as env_file:
        env_file.write(env_content)
    print("[INFO] .env file created successfully.")
    print(f"[INFO] Database will be created at: {db_path}")

def install_dependencies():
    """Installs dependencies from requirements.txt."""
    print("[INFO] Installing dependencies...")
    try:
        subprocess.check_call(["pip3", "install", "-r", "requirements.txt"])
        print("[INFO] Dependencies installed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Failed to install dependencies: {e}")

def main():
    print("Welcome to the Slash installation script!")
    print("This script will help you set up the project quickly.")

    # Check if instance/ directory exists
    instance_path = os.path.join(os.path.dirname(__file__), 'instance')
    if not os.path.exists(instance_path):
        print("[INFO] 'instance/' directory not found. Recreating .env file.")
        # Remove existing .env file if it exists
        if os.path.exists(".env"):
            os.remove(".env")
        print("[INFO] .env file recreated.")
        # Proceed to collect OAuth credentials
        if not check_env_credentials():
            print("[INFO] OAuth credentials or Email credentials not found. Please enter them now.")
            client_id = input("Enter your Google Client ID: ").strip()
            client_secret = getpass("Enter your Google Client Secret: ").strip()
            sender_email = input("Enter your Google Email ID: ").strip()
            sender_password = getpass("Enter your Google Email Password: ")

            # Validate input
            if not client_id or not client_secret or not sender_email or not sender_password:
                print("[ERROR] Both Client ID and Client Secret are required. Exiting...")
                return

            # Create .env file

            encryption_key = generate_key()
            create_env_file(client_id, client_secret, sender_email, sender_password, encryption_key)
            print(f"[INFO] Encryption key: {encryption_key.decode()}")

    else:
        if not check_env_credentials():
            print("[INFO] OAuth credentials or Email credentials not found. Please enter them now.")
            client_id = input("Enter your Google Client ID: ").strip()
            client_secret = getpass("Enter your Google Client Secret: ").strip()
            sender_email = input("Enter your Google Email ID: ").strip()
            sender_password = getpass("Enter your Google Email Password: ")

            # Validate input
            if not client_id or not client_secret or not sender_email or not sender_password:
                print("[ERROR] Both Client ID and Client Secret are required. Exiting...")
                return

            # Create .env file

            encryption_key = generate_key()
            create_env_file(client_id, client_secret, sender_email, sender_password, encryption_key)
            print(f"[INFO] Encryption key: {encryption_key.decode()}")


    # Step 2: Install dependencies
    install_dependencies()

    # Final Instructions
    print("\n[INFO] Setup complete!")
    print("Next Steps:")
    print("1. Set the environment variable for Flask:")
    print("   - For macOS/Linux: export FLASK_APP=./src/modules/app")
    print("   - For Windows Command Prompt: set FLASK_APP=.\src\modules\app")
    print("   - For Windows PowerShell: $Env:FLASK_APP='.\src\modules\app'")
    print("2. Run the application: flask run")
    print("3. Open your browser and visit: http://localhost:5000/")
    print("\nHappy shopping with Slash!")

main()
