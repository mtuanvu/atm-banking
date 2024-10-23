import React, { useState } from 'react';
import { Form, Input, Button, message } from 'antd';
import { depositMoney } from '../apiService';

const Deposit = () => {
  const [loading, setLoading] = useState(false);

  const onFinish = (values) => {
    setLoading(true);
    depositMoney(values)
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
    <Form name="deposit" onFinish={onFinish}>
      <Form.Item name="account_id" rules={[{ required: true, message: 'Please input your account ID!' }]}>
        <Input placeholder="Account ID" />
      </Form.Item>
      <Form.Item name="amount" rules={[{ required: true, message: 'Please input the amount!' }]}>
        <Input placeholder="Amount" type="number" />
      </Form.Item>
      <Form.Item>
        <Button type="primary" htmlType="submit" loading={loading}>
          Deposit
        </Button>
      </Form.Item>
    </Form>
  );
};

export default Deposit;
