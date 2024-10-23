import React, { useState } from 'react';
import { Form, Input, Button, message } from 'antd';
import { loginUser } from '../apiService';

const Login = () => {
  const [loading, setLoading] = useState(false);

  const onFinish = (values) => {
    setLoading(true);
    loginUser(values)
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
    <Form name="login" onFinish={onFinish}>
      <Form.Item name="email" rules={[{ required: true, message: 'Please input your email!' }]}>
        <Input placeholder="Email" />
      </Form.Item>
      <Form.Item name="password" rules={[{ required: true, message: 'Please input your password!' }]}>
        <Input.Password placeholder="Password" />
      </Form.Item>
      <Form.Item>
        <Button type="primary" htmlType="submit" loading={loading}>
          Login
        </Button>
      </Form.Item>
    </Form>
  );
};

export default Login;
