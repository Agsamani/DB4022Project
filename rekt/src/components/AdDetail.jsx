import React, { useEffect, useState } from "react";
import axios from 'axios';
import { useParams } from 'react-router-dom';
import { Carousel, Container, Row, Col, Card } from 'react-bootstrap';

const AdvertisementDetails = ({ad_id}) => {
    
    const [advertisement, setAdvertisement] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        axios
            .get(`http://localhost:8000/api/adv/${ad_id}/`)
            .then((response) => {
                setAdvertisement(response.data[0]);
                setLoading(false);
                console.log(response.data[0])
            })
            .catch((error) => {
                console.error("Error fetching advertisement details:", error);
                setLoading(false);
            });
    }, [ad_id]);

    if (loading) {
        return <div>Loading...</div>;
    }

    if (!advertisement) {
        return <div>Error loading advertisement details.</div>;
    }

    return (
        <Container>
            <Row>
                <Col md={8} class="h-10">
                    {advertisement.imageid != null ? <Carousel>
                        {
                            <Carousel.Item key={0}>
                                <img
                                    className="d-block w-100"
                                    src={"http://localhost:8000/media/"+advertisement.imageid+".png"} 
                                    alt={`Slide ${0}`}
                                />
                            </Carousel.Item>
                        }
                    </Carousel> : <h3>No Images</h3>}
                </Col>
                <Col md={4}>
                    <Card>
                        <Card.Body>
                            <Card.Title>{advertisement.title}</Card.Title>
                            <Card.Subtitle className="mb-2 text-muted">Price: ${advertisement.price}</Card.Subtitle>
                            <Card.Text>
                                <strong>Description:</strong> {advertisement.addesc}
                            </Card.Text>
                            <Card.Text>
                                <strong>Category:</strong> {advertisement.catid}
                            </Card.Text>
                            <Card.Text>
                                <strong>City:</strong> {advertisement.cityid}
                            </Card.Text>
                            {advertisement.brand && (
                                <Card.Text>
                                    <strong>Brand:</strong> {advertisement.brand}
                                </Card.Text>
                            )}
                            {advertisement.material && (
                                <Card.Text>
                                    <strong>Material:</strong> {advertisement.material}
                                </Card.Text>
                            )}
                            {advertisement.productionYear && (
                                <Card.Text>
                                    <strong>Production Year:</strong> {advertisement.productionYear}
                                </Card.Text>
                            )}
                            {advertisement.area && (
                                <Card.Text>
                                    <strong>Area:</strong> {advertisement.area}
                                </Card.Text>
                            )}
                            {advertisement.constructionDate && (
                                <Card.Text>
                                    <strong>Construction Date:</strong> {advertisement.constructionDate}
                                </Card.Text>
                            )}
                            {advertisement.model && (
                                <Card.Text>
                                    <strong>Model:</strong> {advertisement.model}
                                </Card.Text>
                            )}
                            <Card.Text>
                                <small className="text-muted">Created on: {new Date(advertisement.creationdate).toLocaleDateString()}</small>
                            </Card.Text>
                        </Card.Body>
                    </Card>
                </Col>
            </Row>
        </Container>
    );
};

export default AdvertisementDetails;
