import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';  
import Login from './components/Login';
import Register from './components/Register';
import Deposit from './components/Deposit';
import Withdraw from './components/Withdraw';
import Transfer from './components/Transfer';
import TransactionHistory from './components/TransactionHistory';
import PrivateRoute from './components/PrivateRoute';
import AppHeader from './components/AppHeader';

function App() {
  const token = localStorage.getItem('token');

  return (
    <Router>
      {<AppHeader />}

      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/register" element={<Register />} />
        
        <Route path="/deposit" element={<PrivateRoute component={Deposit} />} />
        <Route path="/withdraw" element={<PrivateRoute component={Withdraw} />} />
        <Route path="/transfer" element={<PrivateRoute component={Transfer} />} />
        <Route path="/transactionHistory" element={<PrivateRoute component={TransactionHistory} />} />
      </Routes>
    </Router>
  );
}

export default App;
