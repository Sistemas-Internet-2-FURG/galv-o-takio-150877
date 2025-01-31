import React, { useEffect, useState } from 'react';
import api from '../services/api';

const AdminList = () => {
  const [admins, setAdmins] = useState([]);

  useEffect(() => {
    const fetchAdmins = async () => {
      try {
        const response = await api.get('/admins');
        setAdmins(response.data);
      } catch (error) {
        console.error('Erro ao buscar administradores:', error);
      }
    };

    fetchAdmins();
  }, []);

  return (
    <div>
      <h2>Lista de Administradores</h2>
      <ul>
        {admins.map((admin) => (
          <li key={admin.id}>{admin.usuario}</li>
        ))}
      </ul>
    </div>
  );
};

export default AdminList;
