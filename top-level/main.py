from flask import Flask, render_template
from config import Config, SetupStatus
from forms import CreateForm, TransferForm, StoryQueryForm, CreateHACCPForm
from utils import Setup, CreateBatch, TransferBatch, QueryBatch, CreateHACCP

app = Flask(__name__)
app.config.from_object(Config)

app.setup_status = 0

@app.route('/')
def home():
    if not app.setup_status:
        setup = Setup()
        setup.init()
        app.setup_status = 1
    
    return render_template('home.html', title='ProductChain')


@app.route('/create_batch/', methods=['GET', 'POST'])
def create_batch():
    response = ''
    form = CreateForm()

    print form.validate_on_submit()
    if form.validate_on_submit():
        createBatch = CreateBatch()
        response = createBatch.create(form.batch_id.data, form.owner.data, form.product_type.data, form.region.data, form.constituents.data)
    else:
        response = "Please fill in all fields"

    return render_template('create_batch.html', title='Create Batch', form=form, response=response)

@app.route('/create_HACCP/', methods=['GET', 'POST'])
def create_HACCP():
    response = ''
    form = CreateHACCPForm()

    print form.validate_on_submit()
    if form.validate_on_submit():
        createHACCP = CreateHACCP()
        response = createHACCP.create(form.product_type.data, form.min_temperature.data, form.max_temperature.data)
    else:
        response = "Please fill in all fields"

    return render_template('create_HACCP.html', title='Create HACCP', form=form, response=response)



@app.route('/transfer_batch/', methods=['GET', 'POST'])
def transfer_batch():
    response = ''
    form = TransferForm()
    if form.validate_on_submit():
        transferBatch = TransferBatch()
        response = transferBatch.transfer(form.batch_id.data, form.owner.data, form.product_type.data, form.region.data)
    else:
        response = "Please fill in all fields"
        
    return render_template('transfer_batch.html', title='Transfer Batch', form=form, response=response)


@app.route('/product_story_query/', methods=['GET', 'POST'])
def product_story_query():
    response = ''
    form = StoryQueryForm()
    if form.validate_on_submit():
        queryBatch = QueryBatch()
        response = queryBatch.query(form.batch_id.data)
    else:
        response = "Please fill in all fields"

    return render_template('product_story_query.html', title='Query Batch', form=form, response=response)

if __name__ == '__main__':
    app.run(debug=True)