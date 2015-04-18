from flask import render_template, request, Response, redirect, url_for
from app import app, logger
from forms import RequestForm
import controller
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

@app.route('/receive')
def receive():
    destination = request.args.get('destination')
    amount = request.args.get('amount')
    form = RequestForm(destination, amount, multiple="on")
    if form.errors == {}:
        receiver = controller.generate_receiver(destination=destination, pending_amt=amount)
        return render_template('receive.html', destination=destination,
                               amount=amount,
                               receiver=receiver)
    else:
        logger.warning("invalid form submission")
        logger.warning(form.errors)
    return render_template('index.html', form=form, errors=form.errors,
                           txs=controller.get_num_transactions(),
                           swarm_size=controller.get_swarm_size())
