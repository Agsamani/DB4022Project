
import React, { useEffect, useState } from 'react';
import axios from 'axios';



const Signup = () => {
  const [cities, setCities] = useState([]);

  useEffect(() => {
    axios.get('http://localhost:8000/api/get-cities')
      .then(response => setCities(response.data))
      .catch(error => console.error('Error fetching cities:', error));
  }, []);

  const [formData, setFormData] = useState({
    firstname: '',
    lastname: '',
    email: '',
    cityid: '',
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('http://localhost:8000/api/user/', formData);
      console.log('Data submitted successfully:', response.data);
    } catch (error) {
      console.error('Error submitting data:', error);
    }
  };

  return (
    <div className='d-flex justify-content-center'>
    <div className="w-50 p-3">
      <h2>Signup</h2>
      <form onSubmit={handleSubmit}>
        <div className='mb-3'>
          <label className='form-label'>First Name:</label>
          <input type="text" name="firstname" onChange={handleChange} className='form-control'/>
        </div>
        <div className='mb-3'>
          <label className='form-label'>Last Name:</label>
          <input type="text" name="lastname" onChange={handleChange} className='form-control'/>
        </div>
        <div className='mb-3'>
          <label className='form-label'>Email/Phone:</label>
          <input type="email" name="email" onChange={handleChange} className='form-control'/>
        </div>
        <div className='mb-3'>
          <label for="cityid" className='form-label'>City:</label>

          <select name="cityid" id="cars" onChange={handleChange} class="form-select">
            {cities.map(city => (
              <option value={city.cityid}>{city.cname}</option>
            ))}
          </select>
        </div>
        <button type="submit" className="btn btn-outline-primary">Signup</button>
      </form>
    </div>
    </div>
  );
};

export default Signup;