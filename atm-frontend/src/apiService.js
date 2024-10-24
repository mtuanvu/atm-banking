import axios from 'axios';

const API_URL = 'http://localhost:5000'; // Thay thế với địa chỉ server Flask của bạn

// Đăng ký người dùng
export const registerUser = (userData) => {
  return axios.post("${API_URL}/user/register", userData);
};

// Đăng nhập người dùng
export const loginUser = (loginData) => {
  return axios.post("${API_URL}/user/login", loginData);
};

// Nạp tiền
export const depositMoney = (data) => {
  return axios.post("${API_URL}/deposit", data);
};

// Rút tiền
export const withdrawMoney = async (data) => {
  return await axios.post('http://localhost:5000/transaction/withdraw', data, {
    headers: {
      'Authorization': `Bearer ${localStorage.getItem('token')}`
    }
  });
};

// Chuyển tiền
export const transferMoney = (data) => {
  return axios.post("${API_URL}/transfer", data);
};

// Lịch sử giao dịch
export const fetchTransactionHistory = () => {
  return axios.get("${API_URL}/transactions");
};