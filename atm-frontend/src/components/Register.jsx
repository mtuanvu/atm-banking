import React, { useState } from 'react';
import { Form, Input, Button, message } from 'antd';
import { registerUser } from '../apiService';

const Register = () => {
  const [loading, setLoading] = useState(false);

  const onFinish = (values) => {
    setLoading(true);
    registerUser(values)
      .then((res) => {
        message.success(res.data.message);
      })
      .catch((error) => {
        message.error(error.response.data.error);
      })
      .finally(() => {
        setLoading(false);
      });
  };

  return (
    <Form name="register" onFinish={onFinish}>
      <Form.Item name="name" rules={[{ required: true, message: 'Please input your name!' }]}>
        <Input placeholder="Name" />
      </Form.Item>
      <Form.Item name="email" rules={[{ required: true, message: 'Please input your email!' }]}>
        <Input placeholder="Email" />
      </Form.Item>
      <Form.Item name="password" rules={[{ required: true, message: 'Please input your password!' }]}>
        <Input.Password placeholder="Password" />
      </Form.Item>
      <Form.Item>
        <Button type="primary" htmlType="submit" loading={loading}>
          Register
        </Button>
      </Form.Item>
    </Form>
  );
};

export default Register;
