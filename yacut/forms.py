from flask_wtf import FlaskForm
from wtforms import SubmitField, URLField
from wtforms.validators import DataRequired, Length, Optional


class YacutForm(FlaskForm):
    original_link = URLField(
        'Длинная ссылка',
        validators=[DataRequired(message='Обязательное поле')]
    )
    custom_id = URLField(
        'Укороченная ссылка',
        validators=[Length(1, 20), Optional()]
    )
    submit = SubmitField('Создать')
