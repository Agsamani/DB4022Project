import React, { useEffect, useState } from 'react';
import axios from 'axios';
import AdCard from './AdCard';
import { Container, Row, Col } from 'react-bootstrap';

const AdvList = () => {
  const [products, setProducts] = useState([]);

  useEffect(() => {
    axios.get('http://localhost:8000/api/adv/latest')
      .then(response => setProducts(response.data))
      .catch(error => console.error('Error fetching products:', error));
      console.log(products);
  }, []);

  return (
    <div className='list-group'>
      <h2>Advertisements</h2>
      <Container>
            <Row>
        {products.map(product => (
            <Col>
              <AdCard {...product}/>
            </Col>
        ))}
        </Row> 
      </Container>
    </div>
  );
};

export default AdvList;