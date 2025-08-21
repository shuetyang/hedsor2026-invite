# Email Service Alternatives for Wedding RSVP System

## Overview
If you're having issues with Resend's sandbox mode restrictions, here are excellent alternatives that offer free tiers and better testing capabilities.

## 🏆 **Top Recommendations**

### 1. **SendGrid** ⭐⭐⭐⭐⭐
**Best for: Reliability and generous free tier**

- **Free Tier**: 100 emails/day (3,000/month)
- **No sandbox restrictions** - can send to any email immediately
- **Excellent deliverability**
- **Easy setup**

**Setup:**
```bash
pip install sendgrid
```

**Configuration:**
```env
SENDGRID_API_KEY=your_sendgrid_api_key
FROM_EMAIL=noreply@yourdomain.com
```

### 2. **Mailgun** ⭐⭐⭐⭐⭐
**Best for: Developer-friendly and good free tier**

- **Free Tier**: 5,000 emails/month for 3 months, then 1,000/month
- **No sandbox restrictions**
- **Great API documentation**
- **Good deliverability**

**Setup:**
```bash
pip install requests
```

**Configuration:**
```env
MAILGUN_API_KEY=your_mailgun_api_key
MAILGUN_DOMAIN=yourdomain.com
FROM_EMAIL=noreply@yourdomain.com
```

### 3. **Brevo (formerly Sendinblue)** ⭐⭐⭐⭐
**Best for: User-friendly interface**

- **Free Tier**: 300 emails/day
- **No sandbox restrictions**
- **Beautiful email templates**
- **Good deliverability**

**Setup:**
```bash
pip install sib-api-v3-sdk
```

**Configuration:**
```env
BREVO_API_KEY=your_brevo_api_key
FROM_EMAIL=noreply@yourdomain.com
```

### 4. **Postmark** ⭐⭐⭐⭐
**Best for: Transactional emails and high deliverability**

- **Free Tier**: 100 emails/month
- **Excellent deliverability**
- **Fast delivery**
- **Great for transactional emails**

**Setup:**
```bash
pip install postmarker
```

**Configuration:**
```env
POSTMARK_API_KEY=your_postmark_api_key
FROM_EMAIL=noreply@yourdomain.com
```

## 🚀 **Quick Implementation Guide**

### Option 1: SendGrid (Recommended)

#### Step 1: Sign Up
1. Go to [SendGrid](https://sendgrid.com)
2. Sign up for a free account
3. Verify your email address

#### Step 2: Get API Key
1. Go to Settings → API Keys
2. Create a new API Key
3. Choose "Restricted Access" → "Mail Send"
4. Copy the API key

#### Step 3: Update Your Code
Replace the email sending function in `app.py`:

```python
import sendgrid
from sendgrid.helpers.mail import Mail

def send_confirmation_email(email, name, guest_names, welcome_lunch, wedding_attendance, accommodation, farewell_lunch):
    """Send confirmation email using SendGrid"""
    try:
        # Validate configuration
        api_key = os.environ.get('SENDGRID_API_KEY')
        from_email = os.environ.get('FROM_EMAIL', 'noreply@yourdomain.com')
        
        if not api_key:
            raise ValueError("SendGrid API key not configured")
        
        # Format guest names
        guest_names_text = ", ".join(guest_names) if len(guest_names) > 1 else guest_names[0]
        
        # Email content
        subject = "Crystal & Yang's Wedding - RSVP Confirmation"
        html_content = f"""
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
            <h2 style="color: #333; text-align: center;">🎉 Wedding RSVP Confirmation</h2>
            
            <div style="background: #f9f9f9; padding: 20px; border-radius: 8px; margin: 20px 0;">
                <p style="font-size: 16px; color: #333;">Dear <strong>{name}</strong>,</p>
                
                <p style="font-size: 16px; color: #333;">Thank you for your RSVP to our wedding celebration!</p>
                
                <div style="background: white; padding: 15px; border-radius: 5px; margin: 15px 0;">
                    <p style="margin: 0; font-size: 14px; color: #666; font-weight: bold;">Your RSVP Details:</p>
                    <p style="margin: 5px 0 0 0; font-size: 16px; color: #333;"><strong>Guests:</strong> {guest_names_text}</p>
                    <p style="margin: 5px 0 0 0; font-size: 16px; color: #333;"><strong>Welcome Lunch (May 10):</strong> {welcome_lunch.replace('_', ' ').title()}</p>
                    <p style="margin: 5px 0 0 0; font-size: 16px; color: #333;"><strong>Wedding Day (May 12):</strong> {wedding_attendance.replace('_', ' ').title()}</p>
                    <p style="margin: 5px 0 0 0; font-size: 16px; color: #333;"><strong>Accommodation:</strong> {accommodation.title()}</p>
                    <p style="margin: 5px 0 0 0; font-size: 16px; color: #333;"><strong>Farewell Lunch (May 13):</strong> {farewell_lunch.replace('_', ' ').title()}</p>
                </div>
                
                <p style="font-size: 16px; color: #333;">We're excited to celebrate with you!</p>
            </div>
            
            <div style="text-align: center; margin-top: 30px; padding-top: 20px; border-top: 1px solid #eee;">
                <p style="color: #666; font-size: 14px;">Best regards,</p>
                <p style="color: #333; font-size: 16px; font-weight: bold;">Crystal & Yang</p>
                <p style="color: #666; font-size: 12px;">Hedsor House Wedding - May 12, 2026</p>
            </div>
        </div>
        """
        
        # Send email using SendGrid
        sg = sendgrid.SendGridAPIClient(api_key=api_key)
        message = Mail(
            from_email=from_email,
            to_emails=email,
            subject=subject,
            html_content=html_content
        )
        
        response = sg.send(message)
        print(f"Email sent successfully to {email}")
        return response
        
    except Exception as e:
        print(f"Error sending email to {email}: {e}")
        raise e
```

#### Step 4: Update Requirements
Add to `requirements.txt`:
```
sendgrid==6.10.0
```

#### Step 5: Update Environment Variables
```env
SENDGRID_API_KEY=your_sendgrid_api_key_here
FROM_EMAIL=noreply@yourdomain.com
```

### Option 2: Mailgun (Alternative)

#### Step 1: Sign Up
1. Go to [Mailgun](https://mailgun.com)
2. Sign up for a free account
3. Verify your email address

#### Step 2: Get API Key
1. Go to Settings → API Keys
2. Copy your Private API Key

#### Step 3: Update Your Code
```python
import requests

def send_confirmation_email(email, name, guest_names, welcome_lunch, wedding_attendance, accommodation, farewell_lunch):
    """Send confirmation email using Mailgun"""
    try:
        # Validate configuration
        api_key = os.environ.get('MAILGUN_API_KEY')
        domain = os.environ.get('MAILGUN_DOMAIN')
        from_email = os.environ.get('FROM_EMAIL', f'noreply@{domain}')
        
        if not api_key or not domain:
            raise ValueError("Mailgun API key or domain not configured")
        
        # Format guest names
        guest_names_text = ", ".join(guest_names) if len(guest_names) > 1 else guest_names[0]
        
        # Email content
        subject = "Crystal & Yang's Wedding - RSVP Confirmation"
        html_content = f"""
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
            <h2 style="color: #333; text-align: center;">🎉 Wedding RSVP Confirmation</h2>
            
            <div style="background: #f9f9f9; padding: 20px; border-radius: 8px; margin: 20px 0;">
                <p style="font-size: 16px; color: #333;">Dear <strong>{name}</strong>,</p>
                
                <p style="font-size: 16px; color: #333;">Thank you for your RSVP to our wedding celebration!</p>
                
                <div style="background: white; padding: 15px; border-radius: 5px; margin: 15px 0;">
                    <p style="margin: 0; font-size: 14px; color: #666; font-weight: bold;">Your RSVP Details:</p>
                    <p style="margin: 5px 0 0 0; font-size: 16px; color: #333;"><strong>Guests:</strong> {guest_names_text}</p>
                    <p style="margin: 5px 0 0 0; font-size: 16px; color: #333;"><strong>Welcome Lunch (May 10):</strong> {welcome_lunch.replace('_', ' ').title()}</p>
                    <p style="margin: 5px 0 0 0; font-size: 16px; color: #333;"><strong>Wedding Day (May 12):</strong> {wedding_attendance.replace('_', ' ').title()}</p>
                    <p style="margin: 5px 0 0 0; font-size: 16px; color: #333;"><strong>Accommodation:</strong> {accommodation.title()}</p>
                    <p style="margin: 5px 0 0 0; font-size: 16px; color: #333;"><strong>Farewell Lunch (May 13):</strong> {farewell_lunch.replace('_', ' ').title()}</p>
                </div>
                
                <p style="font-size: 16px; color: #333;">We're excited to celebrate with you!</p>
            </div>
            
            <div style="text-align: center; margin-top: 30px; padding-top: 20px; border-top: 1px solid #eee;">
                <p style="color: #666; font-size: 14px;">Best regards,</p>
                <p style="color: #333; font-size: 16px; font-weight: bold;">Crystal & Yang</p>
                <p style="color: #666; font-size: 12px;">Hedsor House Wedding - May 12, 2026</p>
            </div>
        </div>
        """
        
        # Send email using Mailgun
        response = requests.post(
            f"https://api.mailgun.net/v3/{domain}/messages",
            auth=("api", api_key),
            data={
                "from": from_email,
                "to": email,
                "subject": subject,
                "html": html_content
            }
        )
        
        if response.status_code == 200:
            print(f"Email sent successfully to {email}")
            return response.json()
        else:
            raise Exception(f"Mailgun API error: {response.text}")
        
    except Exception as e:
        print(f"Error sending email to {email}: {e}")
        raise e
```

## 📊 **Comparison Table**

| Service | Free Tier | Sandbox Restrictions | Setup Difficulty | Deliverability |
|---------|-----------|---------------------|------------------|----------------|
| **SendGrid** | 100/day | ❌ None | ⭐⭐ Easy | ⭐⭐⭐⭐⭐ Excellent |
| **Mailgun** | 5K/month (3mo) | ❌ None | ⭐⭐⭐ Medium | ⭐⭐⭐⭐ Good |
| **Brevo** | 300/day | ❌ None | ⭐⭐ Easy | ⭐⭐⭐⭐ Good |
| **Postmark** | 100/month | ❌ None | ⭐⭐⭐ Medium | ⭐⭐⭐⭐⭐ Excellent |
| **Resend** | 3K/month | ✅ Sandbox mode | ⭐⭐ Easy | ⭐⭐⭐⭐ Good |

## 🎯 **Recommendation**

For your wedding RSVP system, I recommend **SendGrid** because:
- ✅ **No sandbox restrictions** - can send to any email immediately
- ✅ **Generous free tier** - 100 emails/day is perfect for wedding RSVPs
- ✅ **Excellent deliverability** - emails won't go to spam
- ✅ **Easy setup** - simple API and good documentation
- ✅ **Reliable** - used by many major companies

## 🚀 **Quick Migration**

To switch from Resend to SendGrid:

1. **Sign up for SendGrid** (free)
2. **Get your API key**
3. **Update your `.env` file**:
   ```env
   SENDGRID_API_KEY=your_sendgrid_api_key
   FROM_EMAIL=noreply@yourdomain.com
   ```
4. **Replace the email function** in `app.py` (see code above)
5. **Add SendGrid to requirements.txt**:
   ```
   sendgrid==6.10.0
   ```
6. **Test with any email address** - no restrictions!

Would you like me to help you implement one of these alternatives?
