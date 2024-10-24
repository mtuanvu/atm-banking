import React, { useEffect, useState } from 'react';
import { Table, message } from 'antd';
import axios from 'axios';

const fetchTransactionHistory = async () => {
  const token = localStorage.getItem('token'); // Lấy token từ localStorage
  try {
    const res = await axios.get('http://localhost:5000/transactions', {
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json",
      },
    });
    return res;
  } catch (error) {
    console.error('Failed to fetch transaction history:', error);
    throw error;
  }
};

const TransactionHistory = () => {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(false); // Trạng thái loading khi tải dữ liệu

  useEffect(() => {
    setLoading(true); // Bật trạng thái loading
    fetchTransactionHistory()
      .then((res) => {
        setData(res.data.transactions);
        setLoading(false); // Tắt trạng thái loading sau khi tải dữ liệu
      })
      .catch((error) => {
        message.error('Failed to fetch transaction history.');
        setLoading(false); // Tắt trạng thái loading khi có lỗi
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
      render: (amount) => `$${amount}`, // Hiển thị số tiền với ký hiệu đô la
    },
    {
      title: 'Date',
      dataIndex: 'date',
      key: 'date',
      render: (date) => new Date(date).toLocaleString(), // Hiển thị ngày tháng rõ ràng hơn
    },
  ];

  return (
    <div style={{ padding: '20px', paddingTop: "3rem" }}>
      <h2>Transaction History</h2>
      <Table
        dataSource={data}
        columns={columns}
        rowKey="id"
        loading={loading} // Trạng thái loading
        pagination={{ pageSize: 10 }} // Phân trang với số mục mỗi trang là 10
      />
    </div>
  );
};

export default TransactionHistory;
