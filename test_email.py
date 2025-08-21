#!/usr/bin/env python3
"""
Test script to verify email configuration and functionality
Run this script to test if your email setup is working correctly.
"""

import os
import sys
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_email_config():
    """Test email configuration"""
    print("🔍 Testing Email Configuration...")
    print("=" * 50)
    
    # Check if .env file exists
    if os.path.exists('.env'):
        print("✅ .env file found")
    else:
        print("❌ .env file not found")
        print("   Create a .env file with your email configuration")
        return False
    
    # Check BREVO_API_KEY
    api_key = os.environ.get('BREVO_API_KEY')
    if api_key:
        print(f"✅ BREVO_API_KEY found: {api_key[:10]}...")
    else:
        print("❌ BREVO_API_KEY not found")
        print("   Add BREVO_API_KEY=your_api_key to your .env file")
        return False
    
    # Check FROM_EMAIL
    from_email = os.environ.get('FROM_EMAIL', 'onboarding@resend.dev')
    print(f"✅ FROM_EMAIL: {from_email}")
    
    # Check if using default domain
    if from_email == 'noreply@yourdomain.com':
        print("⚠️  Using default domain - consider updating to your actual domain")
        print("   This will improve email deliverability")
    
    return True

def test_email_sending():
    """Test sending a test email"""
    print("\n📧 Testing Email Sending...")
    print("=" * 50)
    
    try:
        # Set up Brevo
        api_key = os.environ.get('BREVO_API_KEY')
        if not api_key:
            print("❌ No API key available")
            return False
        
        # Test email parameters
        from_email = os.environ.get('FROM_EMAIL', 'noreply@yourdomain.com')
        test_email = input("Enter your email address to send a test email: ").strip()
        
        if not test_email or '@' not in test_email:
            print("❌ Invalid email address")
            return False
        
        # Check if using default domain
        if from_email == 'noreply@yourdomain.com':
            print("⚠️  Warning: Using default domain")
            print("   Consider updating to your actual domain for better deliverability")
        
        # Send test email
        print(f"📤 Sending test email to {test_email}...")
        
        url = "https://api.brevo.com/v3/smtp/email"
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "api-key": api_key
        }
        
        payload = {
            "sender": {
                "name": "Crystal & Yang Wedding",
                "email": from_email
            },
            "to": [
                {
                    "email": test_email,
                    "name": "Test User"
                }
            ],
            "subject": "Test Email - Crystal & Yang Wedding RSVP System",
            "htmlContent": f"""
            <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
                <h2 style="color: #333; text-align: center;">🧪 Email Test Successful!</h2>
                
                <div style="background: #f9f9f9; padding: 20px; border-radius: 8px; margin: 20px 0;">
                    <p style="font-size: 16px; color: #333;">Hello!</p>
                    
                    <p style="font-size: 16px; color: #333;">This is a test email to verify that your Brevo email configuration is working correctly for the Crystal & Yang Wedding RSVP system.</p>
                    
                    <div style="background: white; padding: 15px; border-radius: 5px; margin: 15px 0;">
                        <p style="margin: 0; font-size: 14px; color: #666; font-weight: bold;">Test Details:</p>
                        <p style="margin: 5px 0 0 0; font-size: 16px; color: #333;"><strong>From:</strong> {from_email}</p>
                        <p style="margin: 5px 0 0 0; font-size: 16px; color: #333;"><strong>To:</strong> {test_email}</p>
                        <p style="margin: 5px 0 0 0; font-size: 16px; color: #333;"><strong>Status:</strong> ✅ Working</p>
                    </div>
                    
                    <p style="font-size: 16px; color: #333;">Your Brevo email system is now ready to send RSVP confirmations!</p>
                </div>
                
                <div style="text-align: center; margin-top: 30px; padding-top: 20px; border-top: 1px solid #eee;">
                    <p style="color: #666; font-size: 14px;">Best regards,</p>
                    <p style="color: #333; font-size: 16px; font-weight: bold;">Crystal & Yang Wedding System</p>
                </div>
            </div>
            """
        }
        
        response = requests.post(url, headers=headers, json=payload)
        
        if response.status_code == 201:
            print(f"✅ Test email sent successfully!")
            print(f"   Response: {response.json()}")
            return True
        else:
            print(f"❌ Error sending test email: {response.status_code} - {response.text}")
            return False
        
    except Exception as e:
        print(f"❌ Error sending test email: {e}")
        return False

def main():
    """Main test function"""
    print("🧪 Crystal & Yang Wedding - Email Configuration Test")
    print("=" * 60)
    
    # Test configuration
    config_ok = test_email_config()
    
    if not config_ok:
        print("\n❌ Configuration test failed. Please fix the issues above.")
        print("\n📝 To set up email functionality:")
        print("1. Create a .env file in your project root")
        print("2. Add your Brevo API key: BREVO_API_KEY=your_api_key_here")
        print("3. Optionally set FROM_EMAIL=your_email@domain.com")
        print("4. Get your API key from: https://app.brevo.com/settings/keys/api")
        return
    
    # Test email sending
    print("\n" + "=" * 60)
    send_test = input("Would you like to send a test email? (y/n): ").strip().lower()
    
    if send_test in ['y', 'yes']:
        email_ok = test_email_sending()
        
        if email_ok:
            print("\n🎉 All tests passed! Your email system is ready.")
        else:
            print("\n❌ Email sending test failed. Check your API key and configuration.")
    else:
        print("\n✅ Configuration test passed! Email system is configured.")

if __name__ == "__main__":
    main()
