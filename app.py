from flask import Flask, request, render_template, redirect, url_for, flash, send_file
from flask_sqlalchemy import SQLAlchemy
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os
from xhtml2pdf import pisa
import io

app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = 'sdubvsrgusyfaiucefbgowuegbiuwcgbefo'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///persons.db'
app.config['UPLOAD_FOLDER'] = 'static/uploads'

db = SQLAlchemy(app)

# Database model
class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    phone = db.Column(db.String(15), nullable=False)
    picture = db.Column(db.String(300), nullable=True)  # Image URL
    bio = db.Column(db.Text, nullable=False)
    skills = db.Column(db.Text, nullable=False)
    links = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"<Person {self.first_name} {self.last_name}>"

# Create the database and tables
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    persons = Person.query.all()  # Fetch all persons from the database
    return render_template('index.html', persons=persons)

@app.route('/create-portfolio', methods=['GET', 'POST'])
def create_portfolio():
    if request.method == 'POST':
        first_name = request.form['firstName']
        last_name = request.form['lastName']
        email = request.form['email']
        phone = request.form['phone']
        bio = request.form['bio']
        skills = request.form['skills']
        links = request.form['links']

        # Handling image upload
        picture = None
        if 'picture' in request.files:
            file = request.files['picture']
            if file.filename != '':
                picture_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
                file.save(picture_path)
                picture = picture_path

        # Create a new person object
        new_person = Person(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            bio=bio,
            skills=skills,
            links=links,
            picture=picture
        )

        # Add to database
        db.session.add(new_person)
        db.session.commit()
        
        flash('Portfolio created successfully!', 'success')
        return redirect(url_for('portfolio', id=new_person.id))

    return render_template('create-portfolio.html')

@app.route('/view-portfolio/<int:id>')
def portfolio(id):
    person = Person.query.get_or_404(id)
    return render_template('view-portfolio.html', person=person)

@app.route('/download/<int:id>')
def download(id):
    person = Person.query.get_or_404(id)

    # Send the PDF file to the user for download
    return render_template('download-pdf.html', person=person)

@app.route('/download-portfolio/<int:id>')
def download_portfolio(id):
    person = Person.query.get_or_404(id)

    # Render the HTML template to a string
    html = render_template('portfolio-pdf.html', person=person)

    # Create a byte stream buffer to hold the PDF data
    buffer = io.BytesIO()

    # Use xhtml2pdf to convert the HTML to PDF
    pisa_status = pisa.CreatePDF(
        html, dest=buffer
    )

    # If PDF creation fails, handle the error
    if pisa_status.err:
        return f"Error: {pisa_status.err}"

    buffer.seek(0)

    # Send the PDF file to the user for download
    return send_file(buffer, as_attachment=True, download_name=f"{person.first_name}_portfolio.pdf", mimetype='application/pdf')

if __name__ == '__main__':
    app.run(debug=True)
