// src/components/Header.js
import React from 'react';
import { Layout, Menu } from 'antd';
import { Link } from 'react-router-dom';

const { Header } = Layout;

const AppHeader = () => {
    return (
        <Header>
            <div className="logo" style={{ color: 'white', fontSize: '24px' }}>
                ATM Banking
            </div>
            <Menu theme="dark" mode="horizontal" defaultSelectedKeys={['1']}>
                <Menu.Item key="1">
                    <Link to="/register">Đăng ký</Link>
                </Menu.Item>
                <Menu.Item key="2">
                    <Link to="/login">Đăng nhập</Link>
                </Menu.Item>
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
            </Menu>
        </Header>
    );
};

export default AppHeader;
