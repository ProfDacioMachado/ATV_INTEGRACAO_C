import unittest
import time
import os
from emprestimo import LoanController
from usuario_mock import UserStoreMock
from livro_mock import BookStoreMock

RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RESET = "\033[0m"
BOLD = "\033[1m"

def run_tests():
    loader = unittest.TestLoader()
    suite = loader.discover(start_dir=".", pattern="test_*.py")
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    return result

def show_tdd_cycle():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"{BOLD}🚀 Demo TDD - Módulo Empréstimo e Devolução\n{RESET}")
    time.sleep(1)
    print(f"{YELLOW}Etapa 1 - RED: execute testes antes de implementar mudanças{RESET}\n")
    time.sleep(1)
    print(f"{BOLD}Executando testes...\n{RESET}")
    result = run_tests()
    if not result.wasSuccessful():
        print(f"\n{RED}❌ Alguns testes falharam (como esperado no RED).{RESET}")
    else:
        print(f"\n{YELLOW}⚠️ Todos os testes passaram — verifique se você já implementou as mudanças.{RESET}")
    input("\nPressione ENTER para reexecutar (após mudanças simuladas) ...")
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"{YELLOW}Etapa 2 - GREEN: reexecute após implementação{RESET}\n")
    result = run_tests()
    if result.wasSuccessful():
        print(f"\n{GREEN}✅ Todos os testes passaram (GREEN).{RESET}")
    else:
        print(f"\n{RED}❌ Ainda há falhas.{RESET}")
        return
    time.sleep(1)
    print(f"\n{YELLOW}Etapa 3 - REFACTOR: com testes passando, refatore com segurança.{RESET}")
    print(f"{BOLD}{GREEN}\nFIM DA DEMONSTRAÇÃO TDD{RESET}")

if __name__ == "__main__":
    show_tdd_cycle()