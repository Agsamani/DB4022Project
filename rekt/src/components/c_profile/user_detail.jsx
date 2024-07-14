import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useAuth } from '../Auth';

const UserDetail = () => {
    const [detail, setDetail] = useState([]);

    useEffect(() => {
      axios.get('http://localhost:8000/api/user/detail')
        .then(response => setDetail(response.data))
        .catch(error => console.error('Error fetching detail:', error));
        
    }, []);
  
    return (
      <div>
        <h2>{detail.firstname} {detail.lastname}</h2>
        <h3>{detail.email}</h3>
        <h3>{detail.cname}</h3>
        
      </div>
    );
}

export default UserDetail