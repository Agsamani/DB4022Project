import { useState } from 'react'
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'

import AdvList from './components/AdvList'
import Navbar from './components/Navbar'
import Login from './components/Login';
import Signup from './components/Signup';
import AuthProvider from './components/Auth';
import Heh from './components/test';
import Profile from './components/Profile';
import CreateAd from './components/CreateAd';
import Search from './components/Search';
import AdvertisementDetails from './components/AdDetail';
import FullAd from './components/FullAd';
import ReportAdvertisement from './components/AdReport';


function App() {

  const [count, setCount] = useState(0)

  return (
    <Router>
      <AuthProvider>
        <Navbar />
        <Routes>
          <Route path="/profile" element={<Profile />} />
          <Route path="/search" element={<Search />} />
          <Route path="/ad/:ad_id/" element={<FullAd />} />
          <Route path="/ad/:ad_id/report" element={<ReportAdvertisement />} />

          <Route path="/new-ad" element={<CreateAd />} />
          <Route path="/login" element={<Login />} />
          <Route path="/signup" element={<Signup />} />
          <Route path="/" element={<AdvList />} />
        </Routes>
      </AuthProvider>
    </Router>
  )
}

export default App
