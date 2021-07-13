import { message } from 'antd';
import {makeAutoObservable} from 'mobx';
import {URL_BASE} from './constents'

class User{
    idsid = null;
    raw = null;

    constructor() {
        this.idsid = window.localStorage.getItem('idsid');
        console.log(this.idsid)
        if (this.idsid !== null && this.idsid !== "null") {
            this.login(this.idsid);
        }
        makeAutoObservable(this)
    }

    register = (idsid, name, email) => {
        const url = encodeURI(`${URL_BASE}/user`)

        fetch(url, {
            method: "post",
            body: JSON.stringify({
                "id": idsid,
                "name": name,
                "email": email,
                "role": "user"
            }),
        }).then(response => {
            if (response.status !== 201) {
                response.text().then(err => message.error(err))
                return
            }
            message.info(`register user ${idsid} succeed!`)
        })
    }

    login = (idsid) => {
        if (idsid === null) {
            this.raw = null;
            return;
        }

        const url = encodeURI(`${URL_BASE}/user/${idsid}`)
        fetch(url).then(response => {
            if (response.status !== 200) {
                response.text().then(err => message.error(err))
                return
            }

            response.json().then(data => {
                this.idsid = data.idsid;
                this.raw = data;
                window.localStorage.setItem('idsid', idsid)
            });
        })
    }

    logout = () => {
        this.idsid = null;
        this.raw = null;
        window.localStorage.setItem('idsid', null);
    }
}

