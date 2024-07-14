import React from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from './Auth';

const Navbar = () => {
  const { token } = useAuth();

  return (
    <nav className='navbar'>
      <h1>WOL</h1>
      <div>
        {!token ? <Link to="/login" type="button" className="m-1 btn btn-outline-primary nav-item">Login</Link> : <Link to="/profile" type="button" className="m-1 btn btn-outline-primary nav-item">Profile</Link>}
        {!token ? <Link to="/signup" type="button" className="m-1 btn btn-primary nav-item">Signup</Link> : <></>}
      </div>
    </nav>
  );
};

export default Navbar;