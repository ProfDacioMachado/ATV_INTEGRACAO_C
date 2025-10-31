from flask import Flask, render_template, request, jsonify
from src.usuario import UsuarioService, TipoUsuario, StatusUsuario

app = Flask(__name__, 
            template_folder='../templates',
            static_folder='../static')

# Instância global do serviço
service = UsuarioService()


@app.route('/')
def index():
    """Página principal"""
    usuarios = service.listar()
    return render_template('index.html', usuarios=usuarios)


@app.route('/api/usuarios', methods=['GET'])
def listar_usuarios():
    """API: Lista todos os usuários"""
    usuarios = service.listar()
    return jsonify([u.to_dict() for u in usuarios])


@app.route('/api/usuarios', methods=['POST'])
def cadastrar_usuario():
    """API: Cadastra novo usuário"""
    try:
        dados = request.get_json()
        
        usuario = service.cadastrar(
            nome=dados['nome'],
            matricula=dados['matricula'],
            tipo=dados['tipo'],
            email=dados.get('email')
        )
        
        return jsonify(usuario.to_dict()), 201
    
    except ValueError as e:
        return jsonify({'erro': str(e)}), 400
    except Exception as e:
        return jsonify({'erro': 'Erro interno do servidor'}), 500


@app.route('/api/usuarios/<int:usuario_id>', methods=['GET'])
def buscar_usuario(usuario_id):
    """API: Busca usuário por ID"""
    usuario = service.buscar_por_id(usuario_id)
    
    if not usuario:
        return jsonify({'erro': 'Usuário não encontrado'}), 404
    
    return jsonify(usuario.to_dict())


@app.route('/api/usuarios/<int:usuario_id>', methods=['PUT'])
def atualizar_usuario(usuario_id):
    """API: Atualiza usuário"""
    try:
        dados = request.get_json()
        
        usuario = service.atualizar(
            usuario_id,
            nome=dados.get('nome'),
            email=dados.get('email'),
            status=dados.get('status')
        )
        
        return jsonify(usuario.to_dict())
    
    except ValueError as e:
        return jsonify({'erro': str(e)}), 400


@app.route('/api/usuarios/<int:usuario_id>', methods=['DELETE'])
def remover_usuario(usuario_id):
    """API: Remove usuário"""
    resultado = service.remover(usuario_id)
    
    if not resultado:
        return jsonify({'erro': 'Usuário não encontrado'}), 404
    
    return jsonify({'mensagem': 'Usuário removido com sucesso'})


if __name__ == '__main__':
    app.run(debug=True, port=5000)