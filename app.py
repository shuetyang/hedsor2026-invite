from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
from dotenv import load_dotenv
import resend

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
if not app.config['SECRET_KEY']:
    print("Warning: SECRET_KEY not set. Using default for development only.")
    app.config['SECRET_KEY'] = 'dev-secret-key-change-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///wedding.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Email configuration
resend.api_key = os.environ.get('RESEND_API_KEY')
if not resend.api_key:
    print("Warning: RESEND_API_KEY not set. Email functionality will be disabled.")

db = SQLAlchemy(app)

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
        
        # Validate required fields
        if not name or not email or not rsvp_status:
            return jsonify({
                'success': False,
                'message': 'Please fill in all required fields.'
            }), 400
        
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
        
        # Try to send confirmation email (but don't fail if it doesn't work)
        try:
            send_confirmation_email(email, name, rsvp_status)
        except Exception as email_error:
            print(f"Email sending failed: {email_error}")
            # Continue anyway - the RSVP was saved successfully
        
        return jsonify({
            'success': True,
            'message': 'RSVP submitted successfully!'
        })
        
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
    stats = {
        'total': len(guests),
        'attending': len([g for g in guests if g.rsvp_status == 'attending']),
        'not_attending': len([g for g in guests if g.rsvp_status == 'not_attending']),
        'maybe': len([g for g in guests if g.rsvp_status == 'maybe'])
    }
    return render_template('admin.html', guests=guests, stats=stats)

def send_confirmation_email(email, name, rsvp_status):
    """Send confirmation email using Resend"""
    try:
        # Email content
        subject = "Wedding RSVP Confirmation"
        html_content = f"""
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
            <h2 style="color: #333; text-align: center;">🎉 Wedding RSVP Confirmation</h2>
            
            <div style="background: #f9f9f9; padding: 20px; border-radius: 8px; margin: 20px 0;">
                <p style="font-size: 16px; color: #333;">Dear <strong>{name}</strong>,</p>
                
                <p style="font-size: 16px; color: #333;">Thank you for your RSVP to our wedding!</p>
                
                <div style="background: white; padding: 15px; border-radius: 5px; margin: 15px 0;">
                    <p style="margin: 0; font-size: 14px; color: #666;">Your response:</p>
                    <p style="margin: 5px 0 0 0; font-size: 18px; font-weight: bold; color: #333;">
                        {rsvp_status.replace('_', ' ').title()}
                    </p>
                </div>
                
                <p style="font-size: 16px; color: #333;">We're excited to celebrate with you!</p>
            </div>
            
            <div style="text-align: center; margin-top: 30px; padding-top: 20px; border-top: 1px solid #eee;">
                <p style="color: #666; font-size: 14px;">Best regards,</p>
                <p style="color: #333; font-size: 16px; font-weight: bold;">Sarah & Michael</p>
                <p style="color: #666; font-size: 12px;">Hedsor House Wedding</p>
            </div>
        </div>
        """
        
        # Send email using Resend
        from_email = os.environ.get('FROM_EMAIL', 'onboarding@resend.dev')
        response = resend.Emails.send({
            "from": from_email,
            "to": email,
            "subject": subject,
            "html": html_content
        })
        
        print(f"Email sent to {email}: {response}")
        
    except Exception as e:
        print(f"Error sending email: {e}")
        raise e

# Create database tables
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
