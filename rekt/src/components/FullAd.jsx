import React from 'react'
import AdvertisementDetails from './AdDetail'
import { useNavigate, useParams } from 'react-router-dom';

const FullAd = () => {
    const { ad_id } = useParams(); 
    const navigate = useNavigate();

  return (
    <div>
        <AdvertisementDetails ad_id={ad_id}/>
        <button className="m-1 btn btn-outline-danger"onClick={(e) => navigate("/ad/" + ad_id + '/report/', { replace: true })}>Report</button>
    </div>
  )
}

export default FullAd