import unittest
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from Model.User import User
from Model import model as md
import controler as ctl

class TestUserSimples(unittest.TestCase):
    
    def setUp(self):
        md.usuarios.clear()
        self.controller = ctl.Controler(True)
    
    def test_criar_usuario_sucesso(self):
        sucesso, resultado = self.controller.Ctr_Criar_Usuario(
            "João Silva", "12345", "ALUNO", "joao@email.com"
        )
        
        self.assertTrue(sucesso)
        self.assertEqual(resultado, "Usuário criado com sucesso")
        self.assertEqual(len(md.usuarios), 1)
    
    def test_buscar_usuario_por_id(self):
        self.controller.Ctr_Criar_Usuario("João Silva", "12345", "ALUNO")
        
        usuario = self.controller.Ctr_Buscar_Usuario_Por_Id(1)
        
        self.assertIsNotNone(usuario)
        self.assertEqual(usuario.get_nome(), "João Silva")
        self.assertEqual(usuario.get_matricula(), "12345")
    
    def test_buscar_usuario_por_matricula(self):
        self.controller.Ctr_Criar_Usuario("João Silva", "12345", "ALUNO")
        
        usuario = self.controller.Ctr_Buscar_Usuario_Por_Matricula("12345")
        
        self.assertIsNotNone(usuario)
        self.assertEqual(usuario.get_nome(), "João Silva")
    
    def test_listar_usuarios(self):
        self.controller.Ctr_Criar_Usuario("João Silva", "12345", "ALUNO")
        self.controller.Ctr_Criar_Usuario("Maria Santos", "67890", "PROFESSOR")
        
        usuarios = self.controller.Ctr_Listar_Usuarios()
        
        self.assertEqual(len(usuarios), 2)
        self.assertEqual(usuarios[0].get_nome(), "João Silva")
        self.assertEqual(usuarios[1].get_nome(), "Maria Santos")
    
    def test_atualizar_usuario_sucesso(self):
        self.controller.Ctr_Criar_Usuario("João Silva", "12345", "ALUNO")
        
        sucesso, resultado = self.controller.Ctr_Atualizar_Usuario(
            1, nome="João Santos", email="joao.santos@email.com"
        )
        
        self.assertTrue(sucesso)
        self.assertEqual(resultado, "Usuário atualizado com sucesso")
        
        usuario = self.controller.Ctr_Buscar_Usuario_Por_Id(1)
        self.assertEqual(usuario.get_nome(), "João Santos")
        self.assertEqual(usuario.get_email(), "joao.santos@email.com")
    
    def test_excluir_usuario_sucesso(self):
        self.controller.Ctr_Criar_Usuario("João Silva", "12345", "ALUNO")
        
        sucesso, resultado = self.controller.Ctr_Excluir_Usuario(1)
        
        self.assertTrue(sucesso)
        self.assertEqual(resultado, "Usuário excluído com sucesso")
        self.assertEqual(len(md.usuarios), 0)
    
    def test_buscar_usuarios_por_tipo(self):
        self.controller.Ctr_Criar_Usuario("João Silva", "12345", "ALUNO")
        self.controller.Ctr_Criar_Usuario("Maria Santos", "67890", "PROFESSOR")
        self.controller.Ctr_Criar_Usuario("Pedro Costa", "11111", "ALUNO")
        
        alunos = self.controller.Ctr_Buscar_Usuarios_Por_Tipo("ALUNO")
        
        self.assertEqual(len(alunos), 2)
        self.assertEqual(alunos[0].get_nome(), "João Silva")
        self.assertEqual(alunos[1].get_nome(), "Pedro Costa")
    
    def test_buscar_usuarios_por_status(self):
        self.controller.Ctr_Criar_Usuario("João Silva", "12345", "ALUNO")
        self.controller.Ctr_Criar_Usuario("Maria Santos", "67890", "PROFESSOR")
        
        self.controller.Ctr_Atualizar_Usuario(2, status="INATIVO")
        
        ativos = self.controller.Ctr_Buscar_Usuarios_Por_Status("ATIVO")
        
        self.assertEqual(len(ativos), 1)
        self.assertEqual(ativos[0].get_nome(), "João Silva")


if __name__ == '__main__':
    unittest.main(verbosity=2)