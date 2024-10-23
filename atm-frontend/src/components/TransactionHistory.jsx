import React, { useEffect, useState } from 'react';
import { Table, message } from 'antd';
import { fetchTransactionHistory } from '../apiService';

const TransactionHistory = () => {
  const [data, setData] = useState([]);

  useEffect(() => {
    fetchTransactionHistory()
      .then((res) => {
        setData(res.data.transactions);
      })
      .catch((error) => {
        message.error('Failed to fetch transaction history.');
      });
  }, []);

  const columns = [
    {
      title: 'Account ID',
      dataIndex: 'account_id',
      key: 'account_id',
    },
    {
      title: 'Transaction Type',
      dataIndex: 'transaction_type',
      key: 'transaction_type',
    },
    {
      title: 'Amount',
      dataIndex: 'amount',
      key: 'amount',
    },
    {
      title: 'Date',
      dataIndex: 'date',
      key: 'date',
    },
  ];

  return <Table dataSource={data} columns={columns} rowKey="id" />;
};

export default TransactionHistory;
