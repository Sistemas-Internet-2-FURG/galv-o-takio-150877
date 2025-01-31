import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Dashboard from './components/Dashboard';
import EditTurma from './components/EditTurma'; // Página de edição de turmas
import Login from './components/Login'; // Página de Login

function App() {
  return (
    <Router>
      <div>
        {/* Barra de navegação */}
        <nav style={styles.navbar}>
          <div style={styles.logo}>Gestão de Turmas e Alunos</div>
        </nav>

        {/* Rotas */}
        <Routes>
          {/* Página de Login */}
          <Route path="/" element={<Login />} />
          {/* Dashboard e Gerenciamento de Turmas */}
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/edit-turma/:id" element={<EditTurma />} />
          {/* Redireciona para a página inicial (Login) caso a rota não exista */}
          <Route path="*" element={<Navigate to="/" />} />
        </Routes>
      </div>
    </Router>
  );
}

const styles = {
  navbar: {
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#007BFF',
    color: '#fff',
    padding: '10px 20px',
    boxShadow: '0 4px 8px rgba(0, 0, 0, 0.1)',
  },
  logo: {
    fontSize: '20px',
    fontWeight: 'bold',
  },
};

export default App;
