import React, { useEffect, useState } from 'react';
import { Layout, Menu, message } from 'antd';
import { Link, useNavigate } from 'react-router-dom';
import { fetchAccountInfo } from './AccountService';  // Import the service

const { Header } = Layout;

const AppHeader = () => {
  const token = localStorage.getItem('token');  // Kiểm tra token từ localStorage
  const [accountId, setAccountId] = useState(localStorage.getItem('account_id') || '');  // Lấy Account ID từ localStorage
  const [balance, setBalance] = useState(localStorage.getItem('balance') || '');  // Lấy số dư từ localStorage

  const navigate = useNavigate();

  // Gọi API để lấy thông tin tài khoản và số dư khi component được render
  useEffect(() => {
    const loadAccountInfo = async () => {
      const accountInfo = await fetchAccountInfo();
      if (accountInfo) {
        setAccountId(accountInfo.account_id);
        setBalance(accountInfo.balance);
      }
    };

    loadAccountInfo();
  }, [token]);  // useEffect chỉ chạy khi token thay đổi

  const handleLogout = () => {
    localStorage.removeItem('token');  // Xóa token khi logout
    localStorage.removeItem('account_id');
    localStorage.removeItem('balance');
    setAccountId('');  // Reset state
    setBalance('');  // Reset state
    navigate('/login');  // Chuyển hướng về trang login
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
                <Link to="/register">Đăng ký</Link>
              </Menu.Item>
              <Menu.Item key="2">
                <Link to="/">Đăng nhập</Link>
              </Menu.Item>
            </>
          ) : (
            <>
              <Menu.Item key="3">
                <Link to="/deposit">Nạp tiền</Link>
              </Menu.Item>
              <Menu.Item key="4">
                <Link to="/withdraw">Rút tiền</Link>
              </Menu.Item>
              <Menu.Item key="5">
                <Link to="/transfer">Chuyển tiền</Link>
              </Menu.Item>
              <Menu.Item key="6">
                <Link to="/transactionHistory">Lịch sử giao dịch</Link>
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
