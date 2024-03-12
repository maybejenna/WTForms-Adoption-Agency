from flask import Flask, render_template, flash, redirect, request, render_template
from flask_debugtoolbar import DebugToolbarExtension

from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, BooleanField, IntegerField, TextAreaField
from wtforms.validators import InputRequired, Optional, URL, NumberRange, AnyOf

from models import db, connect_db, Pet 


app = Flask(__name__)
app.config["SECRET_KEY"] = "oh-so-secret"
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///pet"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


connect_db(app)

@app.route("/")
def index():
    pets = Pet.query.all()  # Or any other query that fits your needs
    return render_template('index.html', pets=pets)

@app.route('/pets/<int:pet_id>')
def show_pet(pet_id):
    pet = Pet.query.get_or_404(pet_id)
    return render_template('pet_detail.html', pet=pet)

class PetForm(FlaskForm):
    name = StringField("Pet Name", validators=[InputRequired()])
    species = SelectField("Species", validators=[InputRequired(), AnyOf(values=["cat", "dog", "porcupine"])], choices=[('cat', 'Cat'), ('dog', 'Dog'), ('porcupine', 'Porcupine')])
    photo_url = StringField("Photo URL", validators=[Optional(), URL()])
    age = IntegerField("Age", validators=[Optional(), NumberRange(min=0, max=30)])
    notes = TextAreaField("Notes", validators=[Optional()])

@app.route("/add", methods=["GET", "POST"])
def add_pet():
    form = PetForm()

    if form.validate_on_submit():
        new_pet = Pet(
            name=form.name.data,
            species=form.species.data,
            photo_url=form.photo_url.data or None,  # Handle optional photo URL
            age=form.age.data,
            notes=form.notes.data,
            available=True  # Assuming all new pets are available by default
        )
        db.session.add(new_pet)
        db.session.commit()
        flash(f"{new_pet.name} added successfully!", "success")
        return redirect("/")
    else:
        return render_template("add_pet.html", form=form)
    
    
class EditPetForm(FlaskForm):
    """Form for editing an existing pet."""
    photo_url = StringField("Photo URL", validators=[Optional(), URL()])
    notes = TextAreaField("Notes", validators=[Optional()])
    available = BooleanField("Available")


@app.route('/<int:pet_id>', methods=['GET', 'POST'])
def edit_pet(pet_id):
    pet = Pet.query.get_or_404(pet_id)
    form = EditPetForm(obj=pet)

    if form.validate_on_submit():
        pet.photo_url = form.photo_url.data
        pet.notes = form.notes.data
        pet.available = form.available.data
        db.session.commit()
        flash(f"{pet.name}'s details updated successfully.")
        return redirect('/')
    else:
        return render_template('edit_pet_form.html', form=form, pet=pet)
    

@app.route("/search")
def search():
    query = request.args.get("query")
    pets = Pet.query.filter(
        (Pet.name.ilike(f"%{query}%")) | 
        (Pet.species.ilike(f"%{query}%")) | 
        (Pet.notes.ilike(f"%{query}%"))
    ).all()
    return render_template("index.html", pets=pets)