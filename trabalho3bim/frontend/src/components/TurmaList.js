import React, { useEffect, useState } from 'react';
import api from '../services/api';

const TurmaList = () => {
  const [turmas, setTurmas] = useState([]);

  useEffect(() => {
    const fetchTurmas = async () => {
      try {
        const response = await api.get('/turmas');
        setTurmas(response.data);
      } catch (error) {
        console.error('Erro ao buscar turmas:', error);
      }
    };

    fetchTurmas();
  }, []);

  return (
    <div>
      <h2>Lista de Turmas</h2>
      <ul>
        {turmas.map((turma) => (
          <li key={turma.id}>{turma.nome}</li>
        ))}
      </ul>
    </div>
  );
};

export default TurmaList;
