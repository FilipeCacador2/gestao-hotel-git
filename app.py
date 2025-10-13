from flask import Flask, render_template, request, redirect, url_for
from clientes import ClientesRepo
from quartos import QuartosRepo
from reservas import ReservasRepo

app = Flask(__name__)

clientes = ClientesRepo()
quartos = QuartosRepo()
reservas = ReservasRepo()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/clientes')
def ver_clientes():
    return render_template('clientes.html', clientes=clientes.list_all())


@app.route('/clientes/add', methods=['POST'])
def add_cliente():
    nome = request.form['nome']
    telefone = request.form['telefone']
    email = request.form['email']
    clientes.add(nome, telefone, email)
    return redirect(url_for('ver_clientes'))


@app.route('/clientes/del/<int:cid>')
def del_cliente(cid):
    clientes.remove(cid)
    return redirect(url_for('ver_clientes'))


@app.route('/quartos')
def ver_quartos():
    return render_template('quartos.html', quartos=quartos.list_all())


@app.route('/quartos/add', methods=['POST'])
def add_quarto():
    numero = int(request.form['numero'])
    tipo = request.form['tipo']
    preco = float(request.form['preco'])
    quartos.add(numero, tipo, preco)
    return redirect(url_for('ver_quartos'))


@app.route('/quartos/del/<int:num>')
def del_quarto(num):
    quartos.remove(num)
    return redirect(url_for('ver_quartos'))


@app.route('/reservas')
def ver_reservas():
    return render_template(
        'reservas.html',
        reservas=reservas.list_all(),
        clientes=clientes.list_all(),
        quartos=quartos.list_all(),
    )


@app.route('/reservas/add', methods=['POST'])
def add_reserva():
    cid = int(request.form['cliente_id'])
    qnum = int(request.form['quarto_numero'])
    checkin = request.form['checkin']
    checkout = request.form['checkout']
    try:
        reservas.create(cid, qnum, checkin, checkout)
    except Exception as e:
        return f"Erro: {e}", 400
    return redirect(url_for('ver_reservas'))


@app.route('/reservas/del/<int:rid>')
def del_reserva(rid):
    reservas.cancel(rid)
    return redirect(url_for('ver_reservas'))


if __name__ == '__main__':
    app.run(debug=True)
