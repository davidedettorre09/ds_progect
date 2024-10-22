import { jwtDecode } from 'jwt-decode';

// Funzione per ottenere il ruolo dell'utente dal token JWT
const getUserRole = () => {
    const token = localStorage.getItem('token');  // Puoi usare sessionStorage se preferisci non persistente
    if (!token) {
        return null;  // Se non c'è un token, l'utente non è autenticato
    }

    try {
        const decodedToken = jwtDecode(token);  // Decodifica il token JWT
        const role = decodedToken.role;  // Estrai il ruolo dal payload
        return role;  // Ritorna il ruolo (admin o client)
    } catch (error) {
        console.error('Errore nella decodifica del token JWT:', error);
        return null;  // In caso di errore, considera l'utente come non autenticato
    }
};

// Componente AdminRoute
const AdminRoute = ({ children }) => {
    const role = getUserRole();  // Recupera il ruolo dell'utente

    if (role === 'admin') {
        return <>{children}</>;  // Se l'utente è admin, ritorna il contenuto del child component
    } else {
        return (<>
        <div className="grid mt-4 text-center">
          <div className="col-100">
            <h3> You are not an Admin </h3>
          </div>
        </div>
        </>);  // Se l'utente non è admin, mostra un messaggio di errore
    }
};

export default AdminRoute;
