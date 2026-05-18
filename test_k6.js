import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
    stages: [
        { duration: '10s', target: 400 },
        { duration: '10s', target: 50 },
        { duration: '10s', target: 1300 }
    ]
};

export default function () {

// нагрузка на echo
    const echoPayload = JSON.stringify({
        "message": "hello",
        "number": 123
    });

    const params = {
        headers: {
            'Content-Type': 'application/json'
        }
    };

    const echoResponse = http.post(
        'http://localhost:5000/sendData', 
        echoPayload, 
        params
    );

    check(echoResponse, {
        'echo status is 200': (r) => r.status === 200,
    });

// нагрузка на sendData
    const sendDataPayload = JSON.stringify({
        age: 19,
        salary: 100,
        name: "robert"
    });

    const sendDataResponse = http.post(
        'http://localhost:5000/sendData', 
        sendDataPayload, 
        params
    );

    check(sendDataResponse, {
        'sendData status is 200': (r) => r.status === 200,
    });

    sleep(1);

}