import { useState } from "react"
import { Link } from 'react-router-dom'
import './Navbar.css'

const Navbar = () => {
    const [menuOpened, setMenuOpened] = useState(false)

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
        <Link to={'/login'}>LOGIN</Link>
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