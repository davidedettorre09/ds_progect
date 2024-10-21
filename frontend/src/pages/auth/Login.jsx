import { useState } from "react"
import './Login.css'

const Login = () => {
    const [username, setUsername] = useState('')
    const [password, setPassword] = useState('')

    const loginHandler = () => {

        try {
            console.log('Username:', username, 'Password:', password)
        } catch (error) {
            console.error('Error:', error)
        } finally{
            setUsername('')
            setPassword('')
        }
    }

  return (
    <>
    <div className="grid text-center mt-4">
      <div className="col-100">
        <h3> Login </h3>
        <form className="login-form" onSubmit={loginHandler}>
            <label  htmlFor="username">Username</label>
            <input type="text" id="username" name="username" required onChange={(e)=> setUsername(e.target.value)}/>
            <label htmlFor="password">Password</label>
            <input type="password" id="password" name="password" required onChange={(e)=> setPassword(e.target.value)}/>
            <button className="button" type="submit">Login</button>
        </form>
      </div>
    </div>
    </>
  )
}

export default Login