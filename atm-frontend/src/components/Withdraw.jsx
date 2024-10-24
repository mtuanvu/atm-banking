import React, { useState } from 'react';
import { Form, Input, Button, message } from 'antd';
import axios from 'axios';

const Withdraw = () => {
  const [loading, setLoading] = useState(false);

  const withdrawMoney = async (data) => {
    try {
      const res = await axios.post('http://localhost:5000/withdraw', data, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`,
          'Content-Type': 'application/json'
        }
      });
      return res;
    } catch (error) {
      console.error('Error during withdrawal request:', error);
      throw error;
    }
  };

  const onFinish = (values) => {
    setLoading(true);
    withdrawMoney(values)
      .then((res) => {
        if (res && res.data && res.data.message) {
          message.success(res.data.message);
        } else {
          message.error('Withdrawal failed');
        }
      })
      .catch((error) => {
        if (error.response && error.response.data && error.response.data.error) {
          message.error(error.response.data.error);
        } else {
          message.error('Server error during withdrawal');
        }
      })
      .finally(() => {
        setLoading(false);
      });
  };

  return (
    <div style={{ maxWidth: '400px', margin: 'auto', paddingTop: '50px' }}>
      <h2>Withdraw Money</h2>
      <Form 
        name="withdraw" 
        onFinish={onFinish} 
        layout="vertical"
      >
        <Form.Item
          label="Account ID"
          name="account_id"
          rules={[{ required: true, message: 'Please input your account ID!' }]}
        >
          <Input placeholder="Enter your Account ID" />
        </Form.Item>

        <Form.Item
          label="Amount"
          name="amount"
          rules={[{ required: true, message: 'Please input the amount!' }]}
        >
          <Input type="number" placeholder="Enter amount to withdraw" />
        </Form.Item>

        <Form.Item>
          <Button type="primary" htmlType="submit" loading={loading} block>
            Withdraw
          </Button>
        </Form.Item>
      </Form>
    </div>
  );
};

export default Withdraw;
