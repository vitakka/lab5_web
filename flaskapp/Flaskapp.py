from flask import Flask, render_template, flash
from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileAllowed, FileRequired
from flask_bootstrap import Bootstrap
from werkzeug.utils import secure_filename
import os
import net as neuronet

app = Flask(__name__)

# Конфигурация
SECRET_KEY = 'secret'
app.config['SECRET_KEY'] = SECRET_KEY
app.config['RECAPTCHA_USE_SSL'] = False

app.config['RECAPTCHA_OPTIONS'] = {'theme': 'white'}

bootstrap = Bootstrap(app)

class NetForm(FlaskForm):
    openid = StringField('openid', validators=[DataRequired()])
    upload = FileField('Load image', validators=[
        FileRequired(),
        FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])
    recaptcha = RecaptchaField()
    submit = SubmitField('send')

@app.route('/')
def data_to():
    some_str = "название страницы опца дрица"
    some_value = 42
    some_pars = {'user':'Ivan','color':'green'}
    return render_template('simple.html',
                           some_str=some_str,
                           some_value=some_value,
                           some_pars=some_pars)

@app.route("/net", methods=['GET', 'POST'])
def net():
    form = NetForm()
    filename = None
    neurodic = {}




    # ПЕРЕНЕСИТЕ ВСЮ ЛОГИКУ СОХРАНЕНИЯ ВНУТРЬ УСЛОВИЯ!
    if form.validate_on_submit():


        try:
            # Сохраняем файл
            filename = os.path.join('./static', secure_filename(form.upload.data.filename))
            form.upload.data.save(filename)
            print('записанный файл если выйдет то увидим'+filename)
            print('--------------------------------------------------------------------------')

            # Обрабатываем изображение нейросетью
            fcount, fimage = neuronet.read_image_files(10, './static')
            decode = neuronet.getresult(fimage)
            print(decode)

            # Записываем результаты
            for elem in decode:
                neurodic[elem[0][1]] = elem[0][2]
                print(elem)

            flash('Файл успешно загружен и обработан!', 'success')

        except Exception as e:
            flash(f'Ошибка при обработке файла: {str(e)}', 'error')
    else:
        print("Форма не валидирована. Ошибки:")
        for field, errors in form.errors.items():
            print(f"Поле {field}: {', '.join(errors)}")

    # Рендерим шаблон ВНЕ условия (выполняется всегда)
    return render_template('net.html', form=form, image_name=filename, neurodic=neurodic)

if __name__ == '__main__':
    # Создаем папку static если её нет
    if not os.path.exists('./static'):
        os.makedirs('./static')
    app.run(debug=True)