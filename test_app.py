import pytest
from app import app, db, Person
from flask import url_for

@pytest.fixture
def client():
    """
    Pytest fixture to configure the Flask app and create
    an in-memory database for testing.
    """
    # Override config for testing
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['WTF_CSRF_ENABLED'] = False  # If you have CSRF, you can disable it for testing
    
    # Create app context, initialize the DB
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        
        # Teardown: drop all tables
        with app.app_context():
            db.drop_all()


def test_index_route(client):
    """
    Test the index route (GET /).
    """
    response = client.get('/')
    assert response.status_code == 200
    assert b"<title>" in response.data  # or any other content check


def test_create_portfolio_get(client):
    """
    Test the GET /create-portfolio to ensure it returns 200.
    """
    response = client.get('/create-portfolio')
    assert response.status_code == 200
    assert b"Create Portfolio" in response.data  # e.g. some form text

def test_portfolio_route(client):
    """
    Test viewing the portfolio page /view-portfolio/<id>.
    """
    # First, create a dummy Person in the test DB
    with app.app_context():
        new_person = Person(
            first_name='Jane',
            last_name='Smith',
            email='jane@smith.com',
            phone='9876543210',
            bio='Some bio',
            skills='HTML, CSS',
            links='https://linkedin.com/in/janesmith'
        )
        db.session.add(new_person)
        db.session.commit()
        person_id = new_person.id

    response = client.get(f'/view-portfolio/{person_id}')
    assert response.status_code == 200
    assert b"Jane" in response.data
    assert b"Smith" in response.data
    assert b"jane@smith.com" in response.data


def test_download_route(client):
    """
    Test the /download/<id> route. 
    It should return a valid HTML page (download-pdf.html) or a 404 if not found.
    """
    # Create a dummy Person
    with app.app_context():
        new_person = Person(
            first_name='Alex',
            last_name='Brown',
            email='alex@brown.com',
            phone='5555555555',
            bio='Data Scientist',
            skills='Machine Learning, Python',
            links='https://github.com/alexbrown'
        )
        db.session.add(new_person)
        db.session.commit()
        person_id = new_person.id

    # Test valid ID
    response = client.get(f'/download/{person_id}')
    assert response.status_code == 200
    assert b"Download PDF" in response.data  # or any unique text from 'download-pdf.html'


def test_download_portfolio_route(client):
    """
    Test the /download-portfolio/<id> route which generates a PDF.
    We'll just check that it returns a 200 status and PDF content type.
    """
    # Create a dummy Person
    with app.app_context():
        new_person = Person(
            first_name='Sam',
            last_name='Green',
            email='sam@green.com',
            phone='4444444444',
            bio='Web Developer',
            skills='Django, React',
            links='https://linkedin.com/in/samgreen'
        )
        db.session.add(new_person)
        db.session.commit()
        person_id = new_person.id

    # Test PDF download
    response = client.get(f'/download-portfolio/{person_id}')
    assert response.status_code == 200
    
    # You can check the content type or content disposition
    # e.g. response.headers.get("Content-Type") == "application/pdf"
    assert b"%PDF" in response.data[:10]  # a quick check for PDF signature if the PDF generated is immediate
