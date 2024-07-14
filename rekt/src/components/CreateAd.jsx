import React, { useEffect, useState } from "react";
import axios from 'axios';
import { Form, Button } from 'react-bootstrap';


const CreateAd = () => {
    const [cities, setCities] = useState([]);

    useEffect(() => {
        axios
            .get("http://localhost:8000/api/get-cities")
            .then((response) => setCities(response.data))
            .catch((error) => console.error("Error fetching cities:", error));
    }, []);
    const [category, setCategory] = useState("");
    const [formData, setFormData] = useState({
        title: null,
        price: null,
        cityid: null,
        addesc: null,
        brand: null,
        material: null,
        productionYear: null,
        area: null,
        constructionDate: null,
        model: null,
        catid: "0"
    });
    const [photos, setPhotos] = useState([]);

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setFormData({
            ...formData,
            [name]: value,
        });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        const formDataWithPhotos = new FormData();

        photos.forEach(photo => {
            console.log(photo)
            formDataWithPhotos.append('images', photo);
        });

        for (const key in formData) {
            if (formData[key])
                formDataWithPhotos.append(key, formData[key]);
        }
        try {
            for (var key of formDataWithPhotos.entries()) {
                console.log(key[0] + ', ' + key[1]);
            }
          const response = await axios.post('http://localhost:8000/api/adv/', 
            Object.fromEntries(formDataWithPhotos), 
            {headers: {
                'Content-Type': 'multipart/form-data'
            }});
          console.log('Data submitted successfully:', response.data);
        } catch (error) {
          console.error('Error submitting data:', error);
        }
    };

    const handleFileChange = (e) => {
        
        setPhotos([...e.target.files]);
        console.log(photos)
    };

    return (
        <div className="container mt-5">
            <h2>Create Advertisement</h2>
            <form onSubmit={handleSubmit}>
                <div className="mb-3">
                    <label className="form-label">Title</label>
                    <input
                        type="text"
                        className="form-control"
                        name="title"
                        value={formData.title}
                        onChange={handleInputChange}
                        required
                    />
                </div>
                <div className="mb-3">
                    <label className="form-label">Price</label>
                    <input
                        type="number"
                        className="form-control"
                        name="price"
                        value={formData.price}
                        onChange={handleInputChange}
                        required
                    />
                </div>
                <div className="mb-3">
                <label for="cityid" className='form-label'>City:</label>

                    <select name="cityid" id="cars" onChange={handleInputChange} class="form-select">
                    {cities.map(city => (
                        <option value={city.cityid}>{city.cname}</option>
                    ))}
                    </select>
                </div>
                <div className="mb-3">
                    <label className="form-label">Description</label>
                    <textarea
                        className="form-control"
                        name="addesc"
                        value={formData.addesc}
                        onChange={handleInputChange}
                        required
                    />
                </div>
                <div className="mb-3">
                    <label className="form-label">Category</label>
                    <select
                        className="form-select"
                        name="catid"
                        value={category}
                        onChange={(e) => {setCategory(e.target.value); handleInputChange(e);} }
                        required
                    >
                        <option value="0">Other</option>
                        <option value="1">Home Appliance</option>
                        <option value="2">Vehicle</option>
                        <option value="3">Real State</option>
                        <option value="4">Digital product</option>
                    </select>
                </div>

                {category === "1" && (
                    <>
                        <div className="mb-3">
                            <label className="form-label">Brand</label>
                            <input
                                type="text"
                                className="form-control"
                                name="brand"
                                value={formData.brand}
                                onChange={handleInputChange}
                            />
                        </div>
                        <div className="mb-3">
                            <label className="form-label">Material</label>
                            <input
                                type="text"
                                className="form-control"
                                name="material"
                                value={formData.material}
                                onChange={handleInputChange}
                            />
                        </div>
                    </>
                )}

                {category === "2" && (
                    <>
                        <div className="mb-3">
                            <label className="form-label">Brand</label>
                            <input
                                type="text"
                                className="form-control"
                                name="brand"
                                value={formData.brand}
                                onChange={handleInputChange}
                            />
                        </div>
                        <div className="mb-3">
                            <label className="form-label">Production Year</label>
                            <input
                                type="number"
                                className="form-control"
                                name="productionYear"
                                value={formData.productionYear}
                                onChange={handleInputChange}
                            />
                        </div>
                    </>
                )}

                {category === "3" && (
                    <>
                        <div className="mb-3">
                            <label className="form-label">Area</label>
                            <input
                                type="text"
                                className="form-control"
                                name="area"
                                value={formData.area}
                                onChange={handleInputChange}
                            />
                        </div>
                        <div className="mb-3">
                            <label className="form-label">Construction Date</label>
                            <input
                                type="date"
                                className="form-control"
                                name="constructionDate"
                                value={formData.constructionDate}
                                onChange={handleInputChange}
                            />
                        </div>
                    </>
                )}

                {category === "4" && (
                    <>
                        <div className="mb-3">
                            <label className="form-label">Brand</label>
                            <input
                                type="text"
                                className="form-control"
                                name="brand"
                                value={formData.brand}
                                onChange={handleInputChange}
                            />
                        </div>
                        <div className="mb-3">
                            <label className="form-label">Model</label>
                            <input
                                type="text"
                                className="form-control"
                                name="model"
                                value={formData.model}
                                onChange={handleInputChange}
                            />
                        </div>
                    </>
                )}
                <Form.Group controlId="formPhotos">
                    <Form.Label>Upload Photos</Form.Label>
                    <Form.Control type="file" multiple onChange={handleFileChange} />
                    <Form.Text className="text-muted">
                    You can upload multiple photos.
                    </Form.Text>
                </Form.Group>

                <button type="submit" className="btn btn-primary">
                    Submit
                </button>
            </form>
        </div>
    );
};

export default CreateAd;
