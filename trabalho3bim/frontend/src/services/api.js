import axios from 'axios';

const api = axios.create({
  baseURL: 'http://127.0.0.1:3000', // URL do backend Flask
});

export default api;
