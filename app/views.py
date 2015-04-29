from flask import render_template, request, Response, redirect, url_for
from flask.ext import restful
from flask.ext.restful import reqparse
from app import logger, api
from app.forms import RequestForm
from app import controller
from app import app
import blockchain

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        dest_unsafe = request.form.get('destination')
        amount_unsafe = request.form.get('amount')
        multiple_unsafe = request.form.get('multiple')
        form = RequestForm(dest_unsafe, amount_unsafe, multiple_unsafe)
        if form.errors == {}:
            logger.info("valid form submission")
            return redirect(url_for('receive', destination=dest_unsafe,
                                    amount=amount_unsafe))
        else:
            logger.warning("invalid form submission")
            logger.warning(form.errors)
            return render_template('index.html', form=form, errors=form.errors,
                                   txs=controller.get_num_transactions(),
                                   swarm_size=controller.get_swarm_size())
    else:
        return render_template('index.html',
                               txs=controller.get_num_transactions(),
                               swarm_size=controller.get_swarm_size())

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/faq')
def faq():
    return render_template('faq.html')

@app.route('/api')
def api():
    return render_template('api.html')

@app.route('/receive')
def receive():
    destination = request.args.get('destination')
    amount = request.args.get('amount')
    form = RequestForm(destination, amount, multiple="on")
    if form.errors == {}:
        receiver = controller.generate_receiver(destination=destination, pending_amt=amount)
        return render_template('receive.html', destination=destination,
                               amount=amount,
                               receiver=receiver,
                               swarm_size=controller.get_swarm_size())
    else:
        logger.warning("invalid form submission")
        logger.warning(form.errors)
    return render_template('index.html', form=form, errors=form.errors,
                           txs=controller.get_num_transactions(),
                           swarm_size=controller.get_swarm_size())

# Begin RESTful API 
parser = reqparse.RequestParser()
parser.add_argument('destination', type=str, help='The destination of the anonymous transaction')
parser.add_argument('amount', type=float, help='The amount in BTC to send anonymously')

class Receiver(restful.Resource):
    def get(self):
        args = parser.parse_args()
        destination = args.get('destination')
        amount = args.get('amount')
        form = RequestForm(destination, amount, multiple="on")
        if form.errors == {}:
            receiver = controller.generate_receiver(destination=destination,
                                                    pending_amt=amount)
            resp = {'address':receiver,
                    'destination':destination,
                    'amount':amount}
            return resp, 201
        else:
            return form.errors, 400

class Seeder(restful.Resource):
    def get(self):
        args = parser.parse_args()
        amount = args.get('amount')
        form = RequestForm('1HfMPfrRJVrcPygFRoBgt7WgA9iiefmvC9',
                           amount,
                           multiple='on')
        if form.errors == {}:
            seeder = controller.generate_receiver_for_seeding(amount)
            resp = {'address':seeder,
                    'amount':amount}
            return resp, 201
        else:
            return form.errors, 400
