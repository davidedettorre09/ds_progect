import { useEffect, useState } from "react"
import { Link, useNavigate } from 'react-router-dom'
import './Navbar.css'
import userServices from "../services/userServices"

const Navbar = () => {
    const [menuOpened, setMenuOpened] = useState(false)
    const [isLoggedIn, setIsLoggedIn] = useState(false)
    const {logoutUser} = userServices
    const navigate = useNavigate()

    useEffect(()=>{
      const token = localStorage.getItem('token')
      if(token){
        setIsLoggedIn(true)
      } else {
        setIsLoggedIn(false)
      }
    }, [])

    const handleLogout = async () => {
      await logoutUser()
      setIsLoggedIn(false)
      navigate('/')
    }


  return (
    <>
    <header className="header">
      <div className="header__content">
        <Link className="header__logo" to={'/'}>
          <strong>MANAGEMENT</strong>
        </Link>
        <ul className="header__menu">
          <Link to={'/'}>Home</Link>
        </ul>
        <div className="header__quick">
        {isLoggedIn && <a onClick={handleLogout}>LOGOUT</a>}
        {!isLoggedIn && <Link to={'/login'}>LOGIN</Link>}
          <div onClick={()=>setMenuOpened(!menuOpened)} className="icon-hamburger">
            <span></span>
            <span></span>
          </div>
        </div>
      </div>
    </header>
    </>
  )
}

export default Navbar