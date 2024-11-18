from getpass import getpass
import os
import subprocess

def create_env_file(client_id, client_secret):
    """Creates a .env file to store Google OAuth credentials."""
    env_content = f"""# Environment variables for Slash
GOOGLE_CLIENT_ID={client_id}
GOOGLE_CLIENT_SECRET={client_secret}
"""
    with open(".env", "w") as env_file:
        env_file.write(env_content)
    print("[INFO] .env file created successfully.")

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

    # Step 1: Collect Google OAuth credentials
    client_id = input("Enter your Google Client ID: ").strip()
    client_secret = getpass("Enter your Google Client Secret: ").strip()

    # Step 2: Validate input
    if not client_id or not client_secret:
        print("[ERROR] Both Client ID and Client Secret are required. Exiting...")
        return

    # Step 3: Create .env file
    create_env_file(client_id, client_secret)

    # Step 4: Install dependencies
    install_dependencies()

    # Final Instructions
    print("\n[INFO] Setup complete!")
    print("Next Steps:")
    print("1. Set the environment variable for Flask:")
    print("   - For macOS/Linux: export FLASK_APP=./src/modules/app")
    print("   - For Windows Command Prompt: set FLASK_APP=.\src\modules\app")
    print("   - For Windows PowerShell: $Env:FLASK_APP='.\src\modules\app'")
    print("2. Run the application: flask run")
    print("3. Open your browser and visit: http://127.0.0.1:5000/")
    print("\nHappy shopping with Slash!")

if __name__ == "__main__":
    main()
