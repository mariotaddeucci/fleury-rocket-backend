from flask import Flask, jsonify, request, Response
from Database import db, Exame, ExameRestricao, ExameTag
from vision_api import read_image_text
from flask_cors import CORS
from icalendar import Calendar, Event
from datetime import datetime, timedelta
from pytz import UTC  # timezone

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})
app.config.from_pyfile('config.cfg')
db.init_app(app)


def exames_by_tag(arr):
    arr = [a.upper() for a in arr]
    exames = ExameTag.query.filter(ExameTag.tag_name.in_(arr)).all()
    exames = [e.id_exame for e in exames]
    exames = list(set(exames))
    return Exame.query.filter(Exame.id.in_(exames)).order_by(Exame.nome).all()


@app.route('/api/ics', methods=['POST'])
def ics():
    content = request.json

    start_date = content.get('start_date', datetime.now())
    minutes = content.get('minutes', 0)
    end_date = start_date + timedelta(minutes=minutes)

    cal = Calendar()
    cal.add('prodid', '-//My calendar product//mxm.dk//')
    cal.add('version', '2.0')

    event = Event()
    event.add('summary', 'Agendamento Consulta Fleury')
    event.add('dtstart', start_date)
    event.add('dtend', end_date)

    cal.add_component(event)
    response = Response(cal.to_ical())
    response.headers["Content-Disposition"] = "attachment; filename=calendar.ics"
    return cal.to_ical()


@app.route('/api/exame')
def exames():
    exames = Exame.query.all()
    exames = [{'name': e.nome, 'ac': e.ac, 'id': e.id} for e in exames]
    return jsonify(exames)


@app.route('/api/roteiro', methods=['POST'])
def roteiro():
    content = request.json
    ids = content.get('examToCronogram', [])

    restr = db.session.query(
        ExameRestricao.id_exame
    ).filter(ExameRestricao.id_exame.in_(ids)) \
        .order_by(ExameRestricao.executar.desc(),
                  ExameRestricao.tempo_restricao).all()

    order = []
    for r in restr:
        if r[0] not in order:
            order.append(r[0])

    n_restr = list(set(ids) - set(order))
    sorted_ids = n_restr + order
    result = [Exame.query.get(e_id).__dict__ for e_id in sorted_ids]

    restricao = {}
    realizado = 0
    for dt in result:
        restricoes = ExameRestricao.query.filter_by(id_exame=dt['id']).all()
        if len(restricoes) > 0:
            for restr in restricoes:
                msg = restr.mensagem.mensagem
                atual = restricao.get(msg, 0)
                tempo_restante = restr.tempo_restricao - realizado
                if atual < tempo_restante:
                    restricao[msg] = tempo_restante
        realizado = realizado + dt['duracao']
        del dt['_sa_instance_state']
    restis = []
    for name, minutes in restricao.items():
        restis.append(name + " " + str(minutes))
    proxima_vaga = datetime.now() + timedelta(days=3)
    return jsonify({
        'exames': result,
        'restricoes': restis,
        'minutos': realizado,
        'disponivel': proxima_vaga
    })


@app.route('/api/getByImage', methods=['POST'])
def get_from_image():
    if request.data:
        # filename = file.filename
        file_location = request.data
        words = read_image_text(file_location)
        exames = exames_by_tag(words)
        result = [exame.__dict__ for exame in exames]
        for r in result:
            del r['_sa_instance_state']
    return jsonify(result)


@app.before_first_request
def cria_db():
    db.create_all()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
