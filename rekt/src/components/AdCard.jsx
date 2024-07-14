import React from 'react';
import { useNavigate } from 'react-router-dom';

const AdCard = ({ advertisementid, title, creationdate, price, imageid }) => {

    const navigate = useNavigate();

  return (
    <div className="card" style={{ width: '18rem' }} onClick={(e) => navigate("/ad/" + advertisementid, { replace: true })}>
      {imageid != null ? <img src={"http://localhost:8000/media/"+imageid+".png"} className="card-img-top" alt={title} /> : <></>}
      <div className="card-body">
        <h5 className="card-title">{title}</h5>
        <p className="card-text">Creation Date: {Date(creationdate)}</p>
        <p className="card-text">Price: ${price}</p>
      </div>
    </div>
  );
};

export default AdCard;