from relatorio_service import RelatorioService, RepositorioMock

def exibir_relatorio(titulo, dados):
    """Função auxiliar para formatar a exibição dos dados do relatório."""
    print("-" * 50)
    print(f"| {titulo.upper():^46} |")
    print("-" * 50)
    
    if not dados:
        print("| Relatório Vazio.                                 |")
        print("-" * 50)
        return

    if isinstance(dados[0], dict):
        # Exibição para Livros Mais Emprestados / Usuários Mais Ativos
        for item in dados:
            if 'titulo' in item:
                print(f"| Livro: {item['titulo'][:30]:<30} | Total: {item['totalEmprestimos']:<10} |")
            elif 'nome' in item:
                print(f"| Usuário: {item['nome'][:30]:<30} | Total: {item['totalEmprestimos']:<10} |")
    else:
        print("| Exibição de dados detalhada não implementada... |")
        
    print("-" * 50)


def menu_principal():
    """Simula o controller principal da aplicação."""
    # Usando o RepositorioMock para demonstrar o funcionamento do relatório
    service = RelatorioService(repositorio=RepositorioMock()) 
    
    while True:
        print("\n=== SGBU - Módulo de Relatórios ===")
        print("1. Relatório de Livros Mais Emprestados")
        print("2. Relatório de Usuários Mais Ativos")
        print("3. Contagem de Status de Acervo")
        print("4. Sair")
        
        escolha = input("Selecione uma opção: ")

        if escolha == '1':
            relatorio = service.gerar_relatorio_livros_mais_emprestados()
            exibir_relatorio("Livros Mais Emprestados", relatorio)
            
        elif escolha == '2':
            relatorio = service.gerar_relatorio_usuarios_mais_ativos()
            exibir_relatorio("Usuários Mais Ativos", relatorio)
            
        elif escolha == '3':
            contagem = service.contar_status_acervo()
            print("-" * 50)
            print(f"| {'STATUS DO ACERVO':^46} |")
            print("-" * 50)
            print(f"| Disponíveis: {contagem['disponivel']:<36} |")
            print(f"| Emprestados: {contagem['emprestado']:<36} |")
            print("-" * 50)
            
        elif escolha == '4':
            print("Encerrando o módulo de relatórios.")
            break
            
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == '__main__':
    menu_principal()