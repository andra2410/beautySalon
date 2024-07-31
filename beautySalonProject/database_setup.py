from sqlalchemy import create_engine, Column, Integer, String, Enum, Date, Time, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker, declarative_base
from sqlalchemy.orm import joinedload

# Define the base class for declarative models
Base = declarative_base()


# Define the User model
class User(Base):
    __tablename__ = 'Users'
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)


# Define the Service model
class Service(Base):
    __tablename__ = 'Services'
    service_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    category = Column(Enum('nails', 'hair', 'cosmetics'), nullable=False)


# Define the Artist model
class Artist(Base):
    __tablename__ = 'Artists'
    artist_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    specialization = Column(Enum('nails', 'hair', 'cosmetics'), nullable=False)


# Define the Appointment model
class Appointment(Base):
    __tablename__ = 'Appointments'
    appointment_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('Users.user_id'))
    artist_id = Column(Integer, ForeignKey('Artists.artist_id'))
    service_id = Column(Integer, ForeignKey('Services.service_id'))
    appointment_date = Column(Date)
    appointment_time = Column(Time)

    user = relationship('User')
    artist = relationship('Artist')
    service = relationship('Service')


# Define the Availability model
class Availability(Base):
    __tablename__ = 'Availability'
    availability_id = Column(Integer, primary_key=True, autoincrement=True)
    artist_id = Column(Integer, ForeignKey('Artists.artist_id'))
    available_date = Column(Date)
    available_time = Column(Time)

    artist = relationship('Artist')


# Define the SQLite database URL
DATABASE_URL = 'sqlite:///./beauty_salon.db'

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Create a session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    """Create database tables."""
    Base.metadata.create_all(bind=engine)


def delete_all_users():
    db = SessionLocal()
    try:
        db.query(User).delete()
        db.commit()
        print("All users deleted successfully.")
    except Exception as e:
        db.rollback()
        print(f"An error occurred: {e}")
    finally:
        db.close()

def delete_all_data():
    db = SessionLocal()
    try:
        # Delete all data from appointments
        db.query(Appointment).delete()
        # Delete all data from users
        db.query(User).delete()
        db.commit()
        print("All appointments and users deleted successfully.")
    except Exception as e:
        db.rollback()
        print(f"An error occurred: {e}")
    finally:
        db.close()

def populate_db():
    """Populate the database with initial data."""
    db = SessionLocal()

    # Add services
    services = [
        ('Manichiura Semipermanentă', 'nails'),
        ('Manichiura Gel', 'nails'),
        ('Manichiura Simplă', 'nails'),
        ('Întreținere Manichiură', 'nails'),
        ('Pedichiură Semipermanentă', 'nails'),
        ('Întreținere Pedichiură', 'nails'),
        ('Manichiură și Pedichiură Simplă', 'nails'),
        ('Manichiură și Pedichiură Semipermanentă', 'nails'),
        ('Manichiură Gel și Pedichiură Simplă', 'nails'),
        ('Manichiură Gel și Pedichiură Semipermanentă', 'nails'),
        ('Tuns Păr Lung', 'hair'),
        ('Tuns Păr Scurt', 'hair'),
        ('Tuns Păr Mediu', 'hair'),
        # ('Coafat', 'hair'),
        ('Tuns Păr Lung + Coafat', 'hair'),
        ('Tuns Păr Scurt + Coafat', 'hair'),
        ('Tuns Păr Mediu + Coafat', 'hair'),
        ('Vopsit Păr Lung', 'hair'),
        ('Vopsit Păr Scurt', 'hair'),
        ('Vopsit Păr Mediu', 'hair'),
        ('Decolorare Păr Scurt', 'hair'),
        ('Decolorare Păr Lung', 'hair'),
        ('Decolorare Păr Mediu', 'hair'),
        ('Spălat', 'hair'),
        ('Coafat Păr Lung', 'hair'),
        ('Coafat Păr Scurt', 'hair'),
        ('Coafat Păr Mediu', 'hair'),
        ('Coafat Ocazie', 'hair'),
        ('Epilare Definitivă Full Body', 'cosmetics'),
        ('Epilare Definitivă Zona Inghinală', 'cosmetics'),
        ('Epilare Definitivă Axile', 'cosmetics'),
        ('Epilare Definitivă Mâini', 'cosmetics'),
        ('Epilare Definitivă Picioare', 'cosmetics'),
        ('Epilare cu Ceară Full-Body', 'cosmetics'),
        ('Epilare cu Ceară Axile', 'cosmetics'),
        ('Epilare cu Ceară Zona Inghinală', 'cosmetics'),
        ('Epilare cu Ceară Picioare', 'cosmetics'),
        ('Epilare cu Ceară Mâini', 'cosmetics'),
        ('Epilare cu Ceară Mustață', 'cosmetics'),
        ('Pensat', 'cosmetics'),
        ('Machiaj de Zi', 'cosmetics'),
        ('Machiaj de Seară', 'cosmetics'),
        ('Machiaj de Ocazie', 'cosmetics'),
        ('Remodelare Corporală', 'cosmetics'),
        ('Ședință de Îndepărtare Tatuaj', 'cosmetics'),
        ('Solar', 'cosmetics')
    ]

    for name, category in services:
        db.add(Service(name=name, category=category))

    # Add artists
    artists = [
        ('Roxana', 'nails'),
        ('Maria', 'nails'),
        ('Eva', 'cosmetics'),
        ('Daria', 'hair'),
        ('Roxana', 'hair'),
        ('Maria', 'hair'),
    ]

    for name, specialization in artists:
        db.add(Artist(name=name, specialization=specialization))

    db.commit()  # Make sure to commit changes to the database
    db.close()  # Close the session


def update_service_names():
    """Update service names in the database."""
    db = SessionLocal()

    updates = {
        'manichiura semipermanenta': 'Manichiura Semipermanentă',
        'manichiura cu gel': 'Manichiura cu Gel',
        'manichiura simpla': 'Manichiura Simplă',
        'intretinere manichiura': 'Întreținere Manichiură',
        'pedichiura semipermanenta': 'Pedichiură Semipermanentă',
        'intretinere pedichiura': 'Întreținere Pedichiură',
        'manichiura + pedichiura simpla': 'Manichiură + Pedichiură Simplă',
        'manichiura + pedichiura semipermanenta': 'Manichiură + Pedichiură Semipermanentă',
        'manichiura gel + pedichiura simpla': 'Manichiură Gel + Pedichiură Simplă',
        'manichiura gel + pedichiura semipermanenta': 'Manichiură Gel + Pedichiură Semipermanentă',
        'tuns par lung': 'Tuns Păr Lung',
        'tuns par scurt': 'Tuns Păr Scurt',
        'tuns par mediu': 'Tuns Păr Mediu',
        'coafat': 'Coafat',
        'tuns par lung + coafat': 'Tuns Păr Lung + Coafat',
        'tuns par scurt + coafat': 'Tuns Păr Scurt + Coafat',
        'tuns par mediu + coafat': 'Tuns Păr Mediu + Coafat',
        'vopsit par lung': 'Vopsit Păr Lung',
        'vopsit par scurt': 'Vopsit Păr Scurt',
        'vopsit par mediu': 'Vopsit Păr Mediu',
        'decolorat par scurt': 'Decolorare Păr Scurt',
        'decolorat par lung': 'Decolorare Păr Lung',
        'decolorat par mediu': 'Decolorare Păr Mediu',
        'spalat': 'Spălat',
        'coafat par lung': 'Coafat Păr Lung',
        'coafat par scurt': 'Coafat Păr Scurt',
        'coafat par mediu': 'Coafat Păr Mediu',
        'coafat ocazie': 'Coafat Ocazie',
        'epilare definitiva full body': 'Epilare Definitivă Full Body',
        'epilare definitiva zona inghinala': 'Epilare Definitivă Zona Inghinală',
        'epilare definitiva axile': 'Epilare Definitivă Axile',
        'epilare definitiva maini': 'Epilare Definitivă Mâini',
        'epilare definitiva picioare': 'Epilare Definitivă Picioare',
        'epilare cu ceara full-body': 'Epilare cu Ceară Full-Body',
        'epilare cu ceara axile': 'Epilare cu Ceară Axile',
        'epilare cu ceara zona inghinala': 'Epilare cu Ceară Zona Inghinală',
        'epilare cu ceara picioare': 'Epilare cu Ceară Picioare',
        'epilare cu ceara maini': 'Epilare cu Ceară Mâini',
        'epilare cu ceara mustata': 'Epilare cu Ceară Mustață',
        'pensat': 'Pensat',
        'machiaj de zi': 'Machiaj de Zi',
        'machiaj de seara': 'Machiaj de Seară',
        'machiaj de ocazie': 'Machiaj de Ocazie',
        'remodelare corporala': 'Remodelare Corporală',
        'sedinta de indepartare tatuaj': 'Ședință de Îndepărtare Tatuaj',
        'solar': 'Solar'
    }

    for old_name, new_name in updates.items():
        db.query(Service).filter(Service.name == old_name).update({'name': new_name}, synchronize_session=False)

    db.commit()
    db.close()


def get_appointment_details():
    """Retrieve detailed appointment information."""
    db = SessionLocal()

    appointments = db.query(Appointment).options(
        joinedload(Appointment.user),
        joinedload(Appointment.artist),
        joinedload(Appointment.service)
    ).all()

    details = []
    for appt in appointments:
        detail = {
            'user_name': appt.user.name,
            'user_phone': appt.user.phone_number,
            'service_name': appt.service.name,
            'category': appt.service.category,
            'artist_name': appt.artist.name,
            'appointment_date': appt.appointment_date,
            'appointment_time': appt.appointment_time
        }
        details.append(detail)

    db.close()
    return details


if __name__ == "__main__":
    init_db()
    populate_db()
    # Optionally update service names if needed
    # update_service_names()
    # Retrieve and print appointment details
    appointment_details = get_appointment_details()
    for detail in appointment_details:
        print(detail)
