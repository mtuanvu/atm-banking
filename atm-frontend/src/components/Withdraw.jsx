import React, { useState } from 'react';
import { Form, Input, Button, message } from 'antd';
import axios from 'axios';  // Import axios trực tiếp vào đây

const Withdraw = () => {
  const [loading, setLoading] = useState(false);  // Trạng thái loading khi xử lý yêu cầu

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
    setLoading(true);  // Bật trạng thái loading khi bắt đầu xử lý
    withdrawMoney(values)
      .then((res) => {
        if (res && res.data && res.data.message) {
          message.success(res.data.message);  // Hiển thị thông báo thành công
        } else {
          message.error('Withdrawal failed');  // Hiển thị thông báo lỗi chung nếu không có phản hồi chi tiết từ server
        }
      })
      .catch((error) => {
        if (error.response && error.response.data && error.response.data.error) {
          message.error(error.response.data.error);  // Hiển thị thông báo lỗi từ server nếu có
        } else {
          message.error('Server error during withdrawal');  // Hiển thị lỗi máy chủ
        }
      })
      .finally(() => {
        setLoading(false);  // Tắt trạng thái loading sau khi xử lý xong
      });
  };

  return (
    <div style={{ maxWidth: '400px', margin: 'auto', paddingTop: '50px' }}>
      <h2>Withdraw Money</h2>
      <Form 
        name="withdraw" 
        onFinish={onFinish}  // Sự kiện gửi form
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
