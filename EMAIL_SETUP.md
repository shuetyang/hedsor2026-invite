# Email Setup Guide for Crystal & Yang Wedding RSVP System

## Overview
The RSVP system uses [Resend](https://resend.com) to send confirmation emails when guests submit their RSVPs. This guide will help you set up and troubleshoot the email functionality.

## Quick Setup

### 1. Get a Resend API Key
1. Go to [https://resend.com](https://resend.com)
2. Sign up for a free account
3. Navigate to the API Keys section
4. Create a new API key
5. Copy the API key (starts with `re_`)

### 2. Configure Environment Variables
Create a `.env` file in your project root with the following content:

```env
# Flask Configuration
SECRET_KEY=your-secret-key-change-this-in-production
FLASK_ENV=production

# Database Configuration
DATABASE_URL=sqlite:///wedding.db

# Resend Email Configuration
RESEND_API_KEY=re_your_actual_api_key_here
FROM_EMAIL=noreply@yourwedding.com

# Optional: Custom domain
CUSTOM_DOMAIN=yourwedding.tk
```

### 3. Test Your Email Configuration
Run the test script to verify everything is working:

```bash
python test_email.py
```

This script will:
- Check if your `.env` file exists
- Verify your API key is configured
- Optionally send a test email to verify functionality

## Important: Resend Sandbox Mode

### 🚨 **Sandbox Mode Limitation**
When you first sign up for Resend, your account is in **sandbox mode**. This means:
- You can **only send emails to verified email addresses**
- Usually, this is just **your own email address** that you used to sign up
- You **cannot send emails to other people** (like your wedding guests)

### ✅ **How to Get Out of Sandbox Mode**

#### Option 1: Verify Your Domain (Recommended)
1. **Add your domain** to Resend:
   - Go to Resend Dashboard → Domains
   - Click "Add Domain"
   - Enter your domain (e.g., `yourwedding.com`)
   
2. **Verify your domain**:
   - Add the required DNS records (SPF, DKIM, MX)
   - Wait for verification (usually 24-48 hours)
   
3. **Use your domain email**:
   - Update your `FROM_EMAIL` to use your domain: `noreply@yourwedding.com`
   - You can now send to any email address

#### Option 2: Use Resend's Verified Domains (Quick Fix)
1. **Use Resend's default domain**:
   - Keep `FROM_EMAIL=onboarding@resend.dev` (default)
   - Add your email as a verified recipient
   
2. **Add verified recipients**:
   - Go to Resend Dashboard → Settings → Verified Recipients
   - Add email addresses you want to send to
   - **Note**: You'll need to add each guest's email individually

#### Option 3: Upgrade to Paid Plan
- Resend's paid plans remove sandbox restrictions
- Starts at $20/month for 50,000 emails
- Good for high-volume wedding RSVPs

### 🧪 **Testing in Sandbox Mode**
If you're still in sandbox mode, you can test by:
1. Adding your test email addresses as verified recipients
2. Using only those emails for testing
3. Updating your `FROM_EMAIL` to use a verified domain

## Troubleshooting

### Common Issues

#### 1. "Email service not configured"
**Cause**: Missing or invalid `RESEND_API_KEY`
**Solution**: 
- Check that your `.env` file exists and contains the correct API key
- Verify the API key starts with `re_`
- Make sure there are no extra spaces or quotes around the API key

#### 2. "Invalid email address"
**Cause**: The email address format is incorrect
**Solution**: 
- Ensure the email contains an `@` symbol
- Check for typos in the email address

#### 3. "Error sending email" - Sandbox Mode Error
**Cause**: Trying to send to unverified email addresses in sandbox mode
**Solutions**:
- Add recipient emails as verified recipients in Resend dashboard
- Verify your domain and use domain emails
- Upgrade to a paid Resend plan

#### 4. "Error sending email"
**Cause**: Various API or network issues
**Solutions**:
- Check your internet connection
- Verify your Resend account has available credits
- Check the Resend dashboard for any account issues
- Ensure your `FROM_EMAIL` is verified in Resend

#### 5. Emails going to spam
**Solutions**:
- Use a verified domain for your `FROM_EMAIL`
- Add SPF and DKIM records to your domain
- Consider using a custom domain with Resend

### Debugging Steps

1. **Check the console output** when submitting an RSVP
2. **Run the test script** to isolate email issues
3. **Check Resend dashboard** for delivery status
4. **Verify environment variables** are loaded correctly
5. **Check if you're in sandbox mode** and add verified recipients

### Testing Locally

To test email functionality locally:

1. Set `FLASK_ENV=development` in your `.env` file
2. Run the Flask app: `python app.py`
3. Submit a test RSVP
4. Check the console for email status messages

## Email Template

The confirmation email includes:
- Personalized greeting with guest name
- Complete RSVP details (all events and accommodation)
- Professional styling
- Contact information

## Production Deployment

For production deployment:

1. **Use environment variables** instead of `.env` file
2. **Set up a custom domain** for better deliverability
3. **Monitor email delivery** through Resend dashboard
4. **Set up webhooks** for delivery tracking (optional)

## Support

If you continue to have issues:

1. Check the [Resend documentation](https://resend.com/docs)
2. Verify your API key is active in the Resend dashboard
3. Test with the provided `test_email.py` script
4. Check the Flask application logs for detailed error messages

## Security Notes

- Never commit your `.env` file to version control
- Keep your API key secure and rotate it regularly
- Use environment variables in production
- Consider rate limiting for RSVP submissions
