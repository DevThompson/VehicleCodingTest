from flask import Flask, request, jsonify, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from dotenv import load_dotenv
load_dotenv()  # take environment variables from .env.
import os



# Init App
app = Flask(__name__)

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DBROOT = os.environ.get('DATABASE_ROOT')
DBSUBDIR = os.environ.get('DATABASE_DIR')

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = DBROOT + os.path.join(BASE_DIR, DBSUBDIR)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Init db
db = SQLAlchemy(app)

# Init ma
ma = Marshmallow(app)


# Vehicle Table
class Vehicle(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  vehicletype = db.Column(db.String(200))
  mileage = db.Column(db.Integer)
  hybrid = db.Column(db.Boolean)

  def __init__(self, vehicletype, mileage, hybrid):
    self.vehicletype = vehicletype
    self.mileage = mileage
    self.hybrid = hybrid

# Vehicle Schema
class VehicleSchema(ma.Schema):
  class Meta:
    fields = ('id', 'vehicletype', 'mileage', 'hybrid')


# Init Schema
vehicle_schema = VehicleSchema()
vehicles_schema = VehicleSchema(many=True)


## POST
@app.route('/vehicle', methods=['POST'])
def add_vehicle():
  vehicletype = request.form['vehicletype']
  mileage = request.form['mileage']

  if request.form['hybrid'] == 'Y':
    hybrid = True
  else:
    hybrid = False

  new_vehicle = Vehicle(vehicletype, mileage, hybrid)
  db.session.add(new_vehicle)
  db.session.commit()

  return redirect('/vehicle')

## GET
@app.route('/vehicle', methods=['GET'])
def get_vehicles():
  all_vehicles = Vehicle.query.all()
  result = vehicles_schema.dump(all_vehicles)

  return render_template('base.html', results=result)


## DELETE
## Used solely for testing
@app.route('/vehicle/<vehicle_id>', methods=['DELETE'])
def delete_vehicle(vehicle_id):
   vehicle = Vehicle.query.get(vehicle_id)
   db.session.delete(vehicle)
   db.session.commit()

   return jsonify({'vechileDeleted': vehicle_id})

@app.route('/')
def home():
  return redirect('/vehicle')


if __name__ == '__main__':
  app.run(debug=True)
