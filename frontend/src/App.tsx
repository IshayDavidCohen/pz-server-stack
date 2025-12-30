import { BrowserRouter, Routes, Route } from 'react-router-dom'
import Safehouse from './pages/Safehouse'
import Whitelister from './pages/Whitelister'
import VideoBackground from './components/VideoBackground'

function App() {
  return (
    <BrowserRouter>
      <VideoBackground />
      <Routes>
        <Route path="/" element={<Safehouse />} />
        <Route path="/whitelister" element={<Whitelister />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App

