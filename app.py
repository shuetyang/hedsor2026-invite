from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from datetime import datetime
import os
from dotenv import load_dotenv
import sendgrid
from sendgrid.helpers.mail import Mail as SendGridMail

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-change-this')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///wedding.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Email configuration
app.config['MAIL_SERVER'] = 'smtp.sendgrid.net'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'apikey'
app.config['MAIL_PASSWORD'] = os.environ.get('SENDGRID_API_KEY')

db = SQLAlchemy(app)
mail = Mail(app)

# Database Models
class Guest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    rsvp_status = db.Column(db.String(20), nullable=False)  # 'attending', 'not_attending', 'maybe'
    guest_count = db.Column(db.Integer, default=1)
    dietary_restrictions = db.Column(db.Text)
    message = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
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

@app.route('/submit_rsvp', methods=['POST'])
def submit_rsvp():
    try:
        name = request.form.get('name')
        email = request.form.get('email')
        rsvp_status = request.form.get('rsvp_status')
        guest_count = int(request.form.get('guest_count', 1))
        dietary_restrictions = request.form.get('dietary_restrictions', '')
        message = request.form.get('message', '')
        
        # Create new guest
        guest = Guest(
            name=name,
            email=email,
            rsvp_status=rsvp_status,
            guest_count=guest_count,
            dietary_restrictions=dietary_restrictions,
            message=message
        )
        
        db.session.add(guest)
        db.session.commit()
        
        # Send confirmation email
        send_confirmation_email(email, name, rsvp_status)
        
        flash('Thank you for your RSVP! You will receive a confirmation email shortly.', 'success')
        return redirect(url_for('home') + '#rsvp')
        
    except Exception as e:
        flash('There was an error submitting your RSVP. Please try again.', 'error')
        return redirect(url_for('home') + '#rsvp')

@app.route('/admin')
def admin():
    # Simple admin view - in production, add proper authentication
    guests = Guest.query.order_by(Guest.created_at.desc()).all()
    stats = {
        'total': len(guests),
        'attending': len([g for g in guests if g.rsvp_status == 'attending']),
        'not_attending': len([g for g in guests if g.rsvp_status == 'not_attending']),
        'maybe': len([g for g in guests if g.rsvp_status == 'maybe'])
    }
    return render_template('admin.html', guests=guests, stats=stats)

def send_confirmation_email(email, name, rsvp_status):
    """Send confirmation email using SendGrid"""
    try:
        sg = sendgrid.SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY'))
        
        # Email content
        subject = "Wedding RSVP Confirmation"
        content = f"""
        Dear {name},
        
        Thank you for your RSVP to our wedding!
        
        Your response: {rsvp_status.title()}
        
        We're excited to celebrate with you!
        
        Best regards,
        The Happy Couple
        """
        
        message = SendGridMail(
            from_email=os.environ.get('FROM_EMAIL', 'noreply@yourwedding.com'),
            to_emails=email,
            subject=subject,
            plain_text_content=content
        )
        
        response = sg.send(message)
        print(f"Email sent to {email}: {response.status_code}")
        
    except Exception as e:
        print(f"Error sending email: {e}")

# Create database tables
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
