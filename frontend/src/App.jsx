import './App.css'
import {BrowserRouter, Route, Routes } from 'react-router-dom'
import Home from './pages/Home'
import Login from './pages/auth/Login'
import Navbar from'./components/Navbar'
import AdminDashboard from './pages/admin/AdminDashboard'
import MyDevices from './pages/client/MyDevices'
import AdminRoute from './components/AdminRoute'

function App() {

  return (
    <>
  <BrowserRouter>
    <Routes>
      <Route path='/' element={<><Navbar/><Home/></>}></Route>
      <Route path='/login' element={<><Navbar/><Login/></>}></Route>
      <Route path='/admin-dashboard' element={<><Navbar/><AdminRoute><AdminDashboard/></AdminRoute></>}></Route>
      <Route path='/my-devices' element={<><Navbar/><MyDevices/></>}></Route>

    </Routes>
  </BrowserRouter>
    </>
  )
}

export default App
