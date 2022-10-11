from flask_app import app
from flask import render_template, request, redirect, flash, session
from flask_app.models import user_model, order_model
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

