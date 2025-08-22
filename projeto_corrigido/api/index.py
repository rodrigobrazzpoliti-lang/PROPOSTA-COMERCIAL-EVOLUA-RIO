from flask import Flask, send_from_directory, jsonify
from flask_cors import CORS
import os
import sys

# Adicionar o diretório atual ao path para imports funcionarem
sys.path.append(os.path.dirname(__file__))

try:
    from models.user import db
    from routes.user import user_bp
    from routes.proposal import proposal_bp
except ImportError as e:
    print(f"Erro de import: {e}")
    # Fallback para desenvolvimento local
    pass

app = Flask(__name__)
app.config['SECRET_KEY'] = 'asdf#FGSgvasgf$5$WGT'

# Habilitar CORS para permitir requisições do frontend
CORS(app)

# Registrar blueprints se disponíveis
try:
    app.register_blueprint(user_bp, url_prefix='/api')
    app.register_blueprint(proposal_bp, url_prefix='/api/proposal')
except NameError:
    print("Blueprints não carregados - modo de desenvolvimento")

# Configuração do banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

try:
    db.init_app(app)
    with app.app_context():
        db.create_all()
except NameError:
    print("Banco de dados não configurado - modo de desenvolvimento")

# Rota de teste para verificar se a API está funcionando
@app.route('/api/health')
def health_check():
    return jsonify({'status': 'OK', 'message': 'API funcionando corretamente'})

# Servir arquivos estáticos do frontend
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    static_folder = os.path.join(os.path.dirname(__file__), '..', 'static')
    
    if path != "" and os.path.exists(os.path.join(static_folder, path)):
        return send_from_directory(static_folder, path)
    else:
        index_path = os.path.join(static_folder, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder, 'index.html')
        else:
            return jsonify({'error': 'Frontend não encontrado', 'path': static_folder}), 404

@app.route('/proposta/<proposal_id>')
def view_proposal_route(proposal_id):
    try:
        from routes.proposal import proposals_storage, view_proposal
        return view_proposal(proposal_id)
    except ImportError:
        return jsonify({'error': 'Módulo de propostas não disponível'}), 500

# Para execução local
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

