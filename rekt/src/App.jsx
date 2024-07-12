import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'

import Heh from './components/test'

function App() {
  const [count, setCount] = useState(0)

  return (
    <>
      <div>
        <Heh/>
      </div>
    </>
  )
}

export default App
