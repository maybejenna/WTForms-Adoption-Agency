from app import app, db 
from models import Pet

with app.app_context():
    db.drop_all()
    db.create_all()

    pets_to_add = [
        Pet(name="Buddy", species="Dog", photo_url="https://cdn.britannica.com/79/232779-050-6B0411D7/German-Shepherd-dog-Alsatian.jpg", age=3, available=True),
        Pet(name="Misty", species="Cat", photo_url="https://images.pexels.com/photos/104827/cat-pet-animal-domestic-104827.jpeg?cs=srgb&dl=pexels-pixabay-104827.jpg&fm=jpg", age=2, available=True),
        Pet(name="Goldie", species="Fish", photo_url="https://www.hikariusa.com/wp/wp-content/uploads/Goldfish-Fancy.jpg", available=True),
        Pet(name="Tweety", species="Bird", age=1, notes="Loves to sing", available=True),
        Pet(name="Hopper", species="Rabbit", age=5, available=False),
        Pet(name="Spike", species="Porcupine", photo_url="https://t3.ftcdn.net/jpg/03/40/69/38/360_F_340693892_PZ6UIBKlo91d5a09Nt3WNPSaCytuFO9U.jpg", age=4, notes="Very friendly, but handle with care!", available=True)
    ]

    for pet in pets_to_add:
        db.session.add(pet)
    db.session.commit()
