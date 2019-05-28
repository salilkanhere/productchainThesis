from flask import Flask, render_template
from config import Config
from forms import CreateForm, TransferForm, StoryQueryForm

app = Flask(__name__)
app.config.from_object(Config)

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/create_batch/', methods=['GET', 'POST'])
def create_batch():
    response = ''
    form = CreateForm()
    print form.validate_on_submit()
    if form.validate_on_submit():
        response = "Hello"
    else:
        response = "Please fill in all fields"

    print(response)
    return render_template('create_batch.html', title='Create Batch', form=form, response=response)


@app.route('/transfer_batch/', methods=['GET', 'POST'])
def transfer_batch():
    response = ''
    form = TransferForm()
    if form.validate_on_submit():
        response = "Hello"
    else:
        response = "Please fill in all fields"
        
    return render_template('transfer_batch.html', title='Transfer Batch', form=form, response=response)


@app.route('/product_story_query/', methods=['GET', 'POST'])
def product_story_query():
    response = ''
    form = StoryQueryForm()
    if form.validate_on_submit():
        response = "Hello"
    else:
        response = "Please fill in all fields"

    return render_template('product_story_query.html', title='Query Batch', form=form, response=response)

if __name__ == '__main__':
    app.run(debug=True)
