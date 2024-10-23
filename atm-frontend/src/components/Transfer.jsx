import React, { useState } from 'react';
import { Form, Input, Button, message } from 'antd';
import { transferMoney } from '../apiService';

const Transfer = () => {
  const [loading, setLoading] = useState(false);

  const onFinish = (values) => {
    setLoading(true);
    transferMoney(values)
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
    <Form name="transfer" onFinish={onFinish}>
      <Form.Item name="from_account_id" rules={[{ required: true, message: 'Please input your account ID!' }]}>
        <Input placeholder="From Account ID" />
      </Form.Item>
      <Form.Item name="to_account_id" rules={[{ required: true, message: 'Please input the receiver account ID!' }]}>
        <Input placeholder="To Account ID" />
      </Form.Item>
      <Form.Item name="amount" rules={[{ required: true, message: 'Please input the amount!' }]}>
        <Input placeholder="Amount" type="number" />
      </Form.Item>
      <Form.Item>
        <Button type="primary" htmlType="submit" loading={loading}>
          Transfer
        </Button>
      </Form.Item>
    </Form>
  );
};

export default Transfer;
