import './App.css'
import {BrowserRouter, Route, Routes } from 'react-router-dom'
import Home from './pages/Home'
import Login from './pages/auth/Login'
import Navbar from'./components/Navbar'

function App() {

  return (
    <>
  <BrowserRouter>
  <Navbar/>
    <Routes>
      <Route path='/' element={<Home/>}></Route>
      <Route path='/login' element={<Login/>}></Route>

    </Routes>
  </BrowserRouter>
    </>
  )
}

export default App
