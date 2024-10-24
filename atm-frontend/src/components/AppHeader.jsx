import React, { useEffect, useState } from 'react';
import { Layout, Menu } from 'antd';
import { Link, useNavigate } from 'react-router-dom';
import { fetchAccountInfo } from './AccountService';

const { Header } = Layout;

const AppHeader = () => {
  const token = localStorage.getItem('token'); 
  const [accountId, setAccountId] = useState(localStorage.getItem('account_id') || '');
  const [balance, setBalance] = useState(localStorage.getItem('balance') || ''); 

  const navigate = useNavigate();

  useEffect(() => {
    const loadAccountInfo = async () => {
      if (token) { 
        try {
          const accountInfo = await fetchAccountInfo(); 
          if (accountInfo) {
            setAccountId(accountInfo.account_id);
            setBalance(accountInfo.balance);
            localStorage.setItem('account_id', accountInfo.account_id); 
            localStorage.setItem('balance', accountInfo.balance); 
          }
        } catch (error) {
          console.error("Error fetching account info:", error);
        }
      }
    };

    loadAccountInfo();
  }, [token]);

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('account_id');
    localStorage.removeItem('balance');
    setAccountId('');
    setBalance('');
    navigate('/login');
  };

  return (
    <Header>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <div className="logo" style={{ color: 'white', fontSize: '24px' }}>
          ATM Banking
        </div>
        <Menu theme="dark" mode="horizontal" defaultSelectedKeys={['1']}>
          {!token ? (
            <>
              <Menu.Item key="1">
                <Link to="/register">Register</Link>
              </Menu.Item>
              <Menu.Item key="2">
                <Link to="/">Login</Link>
              </Menu.Item>
            </>
          ) : (
            <>
              <Menu.Item key="3">
                <Link to="/deposit">Deposit</Link>
              </Menu.Item>
              <Menu.Item key="4">
                <Link to="/withdraw">Withdraw</Link>
              </Menu.Item>
              <Menu.Item key="5">
                <Link to="/transfer">Transfer</Link>
              </Menu.Item>
              <Menu.Item key="6">
                <Link to="/transactionHistory">History</Link>
              </Menu.Item>
              <Menu.Item key="7" onClick={handleLogout}>
                Logout
              </Menu.Item>
            </>
          )}
        </Menu>
        {token && (
          <div style={{ color: 'white', fontSize: '16px' }}>
            Account ID: {accountId} | Balance: ${balance}
          </div>
        )}
      </div>
    </Header>
  );
};

export default AppHeader;
