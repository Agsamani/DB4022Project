import React, { useState } from 'react';
import axios from 'axios';
import { Range, getTrackBackground } from 'react-range';

const SearchForm = () => {
  const [searchData, setSearchData] = useState({
    title: '',
    minPrice: 0,
    maxPrice: 10000
  });
  const [priceRange, setPriceRange] = useState([0, 10000]);
  const [results, setResults] = useState([]);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setSearchData({
      ...searchData,
      [name]: value
    });
  };

  const handlePriceChange = (values) => {
    setPriceRange(values);
    setSearchData({
      ...searchData,
      minPrice: values[0],
      maxPrice: values[1]
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    const { title, minPrice, maxPrice } = searchData;
    const query = new URLSearchParams({
      title,
      minPrice,
      maxPrice
    }).toString();

    axios.get(`http://localhost:8000/api/adv/search?${query}`)
      .then(response => {
        setResults(response.data.results);
        console.log(response.data.results[0].hit);
      })
      .catch(error => {
        console.error('There was an error searching!', error);
      });
  };

  return (
    <div className="container mt-5">
      <h2>Search Advertisements</h2>
      <form onSubmit={handleSubmit}>
        <div className="mb-3">
          <label className="form-label">Title</label>
          <input 
            type="text" 
            className="form-control" 
            name="title" 
            value={searchData.title} 
            onChange={handleInputChange} 
          />
        </div>
        <div className="mb-3">
          <label className="form-label">Price Range</label>
          <Range
            values={priceRange}
            step={10000}
            min={0}
            max={1000000}
            onChange={handlePriceChange}
            renderTrack={({ props, children }) => (
              <div
                {...props}
                style={{
                  ...props.style,
                  height: '6px',
                  width: '100%',
                  background: getTrackBackground({
                    values: priceRange,
                    colors: ['#ccc', '#548BF4', '#ccc'],
                    min: 0,
                    max: 1000000
                  })
                }}
              >
                {children}
              </div>
            )}
            renderThumb={({ props }) => (
              <div
                {...props}
                style={{
                  ...props.style,
                  height: '20px',
                  width: '20px',
                  backgroundColor: '#548BF4'
                }}
              />
            )}
          />
          <div className="d-flex justify-content-between mt-2">
            <span>${priceRange[0]}</span>
            <span>${priceRange[1]}</span>
          </div>
        </div>
        <button type="submit" className="btn btn-primary">Search</button>
      </form>

      <div className="mt-5">
        <h3>Search Results</h3>
        {results.length > 0 ? (
          <ul className="list-group">
            {results.map((result) => (
              <li key={result.id} className="list-group-item">
                <h5>{result.hit.Title}</h5>
                <p>Price: ${result.hit.Price}</p>
              </li>
            ))}
          </ul>
        ) : (
          <p>No results found</p>
        )}
      </div>
    </div>
  );
};

export default SearchForm;
