from flask import Flask, render_template
from config import Config
from forms import CreateForm, TransferForm, StoryQueryForm

app = Flask(__name__)
app.config.from_object(Config)

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/create_batch/')
def create_batch():
    form = CreateForm()
    return render_template('create_batch.html', title='Create Batch', form=form)


@app.route('/transfer_batch/')
def transfer_batch():
    form = TransferForm()
    return render_template('transfer_batch.html', title='Transfer Batch', form=form)


@app.route('/product_story_query/')
def product_story_query():
    form = StoryQueryForm()
    return render_template('product_story_query.html', title='Query Batch', form=form)

if __name__ == '__main__':
    app.run(debug=True)
