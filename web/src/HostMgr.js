import React, { useState, useEffect } from 'react';
import {Table, Row, Col} from 'antd';

const HostList = (props) => {
    const [machines, setMachines] = useState({});
    const [ignoredMachines, setIgnoredMachines] = useState([]);

    const columns = [
        {
            title: 'Name',
            dataIndex: 'name',
            key: 'name',
        },
        {
            title: 'Connection',
            dataIndex: 'connection',
            key: 'connection',
        },
        {
            title: 'Occupied By',
            dataIndex: 'occupied_by',
            key: 'occupied_by',
        }
    ]

    useEffect(() => {
        const url = encodeURI("http://localhost:8000/machines");

        fetch(url).then(response => {
            if (response.status !== 200) {
                response.text().then(err => console.log(err))
                return
            }

            response.json().then(data => {
                setMachines(data)
            })
        })
    }, [ignoredMachines])

    return (
        <Row 
            style={{marginTop: "10vh"}}
            type="flex"
            justify="center"
        >
            <Col span={16}>
                <Table
                    dataSource={Object.values(machines)}
                    columns={columns}
                    pagination={false}
                />
            </Col>
        </Row>
    )
}


export default HostList;
export const MyName = "Yahui, HanNing";