import React, { useEffect, useState } from 'react';
import axios from 'axios';
import AdCard from '../AdCard';
import { Container, Row, Col } from 'react-bootstrap';

const UserAds = () => {
  const [ads, setAds] = useState([]);

  useEffect(() => {
    axios.get('http://localhost:8000/api/user/adv')
      .then(response => setAds(response.data))
      .catch(error => console.error('Error fetching products:', error));
      console.log(ads);
  }, []);

  return (
    <div className='list-group'>
      <h2>Advertisements</h2>
      <Container>
            <Row>
        {ads.map(product => (
            <Col>
              <AdCard {...product}/>
            </Col>
        ))}
        </Row> 
      </Container>
    </div>
  );
}

export default UserAds