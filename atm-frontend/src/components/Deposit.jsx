import React, { useState } from 'react';
import { Form, Input, Button, message } from 'antd';

function Deposit() {
  const [loading, setLoading] = useState(false);  // Để hiển thị trạng thái loading khi gửi yêu cầu

  const handleDeposit = async (values) => {
    setLoading(true);  // Bật trạng thái loading khi bắt đầu gửi yêu cầu
    const token = localStorage.getItem('token');

    const response = await fetch('http://localhost:5000/deposit', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,  // Gửi token trong header
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ account_id: values.account_id, amount: values.amount }),
    });

    const data = await response.json();

    if (response.status === 200) {
      message.success('Deposit successful');
    } else {
      message.error('Error: ' + data.error);
    }
    setLoading(false);  // Tắt trạng thái loading sau khi xử lý xong
  };

  return (
    <div style={{ maxWidth: '400px', margin: 'auto', paddingTop: '50px' }}>
      <h2>Deposit Money</h2>
      <Form 
        name="deposit" 
        onFinish={handleDeposit}  // Sự kiện gửi form
        layout="vertical"
      >
        <Form.Item
          label="Account ID"
          name="account_id"
          rules={[{ required: true, message: 'Please input your Account ID!' }]}
        >
          <Input placeholder="Enter your Account ID" />
        </Form.Item>

        <Form.Item
          label="Amount"
          name="amount"
          rules={[{ required: true, message: 'Please input the amount!' }]}
        >
          <Input type="number" placeholder="Enter amount to deposit" />
        </Form.Item>

        <Form.Item>
          <Button type="primary" htmlType="submit" loading={loading} block>
            Deposit
          </Button>
        </Form.Item>
      </Form>
    </div>
  );
}

export default Deposit;
