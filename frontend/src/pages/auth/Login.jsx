import { useState } from "react"
import './Login.css'
import userServices from "../../services/userServices"

const Login = () => {
    const [username, setUsername] = useState('')
    const [password, setPassword] = useState('')
    const { loginUser } = userServices;

    const loginHandler = async (e) => {
      e.preventDefault()

        try {
            const user = await loginUser({username: username, password: password});
            console.log('User:', user)
            // Redirect to dashboard page
        } catch (error) {
            console.error('Error:', error)
        } finally{
            setUsername('')
            setPassword('')
        }
    }

  return (
    <>
    <div className="grid text-center">
      <div className="col-100 mt-4">
        <h3> Login </h3>
        <form className="login-form" onSubmit={loginHandler}>
            <label  htmlFor="username">Username</label>
            <input type="text" id="username" name="username" required onChange={(e)=> setUsername(e.target.value)}/>
            <label htmlFor="password">Password</label>
            <input type="password" id="password" name="password" required onChange={(e)=> setPassword(e.target.value)}/>
            <button className="button">Login</button>
        </form>
      </div>
    </div>
    </>
  )
}

export default Login