#!/usr/bin/env python3
"""
Test script to verify Brevo API key and diagnose issues
"""

import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_brevo_api_key():
    """Test the Brevo API key"""
    print("🔍 Testing Brevo API Key...")
    print("=" * 50)
    
    # Get API key
    api_key = os.environ.get('BREVO_API_KEY')
    if not api_key:
        print("❌ BREVO_API_KEY not found in environment")
        return False
    
    print(f"✅ API Key found: {api_key[:10]}...")
    
    # Check if it looks like a valid Brevo key
    if api_key.startswith('xkeysib-'):
        print("✅ API Key format looks correct (starts with xkeysib-)")
    else:
        print("⚠️  API Key format doesn't match expected Brevo format")
        print("   Expected: xkeysib-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
        print(f"   Found: {api_key}")
        print("   This might be the issue!")
    
    # Test the API key
    print("\n📧 Testing API key with Brevo...")
    
    url = "https://api.brevo.com/v3/account"
    headers = {
        "accept": "application/json",
        "api-key": api_key
    }
    
    try:
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            print("✅ API key is valid!")
            account_info = response.json()
            print(f"   Account: {account_info.get('email', 'N/A')}")
            return True
        elif response.status_code == 401:
            print("❌ API key is invalid or unauthorized")
            print(f"   Error: {response.text}")
            return False
        else:
            print(f"❌ Unexpected response: {response.status_code}")
            print(f"   Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing API key: {e}")
        return False

def test_email_sending():
    """Test sending a simple email"""
    print("\n📤 Testing email sending...")
    print("=" * 50)
    
    api_key = os.environ.get('BREVO_API_KEY')
    if not api_key:
        print("❌ No API key available")
        return False
    
    # Test email
    test_email = input("Enter your email address to test: ").strip()
    if not test_email or '@' not in test_email:
        print("❌ Invalid email address")
        return False
    
    url = "https://api.brevo.com/v3/smtp/email"
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "api-key": api_key
    }
    
    payload = {
        "sender": {
            "name": "Test Sender",
            "email": "test@example.com"
        },
        "to": [
            {
                "email": test_email,
                "name": "Test User"
            }
        ],
        "subject": "Test Email - Brevo API",
        "htmlContent": "<p>This is a test email to verify your Brevo API key is working.</p>"
    }
    
    try:
        print(f"📤 Sending test email to {test_email}...")
        response = requests.post(url, headers=headers, json=payload)
        
        if response.status_code == 201:
            print("✅ Test email sent successfully!")
            print(f"   Response: {response.json()}")
            return True
        else:
            print(f"❌ Failed to send test email: {response.status_code}")
            print(f"   Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error sending test email: {e}")
        return False

def main():
    """Main function"""
    print("🧪 Brevo API Key Test")
    print("=" * 60)
    
    # Test API key
    key_valid = test_brevo_api_key()
    
    if not key_valid:
        print("\n❌ API key test failed.")
        print("\n📝 To fix this:")
        print("1. Go to https://app.brevo.com/settings/keys/api")
        print("2. Generate a new API key (should start with xkeysib-)")
        print("3. Update your .env file with the new key")
        print("4. Run this test again")
        return
    
    # Test email sending
    print("\n" + "=" * 60)
    send_test = input("Would you like to test sending an email? (y/n): ").strip().lower()
    
    if send_test in ['y', 'yes']:
        email_ok = test_email_sending()
        
        if email_ok:
            print("\n🎉 All tests passed! Your Brevo setup is working.")
        else:
            print("\n❌ Email sending test failed.")
    else:
        print("\n✅ API key test passed!")

if __name__ == "__main__":
    main()
