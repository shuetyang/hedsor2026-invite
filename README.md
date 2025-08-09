# Wedding Invitation Website

A beautiful, elegant wedding invitation website built with Flask, featuring RSVP functionality, email confirmations, and admin management.

## Features

- **Elegant Design**: Sophisticated wedding-themed styling with responsive design
- **RSVP System**: Complete guest response management with form validation
- **Email Confirmations**: Automatic email confirmations using SendGrid
- **Admin Dashboard**: View and manage RSVP submissions with statistics
- **FAQ Section**: Comprehensive answers to common wedding questions
- **Mobile Responsive**: Works perfectly on all devices
- **Database Storage**: SQLite database for guest information
- **Export Functionality**: Export guest list to CSV

## Tech Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, JavaScript
- **Database**: SQLite (can be upgraded to PostgreSQL)
- **Email Service**: SendGrid
- **Hosting**: Render.com (free tier)
- **Domain**: Freenom (.tk, .ml domains)

## Project Structure

```
wedding-invitation/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── Procfile              # Render deployment configuration
├── env_example.txt       # Environment variables template
├── README.md             # This file
├── templates/            # HTML templates
│   ├── base.html         # Base template
│   ├── index.html        # Home page
│   ├── rsvp.html         # RSVP form
│   ├── faq.html          # FAQ page
│   └── admin.html        # Admin dashboard
├── static/               # Static files
│   ├── css/
│   │   └── style.css     # Main stylesheet
│   ├── js/
│   │   └── script.js     # JavaScript functionality
│   └── images/
│       └── frontpage.jpg # Wedding invitation design
└── venv/                 # Python virtual environment
```

## Local Development Setup

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd wedding-invitation
   ```

2. **Create and activate virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp env_example.txt .env
   # Edit .env with your actual values
   ```

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Access the website**
   - Home: http://localhost:5000
   - RSVP: http://localhost:5000/rsvp
   - FAQ: http://localhost:5000/faq
   - Admin: http://localhost:5000/admin

## Deployment to Render

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Initial wedding invitation website"
   git push origin main
   ```

2. **Create Render Account**
   - Go to [render.com](https://render.com)
   - Sign up with your GitHub account

3. **Deploy Web Service**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Configure settings:
     - **Name**: your-wedding-website
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `gunicorn app:app`
     - **Plan**: Free

4. **Set Environment Variables**
   In Render dashboard, go to Environment → Environment Variables:
   ```
   SECRET_KEY=your-secret-key-here
   SENDGRID_API_KEY=your-sendgrid-api-key
   FROM_EMAIL=noreply@yourwedding.com
   ```

5. **Deploy**
   - Click "Create Web Service"
   - Render will automatically deploy your application

## SendGrid Email Setup

1. **Create SendGrid Account**
   - Go to [sendgrid.com](https://sendgrid.com)
   - Sign up for free account (100 emails/day)

2. **Get API Key**
   - Go to Settings → API Keys
   - Create new API Key with "Mail Send" permissions
   - Copy the API key

3. **Verify Sender**
   - Go to Settings → Sender Authentication
   - Verify your domain or single sender email

4. **Add to Environment Variables**
   ```
   SENDGRID_API_KEY=your-api-key-here
   FROM_EMAIL=your-verified-email@domain.com
   ```

## Custom Domain Setup (Optional)

1. **Get Free Domain**
   - Go to [freenom.com](https://freenom.com)
   - Register a free .tk, .ml, .ga, .cf, or .gq domain

2. **Configure DNS**
   - Add CNAME record pointing to your Render URL
   - Or use Render's custom domain feature

3. **Update Environment**
   ```
   CUSTOM_DOMAIN=yourwedding.tk
   ```

## Customization

### Update Wedding Details
Edit `templates/index.html` to change:
- Couple names
- Wedding date and time
- Venue information
- Reception details

### Modify Styling
Edit `static/css/style.css` to customize:
- Colors (primary: #8B7355, accent: #D4AF37)
- Fonts (Playfair Display, Montserrat)
- Layout and spacing

### Add Features
- Photo gallery
- Guest book
- Wedding countdown
- Music player
- Interactive elements

## Admin Features

- **View RSVPs**: See all guest responses in real-time
- **Statistics**: Track attendance numbers
- **Export Data**: Download guest list as CSV
- **Print List**: Print-friendly guest list

## Security Considerations

- Change default SECRET_KEY
- Use HTTPS in production
- Validate all form inputs
- Sanitize user data
- Regular security updates

## Support

For issues or questions:
1. Check the FAQ section
2. Review the code comments
3. Check Flask and SendGrid documentation
4. Contact the development team

## License

This project is created for personal wedding use. Feel free to modify and use for your own wedding!

---

**Made with ❤️ for your special day**
