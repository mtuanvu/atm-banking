import React, { useState } from 'react';
import { Form, Input, Button, message } from 'antd';

const ChangePassword = () => {
    const [email, setEmail] = useState('');
    const [oldPassword, setOldPassword] = useState('');
    const [newPassword, setNewPassword] = useState('');

    const handleSubmit = async () => {
        const response = await fetch('http://localhost:5000/user/change-password', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ email, old_password: oldPassword, new_password: newPassword }),
        });

        if (response.ok) {
            message.success('Password changed successfully!');
            // Reset form fields
            setEmail('');
            setOldPassword('');
            setNewPassword('');
        } else {
            message.error('Failed to change password. Check old password and try again.');
        }
    };

    return (
        <div style={{ maxWidth: '400px', margin: 'auto' }}>
            <h2>Change Password</h2>
            <Form onFinish={handleSubmit} layout="vertical">
                <Form.Item
                    label="Email"
                    name="email"
                    rules={[{ required: true, message: 'Please input your email!' }]}
                >
                    <Input
                        value={email}
                        onChange={e => setEmail(e.target.value)}
                    />
                </Form.Item>
                <Form.Item
                    label="Old Password"
                    name="old_password"
                    rules={[{ required: true, message: 'Please input your old password!' }]}
                >
                    <Input.Password
                        value={oldPassword}
                        onChange={e => setOldPassword(e.target.value)}
                    />
                </Form.Item>
                <Form.Item
                    label="New Password"
                    name="new_password"
                    rules={[{ required: true, message: 'Please input your new password!' }]}
                >
                    <Input.Password
                        value={newPassword}
                        onChange={e => setNewPassword(e.target.value)}
                    />
                </Form.Item>
                <Form.Item>
                    <Button type="primary" htmlType="submit" block>
                        Change Password
                    </Button>
                </Form.Item>
            </Form>
        </div>
    );
};

export default ChangePassword;
