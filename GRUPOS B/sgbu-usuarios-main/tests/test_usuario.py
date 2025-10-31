import pytest
from datetime import datetime
from src.usuario import Usuario, UsuarioService, TipoUsuario, StatusUsuario

class TestUsuarioModel:
    """Testes unitários do modelo Usuario"""
    
    def test_criar_usuario_valido(self):
        """[TDD] Deve criar usuário com dados válidos"""
        usuario = Usuario(
            nome="João Silva",
            matricula="ALU12345",
            tipo=TipoUsuario.ALUNO,
            email="joao@email.com"
        )
        
        assert usuario.nome == "João Silva"
        assert usuario.matricula == "ALU12345"
        assert usuario.tipo == TipoUsuario.ALUNO
        assert usuario.email == "joao@email.com"
        assert usuario.status == StatusUsuario.ATIVO
        assert isinstance(usuario.dataRegistro, str)
    
    def test_rejeitar_nome_curto(self):
        """[TDD] Deve rejeitar nome com menos de 1 caractere"""
        with pytest.raises(ValueError, match="Nome deve ter entre 1 e 100 caracteres"):
            Usuario(
                nome="",
                matricula="ALU12345",
                tipo=TipoUsuario.ALUNO
            )
    
    def test_rejeitar_nome_longo(self):
        """[TDD] Deve rejeitar nome com mais de 100 caracteres"""
        nome_longo = "A" * 101
        with pytest.raises(ValueError, match="Nome deve ter entre 1 e 100 caracteres"):
            Usuario(
                nome=nome_longo,
                matricula="ALU12345",
                tipo=TipoUsuario.ALUNO
            )
    
    def test_rejeitar_matricula_curta(self):
        """[TDD] Deve rejeitar matrícula com menos de 5 caracteres"""
        with pytest.raises(ValueError, match="Matrícula deve ter entre 5 e 20 caracteres"):
            Usuario(
                nome="João Silva",
                matricula="A123",
                tipo=TipoUsuario.ALUNO
            )
    
    def test_rejeitar_matricula_longa(self):
        """[TDD] Deve rejeitar matrícula com mais de 20 caracteres"""
        with pytest.raises(ValueError, match="Matrícula deve ter entre 5 e 20 caracteres"):
            Usuario(
                nome="João Silva",
                matricula="A" * 21,
                tipo=TipoUsuario.ALUNO
            )
    
    def test_rejeitar_email_invalido(self):
        """[TDD] Deve rejeitar email em formato inválido"""
        with pytest.raises(ValueError, match="Email inválido"):
            Usuario(
                nome="João Silva",
                matricula="ALU12345",
                tipo=TipoUsuario.ALUNO,
                email="email_invalido"
            )
    
    def test_aceitar_email_none(self):
        """[TDD] Deve aceitar email None (opcional)"""
        usuario = Usuario(
            nome="João Silva",
            matricula="ALU12345",
            tipo=TipoUsuario.ALUNO,
            email=None
        )
        assert usuario.email is None


class TestUsuarioService:
    """Testes unitários do serviço de usuários"""
    
    @pytest.fixture
    def service(self):
        """Fixture para criar serviço limpo antes de cada teste"""
        return UsuarioService()
    
    def test_cadastrar_usuario_sucesso(self, service):
        """[TDD] Deve cadastrar usuário com sucesso"""
        usuario = service.cadastrar(
            nome="Maria Santos",
            matricula="PROF001",
            tipo="PROFESSOR",
            email="maria@email.com"
        )
        
        assert usuario.id == 1
        assert usuario.nome == "Maria Santos"
        assert usuario.matricula == "PROF001"
    
    def test_rejeitar_matricula_duplicada(self, service):
        """[TDD] Deve rejeitar matrícula duplicada"""
        service.cadastrar(
            nome="João Silva",
            matricula="ALU12345",
            tipo="ALUNO"
        )
        
        with pytest.raises(ValueError, match="Matrícula já cadastrada"):
            service.cadastrar(
                nome="Pedro Souza",
                matricula="ALU12345",
                tipo="ALUNO"
            )
    
    def test_rejeitar_email_duplicado(self, service):
        """[TDD] Deve rejeitar email duplicado"""
        service.cadastrar(
            nome="João Silva",
            matricula="ALU12345",
            tipo="ALUNO",
            email="joao@email.com"
        )
        
        with pytest.raises(ValueError, match="Email já cadastrado"):
            service.cadastrar(
                nome="Pedro Souza",
                matricula="ALU67890",
                tipo="ALUNO",
                email="joao@email.com"
            )
    
    def test_listar_usuarios(self, service):
        """[TDD] Deve listar todos os usuários cadastrados"""
        service.cadastrar("João Silva", "ALU001", "ALUNO")
        service.cadastrar("Maria Santos", "PROF001", "PROFESSOR")
        
        usuarios = service.listar()
        assert len(usuarios) == 2
    
    def test_buscar_usuario_por_id(self, service):
        """[TDD] Deve buscar usuário por ID"""
        usuario = service.cadastrar("João Silva", "ALU001", "ALUNO")
        
        encontrado = service.buscar_por_id(usuario.id)
        assert encontrado.nome == "João Silva"
    
    def test_buscar_usuario_inexistente(self, service):
        """[TDD] Deve retornar None para usuário inexistente"""
        usuario = service.buscar_por_id(999)
        assert usuario is None
    
    def test_atualizar_usuario(self, service):
        """[TDD] Deve atualizar dados de usuário existente"""
        usuario = service.cadastrar("João Silva", "ALU001", "ALUNO")
        
        atualizado = service.atualizar(
            usuario.id,
            nome="João Pedro Silva",
            email="joao.pedro@email.com"
        )
        
        assert atualizado.nome == "João Pedro Silva"
        assert atualizado.email == "joao.pedro@email.com"
    
    def test_remover_usuario(self, service):
        """[TDD] Deve remover usuário por ID"""
        usuario = service.cadastrar("João Silva", "ALU001", "ALUNO")
        
        resultado = service.remover(usuario.id)
        assert resultado is True
        assert service.buscar_por_id(usuario.id) is None
    
    def test_remover_usuario_inexistente(self, service):
        """[TDD] Deve retornar False ao remover usuário inexistente"""
        resultado = service.remover(999)
        assert resultado is False


class TestContratosIntegridade:
    """Testes de contrato e integridade de dados"""
    
    def test_contrato_campos_obrigatorios(self):
        """[CONTRATO] Usuário deve ter todos os campos obrigatórios"""
        usuario = Usuario(
            nome="João Silva",
            matricula="ALU12345",
            tipo=TipoUsuario.ALUNO
        )
        
        assert hasattr(usuario, 'id')
        assert hasattr(usuario, 'nome')
        assert hasattr(usuario, 'matricula')
        assert hasattr(usuario, 'tipo')
        assert hasattr(usuario, 'dataRegistro')
        assert hasattr(usuario, 'status')
    
    def test_contrato_tipo_usuario_enum(self):
        """[CONTRATO] TipoUsuario deve ser enum válido"""
        assert TipoUsuario.ALUNO.value == "ALUNO"
        assert TipoUsuario.PROFESSOR.value == "PROFESSOR"
        assert TipoUsuario.FUNCIONARIO.value == "FUNCIONARIO"
    
    def test_contrato_status_usuario_enum(self):
        """[CONTRATO] StatusUsuario deve ser enum válido"""
        assert StatusUsuario.ATIVO.value == "ATIVO"
        assert StatusUsuario.INATIVO.value == "INATIVO"
        assert StatusUsuario.SUSPENSO.value == "SUSPENSO"
    
    def test_contrato_data_registro_iso8601(self):
        """[CONTRATO] DataRegistro deve estar em formato ISO 8601"""
        usuario = Usuario(
            nome="João Silva",
            matricula="ALU12345",
            tipo=TipoUsuario.ALUNO
        )
        
        # Deve ser possível parsear como datetime
        data = datetime.fromisoformat(usuario.dataRegistro)
        assert isinstance(data, datetime)
    
    def test_contrato_serializacao_json(self):
        """[CONTRATO] Serialização JSON deve preservar tipos"""
        usuario = Usuario(
            nome="João Silva",
            matricula="ALU12345",
            tipo=TipoUsuario.ALUNO,
            email="joao@email.com"
        )
        
        dados = usuario.to_dict()
        
        assert isinstance(dados, dict)
        assert dados['nome'] == "João Silva"
        assert dados['matricula'] == "ALU12345"
        assert dados['tipo'] == "ALUNO"
        assert dados['status'] == "ATIVO"
        assert 'dataRegistro' in dados