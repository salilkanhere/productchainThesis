from flask import Flask, render_template
from config import Config, SetupStatus
from forms import CreateForm, TransferForm, StoryQueryForm, CreateHACCPForm, QueryTempForm
from utils import Setup, CreateBatch, TransferBatch, QueryBatch, CreateHACCP, QueryTemp

app = Flask(__name__)
app.config.from_object(Config)

app.setup_status = 0

@app.route('/')
def home():
    if not app.setup_status:
        setup = Setup()
        setup_result = setup.init()
        if not setup_result:
            print("ERROR: during setup")
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
        if response:
            response = "Create Batch transaction successfully submitted"
        else:
            response = "Failed to submit transaction. Ensure batch does not yet exist and the HACCP exists for the product type. Ensure all constituents are in the same region."
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
        if response:
            response = "Create HACCP transaction successfully submitted"
        else:
            response = "Failed to submit transaction. Ensure product type is either 'MEAT' or 'MILK'"
    else:
        response = "Please fill in all fields"

    return render_template('create_HACCP.html', title='Create HACCP', form=form, response=response)

@app.route('/query_temperature/', methods=['GET', 'POST'])
def query_temperature():
    response = ''
    form = QueryTempForm()

    print form.validate_on_submit()
    if form.validate_on_submit():
        queryTemp = QueryTemp()

        #queryTemp.test(form.batch_id.data)
        response = queryTemp.query(form.batch_id.data)
        if not response:
            response = "Query failed. Ensure batch exists."
    else:
        response = "Please fill in all fields"

    return render_template('query_temperature.html', title='Query Temperature', form=form, response=response)



@app.route('/transfer_batch/', methods=['GET', 'POST'])
def transfer_batch():
    response = ''
    form = TransferForm()
    if form.validate_on_submit():
        transferBatch = TransferBatch()
        response = transferBatch.transfer(form.batch_id.data, form.owner.data, form.product_type.data, form.region.data)
        if response:
            response = "Create HACCP transaction successfully submitted"
        else:
            response = "Failed to submit transaction. Ensure the HACCP exists for the product type"
    else:
        response = "Please fill in all fields"
        
    return render_template('transfer_batch.html', title='Transfer Batch', form=form, response=response)


@app.route('/product_story_query/', methods=['GET', 'POST'])
def product_story_query():
    response = ''
    warn = ''
    form = StoryQueryForm()
    if form.validate_on_submit():
        queryBatch = QueryBatch()

        #queryBatch.test(form.batch_id.data)
        response = queryBatch.query(form.batch_id.data)
        if not response:
            response = []
            warn = "Batch does not exist."
    else:
        warn = "Please fill in all fields"

    return render_template('product_story_query.html', title='Query Batch', form=form, response=response, warn=warn)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
