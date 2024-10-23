// src/App.js
import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom'; // Thay đổi đây
import { Layout } from 'antd';
import AppHeader from './components/Header';
import Register from './components/Register';
import Login from './components/Login';
import Deposit from './components/Deposit';
import Withdraw from './components/Withdraw';
import Transfer from './components/Transfer';
import TransactionHistory from './components/TransactionHistory';

const { Content } = Layout;

const App = () => {
    return (
        <Router>
            <Layout>
                <AppHeader />
                <Content style={{ padding: '0 50px', marginTop: 64 }}>
                    <Routes>
                        <Route path="/register" element={<Register />} />
                        <Route path="/login" element={<Login />} />
                        <Route path="/deposit" element={<Deposit />} />
                        <Route path="/withdraw" element={<Withdraw />} />
                        <Route path="/transfer" element={<Transfer />} />
                        <Route path="/transactionHistory" element={<TransactionHistory />} />
                    </Routes>
                </Content>
            </Layout>
        </Router>
    );
};

export default App;
