#!/usr/bin/env python3
"""
Helper script to set up local environment variables for email testing.
This script will create a .env file with your email configuration.
"""

import os

def create_env_file():
    """Create a .env file for local development"""
    
    # Check if .env already exists
    if os.path.exists('.env'):
        print("⚠️  .env file already exists!")
        response = input("Do you want to overwrite it? (y/N): ")
        if response.lower() != 'y':
            print("Aborted. Existing .env file preserved.")
            return
    
    print("📧 Setting up local environment for email testing...")
    print()
    
    # Get user input
    print("Please provide your email configuration:")
    resend_api_key = input("Resend API Key (get from https://resend.com/api-keys): ").strip()
    
    if not resend_api_key:
        print("❌ Resend API Key is required for email functionality!")
        return
    
    from_email = input("From Email (default: onboarding@resend.dev): ").strip()
    if not from_email:
        from_email = "onboarding@resend.dev"
    
    secret_key = input("Secret Key (default: dev-secret-key-change-this-in-production): ").strip()
    if not secret_key:
        secret_key = "dev-secret-key-change-this-in-production"
    
    # Create .env content
    env_content = f"""# Flask Configuration
SECRET_KEY={secret_key}
FLASK_ENV=development

# Database Configuration
DATABASE_URL=sqlite:///wedding.db

# Resend Email Configuration
RESEND_API_KEY={resend_api_key}
FROM_EMAIL={from_email}

# Optional: Custom domain
CUSTOM_DOMAIN=yourwedding.tk
"""
    
    # Write to .env file
    try:
        with open('.env', 'w') as f:
            f.write(env_content)
        
        print("✅ .env file created successfully!")
        print("📝 You can now test email functionality locally.")
        print("🚀 Run 'python app.py' to start the development server.")
        
    except Exception as e:
        print(f"❌ Error creating .env file: {e}")

def test_email_config():
    """Test if email configuration is working"""
    print("🧪 Testing email configuration...")
    
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        resend_api_key = os.environ.get('RESEND_API_KEY')
        from_email = os.environ.get('FROM_EMAIL')
        
        if not resend_api_key:
            print("❌ RESEND_API_KEY not found in environment variables")
            return False
        
        print(f"✅ Resend API Key: {resend_api_key[:10]}...")
        print(f"✅ From Email: {from_email}")
        print("✅ Email configuration looks good!")
        return True
        
    except Exception as e:
        print(f"❌ Error testing configuration: {e}")
        return False

if __name__ == "__main__":
    print("🎉 Wedding Website Local Email Setup")
    print("=" * 40)
    print()
    
    choice = input("Choose an option:\n1. Create/Update .env file\n2. Test current configuration\nEnter choice (1 or 2): ").strip()
    
    if choice == "1":
        create_env_file()
    elif choice == "2":
        test_email_config()
    else:
        print("Invalid choice. Please run the script again.")
