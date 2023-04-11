from flask.views import MethodView
from wtforms import Form, StringField, SubmitField, FloatField, IntegerField
from flask import Flask, render_template, request

from calories import Calories
from temperature import Temperature

app = Flask(__name__)


class HomePage(MethodView):
    def get(self):
        return render_template('index.html')


class CaloriesFormPage(MethodView):
    def get(self):
        calories_form = CaloriesForm()
        return render_template('calories_form_page.html', calories_form=calories_form)


class ResultPage(MethodView):
    def post(self):
        calories_form = CaloriesForm(request.form)

        weight = calories_form.weight.data
        height = calories_form.height.data
        age = calories_form.age.data

        city = calories_form.city.data
        country = calories_form.country.data

        temperature = Temperature(city=city, country=country)

        the_calories = Calories(weight=weight, height=height, age=age, temperature=temperature.get())

        return render_template('results.html', calories=the_calories.calculate())


class CaloriesForm(Form):
    weight = FloatField('Weight (kg): ', default=75)
    height = FloatField('Height (cm): ', default=180)
    age = IntegerField('Age: ', default=25)

    city = StringField('City: ', default='Washington DC')
    country = StringField('Country: ', default='USA')

    button = SubmitField('Calculate')


app.add_url_rule('/', view_func=HomePage.as_view('home_page'))

app.add_url_rule('/calories_form', view_func=CaloriesFormPage.as_view('calories_form_page'))

app.add_url_rule('/results', view_func=ResultPage.as_view('results_page'))

app.run(debug=True)
