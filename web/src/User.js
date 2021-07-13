import React, {useState} from "react";
import { Row, Button, Form, Input, Tooltip} from "antd"
import {user} from './store'

export const RegisterForm = () => {
    const [idsid, setIdsid] = useState(null);
    const [email, setEmail] = useState(null);
    const [fullName, setFullName] = useState(null);

    return (
        <Row type="flex" justify="center">
            <Form
                labelCol={{span: 8}}
                wrapperCol={{span: 16}}
                labelAlign="left"
            >
                <Form.Item
                    label={<Tooltip title="Windows Username">IDSID</Tooltip>}
                    rules={[{ required: true, message: 'Please input your idsid!' }]}
                >
                    <Input
                        value={idsid}
                        onChange={e => setIdsid(e.target.value)}
                    />
                </Form.Item>

                <Form.Item
                    label="Email"
                    rules={[{ required: true, message: 'Please input your email!' }]}
                >
                    <Input
                        value={email}
                        onChange={e => setEmail(e.target.value)}
                    />
                </Form.Item>

                <Form.Item
                    label="Full Name"
                    rules={[{ required: true, message: 'Please input your full name!' }]}
                >
                    <Input
                        value={fullName}
                        onChange={e => setFullName(e.target.value)}
                    />
                </Form.Item>

                {/* Idsid:     {idsid}<br/>
                Email:     {email}<br/>
                Full Name: {fullName}<br/> */}

                <br/>

                <Button
                    type="primary"
                    block={true}
                    onClick={() => {
                        // message.info(idsid, 10)
                        // message.info(email, 10)
                        // message.info(fullName, 10)

                        user.register(idsid, fullName, email)
                    }}
                >
                    Register
                </Button>

                <br/>
                <br/>

                <a href="/">
                    <Button
                        type="primary"
                        block={true}
                    >
                        Back to Login Page!
                    </Button>
                </a>
            </Form>
        </Row>
    )
}

export const LoginForm = () => {
    const [idsid, setIdsid] = useState(null);
    
    return (
        <Row type="flex" justify="center" style={{marginTop: "10vh"}}>
            <Form
                labelCol={{span: 8}}
                wrapperCol={{span: 16}}
                labelAlign="left"
            >
                <Form.Item
                    label={<Tooltip title="Windows Username">IDSID</Tooltip>}
                    rules={[{ required: true, message: 'Please input your idsid!' }]}
                >
                    <Input
                        value={idsid}
                        onChange={e => setIdsid(e.target.value)}
                    />
                </Form.Item>

                <Button
                    block={true}
                    type="primary"
                    onClick={() => user.login(idsid)}
                >
                    Login
                </Button>
            </Form>
        </Row>
    )
}

export const LogoutBtn = () => {
    return (
        <Button
            type="danger"
            size="large"
            shape="round"
            onClick={() => user.logout()}
            style={{margin: "20px 20px"}}
        >
            Logout
        </Button>
    )
}
 
export const Head = () => {
    let button
    if (user.raw===null) {
        button=<div>
            <a href="/register">Register</a>
        </div>
    } else {
        button=<LogoutBtn/>
    }
    return (
        <Row type="flex" justify="end">
            {button}
            {/* <Button>Login</Button> */}
            {/* <Button>Register</Button> */}
            {/* <Button>Logout</Button> */}
        </Row>
    )
}