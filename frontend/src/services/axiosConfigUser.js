import axios from 'axios';

const BASE_API_URL = process.env.REACT_APP_BASE_API_URL_USER;

const axiosInstance = axios.create({
    baseURL: BASE_API_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

const authAxios = axios.create({
    baseURL: BASE_API_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

// Funzione per verificare se il token scaduto
const isTokenExpired = async (token) => {
    try {
        await authAxios.post("/token/verify/", { token });
        return false;  // Token valido
    } catch (error) {
        if (error.response && [401, 403].includes(error.response.status)) {
            return true;  // Token scaduto o non valido
        }
        console.error('Errore nella verifica del token:', error);
        throw error;
    }
};

// Funzione per aggiornare il token di accesso
const refreshAccessToken = async (refreshToken) => {
    try {
        const response = await authAxios.post("/token/refresh/", { refresh: refreshToken });
        return response.data.access;
    } catch (error) {
        console.error('Errore durante il refresh del token:', error);
        localStorage.removeItem('token');
        localStorage.removeItem('refreshToken');
        throw error;
    }
};

// Interceptor per gestire le richieste
axiosInstance.interceptors.request.use(
    async (config) => {
        const token = localStorage.getItem('token');
        const refreshToken = localStorage.getItem('refreshToken');

        //console.log('Interceptor: Token iniziale:', token);

        if (token) {
            try {
                const isExpired = await isTokenExpired(token);
                //console.log('Interceptor: Token scaduto:', isExpired);

                if (isExpired) {
                    const newAccessToken = await refreshAccessToken(refreshToken);
                    //console.log('Interceptor: Nuovo token di accesso:', newAccessToken);
                    localStorage.setItem('token', newAccessToken);
                    config.headers['Authorization'] = `Bearer ${newAccessToken}`;
                } else {
                    config.headers['Authorization'] = `Bearer ${token}`;
                }
            } catch (error) {
                console.error('Interceptor: Errore durante la gestione del token:', error);
                throw error;
            }
        }

        return config;
    },
    (error) => {
        console.error('Interceptor: Errore nella richiesta:', error);
        return Promise.reject(error);
    }
);

export default axiosInstance;