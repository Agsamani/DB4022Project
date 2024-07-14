import React, { useState } from "react";
import axios from 'axios';
import { useParams } from 'react-router-dom';
import { Form, Button, Container, Row, Col } from 'react-bootstrap';

const ReportAdvertisement = () => {
    const { ad_id } = useParams(); // Get ad_id from URL parameters
    const [catid, setCatId] = useState(0);
    const [rdesc, setRDesc] = useState('');
    const [error, setError] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();
        
        try {
            const response = await axios.post(`http://localhost:8000/api/adv/${ad_id}/report`, {
                catid,
                rdesc
            });
            console.log('Report submitted successfully:', response.data);
            // Optionally: Redirect to a success page or show a success message
        } catch (error) {
            console.error('Error submitting report:', error);
            setError('Failed to submit report. Please try again later.');
        }
    };

    return (
        <Container className="mt-5">
            <Row>
                <Col md={{ span: 6, offset: 3 }}>
                    <h2>Report Advertisement</h2>
                    <Form onSubmit={handleSubmit}>
                        <Form.Group className="mb-3">
                            <Form.Label>Category</Form.Label>
                            <Form.Control
                                as="select"
                                value={catid}
                                onChange={(e) => setCatId(e.target.value)}
                                required
                            >
                                <option value={0}>Select Category</option>
                                <option value={1}>Fraudulent</option>
                                <option value={2}>Offensive</option>
                                <option value={3}>Inappropriate Content</option>
                                {/* Add more categories as needed */}
                            </Form.Control>
                        </Form.Group>
                        <Form.Group className="mb-3">
                            <Form.Label>Description</Form.Label>
                            <Form.Control
                                as="textarea"
                                rows={3}
                                value={rdesc}
                                onChange={(e) => setRDesc(e.target.value)}
                                required
                            />
                        </Form.Group>
                        {error && <p className="text-danger">{error}</p>}
                        <Button variant="primary" type="submit">
                            Submit Report
                        </Button>
                    </Form>
                </Col>
            </Row>
        </Container>
    );
};

export default ReportAdvertisement;
