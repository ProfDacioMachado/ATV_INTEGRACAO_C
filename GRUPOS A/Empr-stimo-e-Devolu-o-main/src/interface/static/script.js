// Função para carregar empréstimos na tabela
async function carregarEmprestimos() {
  const tbody = document.querySelector("#loan-table tbody");
  if (!tbody) return;

  try {
    const resp = await fetch("/api/loans");
    const loans = await resp.json();
    
    tbody.innerHTML = "";
    
    if (loans.length === 0) {
      tbody.innerHTML = '<tr><td colspan="5" class="no-data">Nenhum empréstimo registrado</td></tr>';
      return;
    }
    
    loans.forEach(l => {
      const tr = document.createElement("tr");
      tr.innerHTML = `
        <td>${l.id}</td>
        <td>${l.user || 'N/A'}</td>
        <td>${l.book || 'N/A'}</td>
        <td>${l.status || 'Ativo'}</td>
        <td>${l.loan_date ? new Date(l.loan_date).toLocaleDateString('pt-BR') : 'N/A'}</td>
      `;
      tbody.appendChild(tr);
    });
  } catch (error) {
    tbody.innerHTML = '<tr><td colspan="5" class="no-data">Erro ao carregar empréstimos</td></tr>';
    console.error('Erro:', error);
  }
}

// Função para carregar lista de devoluções
async function carregarDevolucoes() {
  const returnList = document.querySelector("#return-list");
  if (!returnList) return;

  try {
    const resp = await fetch("/api/loans");
    const loans = await resp.json();
    
    returnList.innerHTML = "";
    
    // Filtrar apenas empréstimos ativos
    const activeLoans = loans.filter(l => l.status === 'Ativo' || !l.return_date);
    
    if (activeLoans.length === 0) {
      returnList.innerHTML = '<li class="no-data">Nenhum empréstimo ativo para devolução</li>';
      return;
    }
    
    activeLoans.forEach(l => {
      const li = document.createElement("li");
      li.innerHTML = `
        <div class="loan-info">
          <strong>ID ${l.id}</strong> - ${l.book || 'Livro'} (${l.user || 'Usuário'})
        </div>
        <button onclick="devolverLivro(${l.id})">Devolver</button>
      `;
      returnList.appendChild(li);
    });
  } catch (error) {
    returnList.innerHTML = '<li class="no-data">Erro ao carregar empréstimos</li>';
    console.error('Erro:', error);
  }
}

// Função para registrar devolução
async function devolverLivro(loanId) {
  const messageDiv = document.querySelector("#message");
  
  try {
    const resp = await fetch(`/api/loans/${loanId}/return`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      }
    });
    
    const result = await resp.json();
    
    if (resp.ok) {
      if (messageDiv) {
        messageDiv.innerHTML = '<p class="success">Devolução registrada com sucesso!</p>';
      }
      // Recarregar lista após 1 segundo
      setTimeout(() => {
        carregarDevolucoes();
        if (messageDiv) messageDiv.innerHTML = '';
      }, 1000);
    } else {
      if (messageDiv) {
        messageDiv.innerHTML = `<p class="error">Erro: ${result.error || 'Não foi possível registrar a devolução'}</p>`;
      }
    }
  } catch (error) {
    if (messageDiv) {
      messageDiv.innerHTML = '<p class="error">Erro ao processar devolução</p>';
    }
    console.error('Erro:', error);
  }
}

// Carregar dados ao carregar a página
document.addEventListener("DOMContentLoaded", () => {
  carregarEmprestimos();
  carregarDevolucoes();
});
