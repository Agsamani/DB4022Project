import React from 'react';
import { useNavigate } from "react-router-dom";
import { useAuth } from './Auth';
import { useState } from "react";
import axios from 'axios';


const Login = () => {
    const { setToken } = useAuth();
    const navigate = useNavigate();

    const [email, setEmail] = useState([]);
    const [otp, setOtp] = useState([]);

    const handleOtpRequest = async (e) => {
        e.preventDefault();
        try {
            const response = await axios.post('http://localhost:8000/api/get-otp/', email);
            console.log('Get Otp Success!', response.data);
        } catch (error) {
            console.error('Error Getting Otp:', error);
        }
    };

    const handleLogin = async (e) => {
        e.preventDefault();
        try {
            const response = await axios.post('http://localhost:8000/api/login/', {...email, ...otp});
            console.log('Login Success!', response.data.token);
            setToken(response.data.token);
            navigate("/", { replace: true });
        } catch (error) {
            console.error('Login Fail! :', error);
        }
    };

    return (
        <div className='d-flex justify-content-center'>

        <div className="border w-50 p-3 ">
            <h2>Login</h2>
            <form onSubmit={handleOtpRequest}>
            <div className='mb-3'>
                <label className='form-label'>Email:</label>
                <input type="text" name="email" onChange={(e) => {
                    const { name, value } = e.target;
                    setEmail({
                    [name]: value
                    });
                }} className='form-control'/>
            </div>
            <button type="submit" className="btn btn-outline-primary">Get OTP</button>
            </form>
            <form onSubmit={handleLogin}>
            <div className='mb-3'>
                <label className='form-label'>OTP:</label>
                <input type="number" name="otp" onChange={(e) => {
                    const { name, value } = e.target;
                    setOtp({
                    [name]: value
                    });
                }} className='form-control'/>
            </div>
            <button type="submit" className="btn btn-outline-primary">Login</button>
          </form>
        </div>
        </div>

    );
};

export default Login;