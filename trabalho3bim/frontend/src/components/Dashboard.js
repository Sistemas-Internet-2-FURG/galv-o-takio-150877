import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../services/api';

const Dashboard = () => {
  const [turmas, setTurmas] = useState([]);
  const [novaTurma, setNovaTurma] = useState('');
  const [mensagem, setMensagem] = useState('');
  const [erro, setErro] = useState('');
  const navigate = useNavigate();

  // Carrega as turmas ao montar o componente
  useEffect(() => {
    const fetchTurmas = async () => {
      try {
        const response = await api.get('/turmas', {
          headers: { Authorization: `Bearer ${localStorage.getItem('token')}` },
        });
        setTurmas(response.data);
      } catch (error) {
        console.error('Erro ao buscar turmas:', error);
        setErro('Erro ao carregar turmas.');
      }
    };

    fetchTurmas();
  }, []);

  // Adiciona uma nova turma
  const handleAddTurma = async (e) => {
    e.preventDefault();
    try {
      await api.post('/turmas', { nome: novaTurma }, {
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` },
      });

      // Atualiza a lista de turmas
      const response = await api.get('/turmas', {
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` },
      });
      setTurmas(response.data);
      setMensagem('Turma adicionada com sucesso!');
      setNovaTurma(''); // Limpa o campo de input
    } catch (error) {
      console.error('Erro ao adicionar turma:', error);
      setErro('Erro ao adicionar turma.');
    }
  };

  // Navega para a página de edição de turma
  const handleEditTurma = (id) => {
    navigate(`/edit-turma/${id}`);
  };

  return (
    <div style={styles.container}>
      <h2 style={styles.title}>Gerenciamento de Turmas</h2>
      {mensagem && <p style={{ color: 'green', textAlign: 'center' }}>{mensagem}</p>}
      {erro && <p style={{ color: 'red', textAlign: 'center' }}>{erro}</p>}

      {/* Tabela de Turmas */}
      <table style={styles.table}>
        <thead>
          <tr style={styles.tableHeader}>
            <th style={styles.tableCell}>ID</th>
            <th style={styles.tableCell}>Nome</th>
            <th style={styles.tableCell}>Ações</th>
          </tr>
        </thead>
        <tbody>
          {turmas.map((turma, index) => (
            <tr key={turma.id} style={index % 2 === 0 ? styles.tableRow : {}}>
              <td style={styles.tableCell}>{turma.id}</td>
              <td style={styles.tableCell}>{turma.nome}</td>
              <td style={styles.tableCell}>
                <button
                  style={styles.editButton}
                  onClick={() => handleEditTurma(turma.id)}
                >
                  Editar
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      {/* Formulário para adicionar turmas */}
      <form onSubmit={handleAddTurma} style={styles.form}>
        <input
          type="text"
          placeholder="Nome da turma"
          value={novaTurma}
          onChange={(e) => setNovaTurma(e.target.value)}
          required
          style={styles.input}
        />
        <button type="submit" style={styles.button}>
          Adicionar Turma
        </button>
      </form>
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
  editButton: {
    padding: '5px 10px',
    fontSize: '14px',
    backgroundColor: '#ffc107',
    color: '#fff',
    border: 'none',
    borderRadius: '5px',
    cursor: 'pointer',
    marginLeft: '5px',
  },
  input: {
    width: 'calc(100% - 110px)',
    padding: '10px',
    fontSize: '16px',
    marginRight: '10px',
    borderRadius: '5px',
    border: '1px solid #ddd',
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

export default Dashboard;
