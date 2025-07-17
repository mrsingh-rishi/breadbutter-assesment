#!/usr/bin/env python3
"""
Script to run the talent matchmaking engine with sample data.
"""

import subprocess
import sys
import os
import time

def run_command(command, description):
    """Run a command and handle errors."""
    print(f"\n{'='*50}")
    print(f"🚀 {description}")
    print(f"{'='*50}")
    
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {e}")
        if e.stderr:
            print(f"Error details: {e.stderr}")
        return False

def main():
    """Main function to set up and run the application."""
    print("🎯 Talent Matchmaking Engine Setup")
    print("=" * 50)
    
    # Check if virtual environment exists
    if not os.path.exists("venv"):
        print("📦 Creating virtual environment...")
        if not run_command("python -m venv venv", "Creating virtual environment"):
            sys.exit(1)
    
    # Activate virtual environment and install dependencies
    activate_cmd = "source venv/bin/activate" if os.name != 'nt' else "venv\\Scripts\\activate"
    
    print("📥 Installing dependencies...")
    install_cmd = f"{activate_cmd} && pip install -r requirements.txt"
    if not run_command(install_cmd, "Installing dependencies"):
        print("⚠️  Continuing without installing dependencies...")
    
    # Check if .env file exists
    if not os.path.exists(".env"):
        print("⚙️  Creating .env file...")
        if os.path.exists(".env.example"):
            run_command("cp .env.example .env", "Creating .env file")
        else:
            # Create a basic .env file
            with open(".env", "w") as f:
                f.write("DATABASE_URL=sqlite:///./talent_matchmaking.db\n")
                f.write("SECRET_KEY=your-secret-key-change-this-in-production\n")
                f.write("ALGORITHM=HS256\n")
                f.write("ACCESS_TOKEN_EXPIRE_MINUTES=30\n")
                f.write("ENVIRONMENT=development\n")
    
    # Populate sample data
    print("📊 Populating sample data...")
    data_cmd = f"{activate_cmd} && python scripts/populate_sample_data.py"
    if not run_command(data_cmd, "Populating sample data"):
        print("⚠️  Continuing without sample data...")
    
    # Start the application
    print("🌟 Starting the Talent Matchmaking Engine...")
    print("\n" + "="*50)
    print("📱 Application will be available at:")
    print("   • Main API: http://localhost:8000")
    print("   • API Docs: http://localhost:8000/docs")
    print("   • API Info: http://localhost:8000/info")
    print("="*50)
    print("\n🛑 Press Ctrl+C to stop the server\n")
    
    # Start the server
    server_cmd = f"{activate_cmd} && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"
    try:
        subprocess.run(server_cmd, shell=True, check=True)
    except KeyboardInterrupt:
        print("\n👋 Server stopped. Thank you for using Talent Matchmaking Engine!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
