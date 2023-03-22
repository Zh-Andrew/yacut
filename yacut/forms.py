from flask_wtf import FlaskForm
from wtforms import SubmitField, URLField
from wtforms.validators import DataRequired, Length, Optional, Regexp

from . import PATTERN_SHORT_URL, PATTERN_URL


class YacutForm(FlaskForm):
    original_link = URLField(
        'Длинная ссылка',
        validators=[
            DataRequired(message='Обязательное поле'),
            Regexp(PATTERN_URL,
                   message='Ссылка некорректна')
        ]
    )
    custom_id = URLField(
        'Укороченная ссылка',
        validators=[
            Length(1, 16),
            Optional(),
            Regexp(PATTERN_SHORT_URL,
                   message='Разрешенные символы: прописные,'
                           ' строчные латинские буквы, цифры.')
        ]
    )
    submit = SubmitField('Создать')
