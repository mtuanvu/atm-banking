import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';  
import Login from './components/Login';
import Register from './components/Register';
import Deposit from './components/Deposit';
import Withdraw from './components/Withdraw';
import Transfer from './components/Transfer';
import TransactionHistory from './components/TransactionHistory';
import PrivateRoute from './components/PrivateRoute';
import AppHeader from './components/AppHeader';  // Import AppHeader

function App() {
  const token = localStorage.getItem('token');

  return (
    <Router>
      {/* Hiển thị AppHeader nếu người dùng đã đăng nhập */}
      {token && <AppHeader />}

      <Routes>
        <Route path="/" element={<Login />} />  {/* Đường dẫn đăng nhập */}
        <Route path="/register" element={<Register />} />  {/* Đường dẫn đăng ký */}
        
        {/* Sử dụng PrivateRoute để bảo vệ các route cần đăng nhập */}
        <Route path="/deposit" element={<PrivateRoute component={Deposit} />} />  {/* Bảo vệ route nạp tiền */}
        <Route path="/withdraw" element={<PrivateRoute component={Withdraw} />} />  {/* Bảo vệ route rút tiền */}
        <Route path="/transfer" element={<PrivateRoute component={Transfer} />} />  {/* Bảo vệ route chuyển tiền */}
        <Route path="/transactionHistory" element={<PrivateRoute component={TransactionHistory} />} />  {/* Bảo vệ route lịch sử giao dịch */}
      </Routes>
    </Router>
  );
}

export default App;
