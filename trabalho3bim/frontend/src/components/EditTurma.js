import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import api from '../services/api';

const EditTurma = () => {
  const { id } = useParams(); // Obtém o ID da turma a partir da URL
  const navigate = useNavigate();
  const [turma, setTurma] = useState({});
  const [alunos, setAlunos] = useState([]);
  const [novoNome, setNovoNome] = useState('');
  const [novoAluno, setNovoAluno] = useState('');

  // Carrega os dados da turma e seus alunos
  useEffect(() => {
    const fetchTurma = async () => {
      try {
        const responseTurma = await api.get(`/turmas/${id}`, {
          headers: { Authorization: `Bearer ${localStorage.getItem('token')}` },
        });
        setTurma(responseTurma.data);
        setNovoNome(responseTurma.data.nome);

        const responseAlunos = await api.get(`/turmas/${id}/alunos`, {
          headers: { Authorization: `Bearer ${localStorage.getItem('token')}` },
        });
        setAlunos(responseAlunos.data);
      } catch (error) {
        console.error('Erro ao carregar turma ou alunos:', error);
      }
    };

    fetchTurma();
  }, [id]);

  // Atualiza o nome da turma
  const handleEditTurma = async () => {
    try {
      await api.put(`/turmas/${id}`, { nome: novoNome }, {
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` },
      });
    } catch (error) {
      console.error('Erro ao atualizar turma:', error);
    }
  };

  // Exclui a turma
  const handleDeleteTurma = async () => {
    if (window.confirm('Tem certeza que deseja excluir esta turma?')) {
      try {
        await api.delete(`/turmas/${id}`, {
          headers: { Authorization: `Bearer ${localStorage.getItem('token')}` },
        });
        navigate('/dashboard');
      } catch (error) {
        console.error('Erro ao excluir turma:', error);
      }
    }
  };

  // Exclui um aluno
  const handleDeleteAluno = async (alunoId) => {
    if (window.confirm('Tem certeza que deseja excluir este aluno?')) {
      try {
        await api.delete(`/alunos/${alunoId}`, {
          headers: { Authorization: `Bearer ${localStorage.getItem('token')}` },
        });
        setAlunos(alunos.filter((aluno) => aluno.id !== alunoId)); // Remove o aluno da lista
      } catch (error) {
        console.error('Erro ao excluir aluno:', error);
      }
    }
  };

  // Adiciona um novo aluno na turma
  const handleAddAluno = async () => {
    if (!novoAluno.trim()) {
      return;
    }

    try {
      const response = await api.post('/alunos', { nome: novoAluno, turma_id: id }, {
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` },
      });
      setAlunos([...alunos, response.data]); // Atualiza a lista de alunos
      setNovoAluno(''); // Limpa o campo de entrada
    } catch (error) {
      console.error('Erro ao adicionar aluno:', error);
    }
  };

  return (
    <div style={styles.container}>
      <h2 style={styles.title}>Editar Turma</h2>

      {/* Nome da turma e botões de ação */}
      <div style={styles.turmaInfo}>
        <strong>Nome da Turma:</strong>{' '}
        <input
          type="text"
          value={novoNome}
          onChange={(e) => setNovoNome(e.target.value)}
          style={styles.input}
        />
        <button style={styles.editButton} onClick={handleEditTurma}>
          Salvar Nome
        </button>
        <button style={styles.deleteButton} onClick={handleDeleteTurma}>
          Excluir Turma
        </button>
      </div>

      {/* Tabela de alunos */}
      <table style={styles.table}>
        <thead>
          <tr style={styles.tableHeader}>
            <th style={styles.tableCell}>ID</th>
            <th style={styles.tableCell}>Nome</th>
            <th style={styles.tableCell}>Ações</th>
          </tr>
        </thead>
        <tbody>
          {alunos.map((aluno, index) => (
            <tr key={aluno.id} style={index % 2 === 0 ? styles.tableRow : {}}>
              <td style={styles.tableCell}>{aluno.id}</td>
              <td style={styles.tableCell}>{aluno.nome}</td>
              <td style={styles.tableCell}>
                <button
                  style={styles.deleteButton}
                  onClick={() => handleDeleteAluno(aluno.id)}
                >
                  Excluir
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      {/* Formulário para adicionar aluno */}
      <div style={styles.addAluno}>
        <input
          type="text"
          placeholder="Nome do Aluno"
          value={novoAluno}
          onChange={(e) => setNovoAluno(e.target.value)}
          style={styles.input}
        />
        <button style={styles.addButton} onClick={handleAddAluno}>
          Adicionar Aluno
        </button>
      </div>

      <button style={styles.button} onClick={() => navigate('/dashboard')}>
        Voltar
      </button>
    </div>
  );
};

const styles = {
  container: {
    maxWidth: '800px',
    margin: '20px auto',
    padding: '20px',
    backgroundColor: '#f5f5f5',
    borderRadius: '10px',
    boxShadow: '0 4px 8px rgba(0, 0, 0, 0.1)',
  },
  title: {
    fontSize: '24px',
    marginBottom: '20px',
    textAlign: 'center',
    color: '#333',
  },
  turmaInfo: {
    display: 'flex',
    alignItems: 'center',
    gap: '10px',
    marginBottom: '20px',
  },
  input: {
    flex: 1,
    padding: '10px',
    fontSize: '16px',
    borderRadius: '5px',
    border: '1px solid #ddd',
  },
  editButton: {
    padding: '5px 10px',
    fontSize: '14px',
    backgroundColor: '#ffc107',
    color: '#fff',
    border: 'none',
    borderRadius: '5px',
    cursor: 'pointer',
  },
  deleteButton: {
    padding: '5px 10px',
    fontSize: '14px',
    backgroundColor: '#dc3545',
    color: '#fff',
    border: 'none',
    borderRadius: '5px',
    cursor: 'pointer',
  },
  addButton: {
    padding: '5px 10px',
    fontSize: '14px',
    backgroundColor: '#28a745',
    color: '#fff',
    border: 'none',
    borderRadius: '5px',
    cursor: 'pointer',
  },
  addAluno: {
    display: 'flex',
    alignItems: 'center',
    gap: '10px',
    marginBottom: '20px',
  },
  table: {
    width: '100%',
    borderCollapse: 'collapse',
    marginBottom: '20px',
    textAlign: 'left',
  },
  tableHeader: {
    backgroundColor: '#007BFF',
    color: '#fff',
    textAlign: 'left',
  },
  tableCell: {
    border: '1px solid #ddd',
    padding: '10px',
  },
  tableRow: {
    backgroundColor: '#f9f9f9',
  },
  button: {
    padding: '10px 20px',
    fontSize: '16px',
    backgroundColor: '#007BFF',
    color: '#fff',
    border: 'none',
    borderRadius: '5px',
    cursor: 'pointer',
  },
};

export default EditTurma;
