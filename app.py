from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
from config import config

# Get configuration based on environment
config_name = os.environ.get('FLASK_ENV', 'development')
app_config = config[config_name]

app = Flask(__name__)
app.config.from_object(app_config)

# Custom Jinja filter for parsing JSON
@app.template_filter('from_json')
def from_json(value):
    import json
    try:
        return json.loads(value)
    except:
        return []

# Email configuration
if not app_config.BREVO_API_KEY:
    print("Warning: BREVO_API_KEY not set. Email functionality will be disabled.")
    print("To test email functionality locally:")
    print("1. Create a .env file in your project root")
    print("2. Add your Brevo API key: BREVO_API_KEY=your_api_key_here")
    print("3. Get your API key from: https://app.brevo.com/settings/keys/api")

db = SQLAlchemy(app)

# Database Models
class Guest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    guest_count = db.Column(db.Integer, default=1)
    guest_names = db.Column(db.Text)  # JSON string of guest names
    message = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Welcome Lunch
    welcome_lunch = db.Column(db.String(20), nullable=False)  # 'attending', 'not_attending'
    
    # Wedding Day
    wedding_attendance = db.Column(db.String(20), nullable=False)  # 'attending', 'not_attending'
    
    # Accommodation
    accommodation = db.Column(db.String(10), nullable=False)  # 'yes', 'no'
    
    # Farewell Lunch
    farewell_lunch = db.Column(db.String(20), nullable=False)  # 'attending', 'not_attending'
    
    def __repr__(self):
        return f'<Guest {self.name}>'

# Routes
@app.route('/')
def home():
    guests = Guest.query.order_by(Guest.created_at.desc()).all()
    return render_template('index.html', guests=guests)

@app.route('/rsvp')
def rsvp():
    return redirect(url_for('home') + '#rsvp')

@app.route('/faq')
def faq():
    return redirect(url_for('home') + '#faq')

@app.route('/schedule')
def schedule():
    return send_from_directory('materials', 'crystal and yang wedding.png')

@app.route('/submit_rsvp', methods=['POST'])
def submit_rsvp():
    try:
        import json
        
        # Primary contact information
        name = request.form.get('name')
        email = request.form.get('email')
        guest_count = int(request.form.get('guest_count', 1))
        message = request.form.get('message', '')
        
        # Guest names (array from form)
        guest_names_list = request.form.getlist('guest_names[]')
        guest_names_json = json.dumps(guest_names_list)
        
        # Event attendance
        welcome_lunch = request.form.get('welcome_lunch')
        wedding_attendance = request.form.get('wedding_attendance')
        accommodation = request.form.get('accommodation')
        farewell_lunch = request.form.get('farewell_lunch')
        
        # Debug: Print received values
        print(f"Debug - Received form data:")
        print(f"  welcome_lunch: '{welcome_lunch}'")
        print(f"  wedding_attendance: '{wedding_attendance}'")
        print(f"  accommodation: '{accommodation}'")
        print(f"  farewell_lunch: '{farewell_lunch}'")
        
        # Validate required fields
        required_fields = {
            'name': name,
            'email': email,
            'guest_count': guest_count,
            'welcome_lunch': welcome_lunch,
            'wedding_attendance': wedding_attendance,
            'accommodation': accommodation,
            'farewell_lunch': farewell_lunch
        }
        
        missing_fields = [field for field, value in required_fields.items() if not value]
        if missing_fields:
            return jsonify({
                'success': False,
                'message': f'Please fill in all required fields: {", ".join(missing_fields)}'
            }), 400
        
        # Validate guest names match guest count
        # Note: guest_names_list now includes the primary contact name
        if len(guest_names_list) != guest_count:
            return jsonify({
                'success': False,
                'message': f'Please provide names for all {guest_count} guest(s). You provided {len(guest_names_list)} names.'
            }), 400
        
        # Create new guest
        guest = Guest(
            name=name,
            email=email,
            guest_count=guest_count,
            guest_names=guest_names_json,
            message=message,
            welcome_lunch=welcome_lunch,
            wedding_attendance=wedding_attendance,
            accommodation=accommodation,
            farewell_lunch=farewell_lunch
        )
        
        db.session.add(guest)
        db.session.commit()
        
        # Send confirmation email
        email_sent = False
        email_error = None
        try:
            if app_config.BREVO_API_KEY:
                send_confirmation_email(email, name, guest_names_list, welcome_lunch, wedding_attendance, accommodation, farewell_lunch)
                email_sent = True
                print(f"Confirmation email sent successfully to {email}")
            else:
                print("Warning: BREVO_API_KEY not configured. Email not sent.")
                email_error = "Email service not configured"
        except Exception as email_error:
            print(f"Email sending failed: {email_error}")
            # Continue anyway - the RSVP was saved successfully
        
        response_data = {
            'success': True,
            'message': 'RSVP submitted successfully!'
        }
        
        if email_sent:
            response_data['message'] += ' A confirmation email has been sent to your email address.'
        elif email_error:
            response_data['message'] += f' (Note: Email notification failed: {email_error})'
        
        return jsonify(response_data)
        
    except Exception as e:
        print(f"RSVP submission error: {e}")
        return jsonify({
            'success': False,
            'message': 'There was an error submitting your RSVP. Please try again.'
        }), 500

@app.route('/admin')
def admin():
    # Simple admin view - in production, add proper authentication
    guests = Guest.query.order_by(Guest.created_at.desc()).all()
    
    # Calculate statistics
    total_primary_contacts = len(guests)
    total_guests = sum(g.guest_count for g in guests)
    
    # Wedding attendance stats (based on total guest count)
    wedding_attending = sum(g.guest_count for g in guests if g.wedding_attendance == 'attending')
    
    # Event attendance stats (based on total guest count)
    welcome_lunch_attending = sum(g.guest_count for g in guests if g.welcome_lunch == 'attending')
    farewell_lunch_attending = sum(g.guest_count for g in guests if g.farewell_lunch == 'attending')
    
    # Accommodation stats (based on total guest count)
    accommodation_needed = sum(g.guest_count for g in guests if g.accommodation == 'yes')
    
    stats = {
        'total_primary_contacts': total_primary_contacts,
        'total_guests': total_guests,
        'wedding_attending': wedding_attending,
        'welcome_lunch_attending': welcome_lunch_attending,
        'farewell_lunch_attending': farewell_lunch_attending,
        'accommodation_needed': accommodation_needed
    }
    
    return render_template('admin.html', guests=guests, stats=stats)

def send_confirmation_email(email, name, guest_names, welcome_lunch, wedding_attendance, accommodation, farewell_lunch):
    """Send confirmation email using Brevo"""
    try:
        import requests
        
        # Validate email configuration
        api_key = app_config.BREVO_API_KEY
        if not api_key:
            raise ValueError("Brevo API key not configured")
        
        if not app_config.FROM_EMAIL:
            raise ValueError("FROM_EMAIL not configured")
        
        # Validate email format
        if not email or '@' not in email:
            raise ValueError("Invalid email address")
        
        # Format guest names
        guest_names_text = ", ".join(guest_names) if len(guest_names) > 1 else guest_names[0]
        
        # Email content
        subject = "Crystal & Yang's Wedding - RSVP Confirmation"
        html_content = f"""
<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="background:#faf7f2;padding:32px 0;">
  <tr>
    <td align="center">
      <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="600" style="max-width:600px;background:#ffffff;border-radius:14px;border:1px solid #e9e4da;box-shadow:0 1px 6px rgba(0,0,0,0.04);">
        <tr>
          <td style="padding:32px 36px 16px 36px;border-bottom:1px solid #efeae0;">
            <div style="font-family: 'Didot', 'Bodoni MT', Georgia, 'Times New Roman', serif; font-size:28px; line-height:1.2; color:#2b2b2b; text-align:center; letter-spacing:0.5px;">
              Crystal &amp; Yang
            </div>
            <div style="font-family: Arial, Helvetica, sans-serif; font-size:12px; letter-spacing:2px; text-transform:uppercase; color:#8a7e6a; text-align:center; margin-top:6px;">
              Wedding RSVP Confirmation
            </div>
          </td>
        </tr>

        <tr>
          <td style="padding:24px 36px 0 36px;">
            <p style="margin:0 0 10px 0; font-family: Arial, Helvetica, sans-serif; font-size:16px; color:#2b2b2b;">
              Dear <strong>{name}</strong>,
            </p>
            <p style="margin:0 0 18px 0; font-family: Arial, Helvetica, sans-serif; font-size:16px; color:#2b2b2b;">
              Thank you for your RSVP — we can’t wait to celebrate together!
            </p>
          </td>
        </tr>

        <tr>
          <td style="padding:0 36px 0 36px;">
            <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:#f9f7f3;border:1px solid #efeae0;border-radius:10px;">
              <tr>
                <td style="padding:16px 18px;">
                  <div style="font-family: Arial, Helvetica, sans-serif; font-size:12px; color:#8a7e6a; letter-spacing:1.5px; text-transform:uppercase; margin-bottom:6px;">
                    Your RSVP Details
                  </div>
                  <div style="font-family: Arial, Helvetica, sans-serif; font-size:16px; color:#2b2b2b; line-height:1.6;">
                    <div><strong>Guests</strong>: {guest_names_text}</div>
                    <div><strong>Welcome Lunch (May 10)</strong>: {welcome_lunch.replace('_', ' ').title()}</div>
                    <div><strong>Wedding Day (May 12)</strong>: {wedding_attendance.replace('_', ' ').title()}</div>
                    <div><strong>Accommodation</strong>: {accommodation.title()}</div>
                    <div><strong>Farewell Lunch (May 13)</strong>: {farewell_lunch.replace('_', ' ').title()}</div>
                  </div>
                </td>
              </tr>
            </table>
          </td>
        </tr>

        <tr>
          <td style="padding:22px 36px 0 36px;">
            <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="border-collapse:separate;">
              <tr>
                <td style="vertical-align:top; padding:0 0 16px 0;">
                  <div style="font-family: Arial, Helvetica, sans-serif; font-size:12px; color:#8a7e6a; letter-spacing:1.5px; text-transform:uppercase; margin-bottom:6px;">
                    Arrival & Check-In
                  </div>
                  <div style="font-family: Arial, Helvetica, sans-serif; font-size:16px; color:#2b2b2b; line-height:1.6;">
                    Please arrive <em>camera-ready</em> (dressed up & make-up done). Check-in opens from <strong>2:00 PM</strong>, then join us for a welcome toast at <strong>2:30 PM</strong>.
                  </div>
                </td>
              </tr>
              <tr>
                <td style="vertical-align:top; padding:0 0 16px 0;">
                  <div style="font-family: Arial, Helvetica, sans-serif; font-size:12px; color:#8a7e6a; letter-spacing:1.5px; text-transform:uppercase; margin-bottom:6px;">
                    Dress Code
                  </div>
                  <div style="font-family: Arial, Helvetica, sans-serif; font-size:16px; color:#2b2b2b; line-height:1.6;">
                    Black tie for men; pastel long dresses for daytime for women (no white/cream) + optional darker looks in the evening.
                  </div>
                </td>
              </tr>
              <tr>
                <td style="vertical-align:top; padding:0 0 6px 0;">
                  <div style="font-family: Arial, Helvetica, sans-serif; font-size:12px; color:#8a7e6a; letter-spacing:1.5px; text-transform:uppercase; margin-bottom:6px;">
                    Venue
                  </div>
                  <div style="font-family: Arial, Helvetica, sans-serif; font-size:16px; color:#2b2b2b; line-height:1.6;">
                    Hedsor House, Buckinghamshire.  
                    For full details &amp; travel tips, please visit our
                    <a href="https://crystal-yang-wedding.up.railway.app" target="_blank" style="color:#b8a16a; text-decoration:none; font-weight:bold;">
                      wedding website
                    </a>.
                  </div>
                </td>
              </tr>
            </table>
          </td>
        </tr>

        <tr>
          <td style="padding:22px 36px 28px 36px;">
            <div style="height:1px;background:#efeae0;margin:10px 0 18px 0;"></div>
            <p style="margin:0; font-family: Arial, Helvetica, sans-serif; font-size:16px; color:#2b2b2b;">
              If anything changes, just 
              <a href="https://wa.me/14415244044" target="_blank" style="color:#b8a16a; font-weight:bold; text-decoration:none;">
                WhatsApp us
              </a> — do not reply to this email!
            </p>
          </td>
        </tr>

        <tr>
          <td style="padding:0 36px 30px 36px; text-align:center;">
            <div style="font-family: Arial, Helvetica, sans-serif; color:#8a7e6a; font-size:13px;">With love,</div>
            <div style="font-family: 'Didot','Bodoni MT',Georgia,'Times New Roman',serif; font-size:18px; color:#2b2b2b; margin-top:2px;">
              Crystal &amp; Yang
            </div>
            <div style="font-family: Arial, Helvetica, sans-serif; font-size:12px; color:#8a7e6a; margin-top:4px;">
              Hedsor House — May 12, 2026
            </div>
            <div style="margin-top:10px;">
              <a href="https://crystal-yang-wedding.up.railway.app" target="_blank" style="font-family: Arial, Helvetica, sans-serif; font-size:12px; color:#b8a16a; text-decoration:none;">
                Visit our wedding website ↗
              </a>
            </div>
          </td>
        </tr>
      </table>
    </td>
  </tr>
</table>
"""


        
        # Send email using Brevo API
        url = "https://api.brevo.com/v3/smtp/email"
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "api-key": api_key
        }
        
        payload = {
            "sender": {
                "name": "Crystal & Yang Wedding",
                "email": app_config.FROM_EMAIL
            },
            "to": [
                {
                    "email": email,
                    "name": name
                }
            ],
            "subject": subject,
            "htmlContent": html_content
        }
        
        response = requests.post(url, headers=headers, json=payload)
        
        if response.status_code == 201:
            print(f"Email sent successfully to {email}")
            return response.json()
        else:
            raise Exception(f"Brevo API error: {response.status_code} - {response.text}")
        
    except Exception as e:
        print(f"Error sending email to {email}: {e}")
        raise e

# Create database tables
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
