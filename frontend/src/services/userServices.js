import axiosInstance from "./axiosConfigUser";

const BASE_API_URL = process.env.REACT_APP_BASE_API_URL;

/**
 * Registers a new user with the provided user data.
 * @param {Object} userData - An object containing user registration data.
 * @returns {Object} - The server response data.
 * @throws Will throw an error if registration fails.
 */
const registerUser = async (userData) => {
  try {
    const response = await axiosInstance.post(`${BASE_API_URL}/users/`, userData);
    //console.log("Registration successful:", response.data);
    return response.data;
  } catch (error) {
    console.error("Error registering the user!", error);
    throw error;
  }
};


/**
 * Logs in the user and stores the JWT tokens (access and refresh) securely.
 * @param {Object} userData - An object containing user credentials (e.g., email and password).
 * @returns {Object} - The server response data containing the access and refresh tokens.
 * @throws Will throw an error if login fails.
 */
const loginUser = async (userData) => {
  try {
    const response = await axiosInstance.post(`${BASE_API_URL}/login/`, userData);

    // Destructure access and refresh tokens from the response
    const { access, refresh, } = response.data;

    if (access && refresh) {
      // Save the tokens in localStorage (you can also use secure cookies)
      localStorage.setItem('token', access);
      localStorage.setItem('refreshToken', refresh);
      //console.log("Logged in successfully. Tokens saved:", { access, refresh });
    } else {
      console.error('Authentication error: Tokens not provided');
      throw new Error('Authentication error: Tokens not provided');
    }

    return response.data;
  } catch (error) {
    console.error("Error logging in the user!", error);
    throw error;
  }
};

/**
 * Logs out the user and removes JWT tokens from storage.
 * @returns {Object} - The server response data.
 * @throws Will throw an error if logout fails.
 */
const logoutUser = async () => {
  try {
    //const response = await axiosInstance.post(`${BASE_API_URL}/logout/`);
    //console.log("Logged out successfully:", response.data);

    // Remove tokens from localStorage
    localStorage.removeItem("token");
    localStorage.removeItem("refreshToken");

    //console.log("Tokens removed from local storage");
    // return response.data;
    return
  } catch (error) {
    console.error("Error logging out the user!", error);
    throw error;
  }
};

export default {
  registerUser,
  loginUser,
  logoutUser,
};