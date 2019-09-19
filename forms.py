# -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, URL

class NavcardForm(FlaskForm):
    name = StringField('name', validators=[DataRequired(), Length(1,50)])
    url = StringField('url', validators=[DataRequired(), URL(), Length(1,255)])
    thumnail = StringField('thumnail', validators=[DataRequired(), URL(), Length(1,255)])
    submit = SubmitField()