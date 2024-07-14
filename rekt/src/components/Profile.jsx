import React from 'react'
import UserDetail from './c_profile/user_detail'
import UserAds from './c_profile/user_ads'
import { useNavigate } from 'react-router-dom';
import { useAuth } from './Auth';

const Profile = () => {

    const { setToken } = useAuth();
    const navigate = useNavigate();
  
    const handleLogout = () => {
      setToken();
      navigate("/", { replace: true });
    };
  return (
    <div>
        <UserDetail />
        <UserAds />
        <button className="m-1 btn btn-outline-primary" onClick={(e) => navigate("/new-ad", { replace: true })}>New Ad</button>
        <button className="m-1 btn btn-outline-primary" onClick={handleLogout}>Logout</button> 

    </div>
  )
}

export default Profile