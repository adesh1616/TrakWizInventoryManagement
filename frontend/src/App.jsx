// import React, { useState } from 'react';
// import axios from 'axios';

// const App = () => {
//   const [username, setUsername] = useState('');
//   const [password, setPassword] = useState('');
//   const [message, setMessage] = useState('');

//   const register = async () => {
//     try {
//       const res = await axios.post('http://127.0.0.1:8000/register/', {
//         username,
//         password,
//       });
//       setMessage('User registered successfully!');
//     } catch (err) {
//       setMessage('Error registering user');
//     }
//   };

//   const login = async () => {
//     try {
//       const res = await axios.post('http://127.0.0.1:8000/login/', {
//         username,
//         password,
//       });
//       localStorage.setItem('token', res.data.access_token);
//       setMessage('User logged in successfully!');
//     } catch (err) {
//       setMessage('Error logging in');
//     }
//   };

//   const getProtected = async () => {
//     try {
//       const token = localStorage.getItem('token');
//       const res = await axios.get('http://127.0.0.1:8000/protected/', {
//         headers: { Authorization: `Bearer ${token}` },
//       });
//       setMessage(res.data.message);
//     } catch (err) {
//       setMessage('Error accessing protected route');
//     }
//   };

//   return (
//     <div>
//       <input
//         type="text"
//         placeholder="Username"
//         onChange={(e) => setUsername(e.target.value)}
//       />
//       <input
//         type="password"
//         placeholder="Password"
//         onChange={(e) => setPassword(e.target.value)}
//       />
//       <button onClick={register}>Register</button>
//       <button onClick={login}>Login</button>
//       <button onClick={getProtected}>Access Protected Route</button>
//       <p>{message}</p>
//     </div>
//   );
// };

// export default App;


import React, { useState } from 'react';
import axios from 'axios';

const Inventory = () => {
  // Add your inventory management code here
};

const App = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  const register = async () => {
    try {
      const res = await axios.post('http://127.0.0.1:8000/register/', {
        username,
        password,
      });
      setMessage('User registered successfully!');
    } catch (err) {
      setMessage('Error registering user');
    }
  };

  const login = async () => {
    try {
      const res = await axios.post('http://127.0.0.1:8000/login/', {
        username,
        password,
      });
      localStorage.setItem('token', res.data.access_token);
      setMessage('User logged in successfully!');
      setIsLoggedIn(true);
    } catch (err) {
      setMessage('Error logging in');
    }
  };

  const getProtected = async () => {
    try {
      const token = localStorage.getItem('token');
      const res = await axios.get('http://127.0.0.1:8000/protected/', {
        headers: { Authorization: `Bearer ${token}` },
      });
      setMessage(res.data.message);
    } catch (err) {
      setMessage('Error accessing protected route');
    }
  };

  if (isLoggedIn) {
    return <Inventory />;
  }

  return (
    <div>
      <input
        type="text"
        placeholder="Username"
        onChange={(e) => setUsername(e.target.value)}
      />
      <br /> 
      <input
        type="password"
        placeholder="Password"
        onChange={(e) => setPassword(e.target.value)}
      />
      <br /> <button onClick={register}>Register</button>
      
      <br /> <button onClick={login}>Login</button>
      <br /> <button onClick={getProtected}>Access Protected Route</button>
      <p>{message}</p>
    </div>
  );
};

export default App;






// import React, { useState } from 'react';
// import axios from 'axios';

// const App = () => {
//   const [username, setUsername] = useState('');
//   const [password, setPassword] = useState('');
//   const [message, setMessage] = useState('');

//   const register = async () => {
//     try {
//       const res = await axios.post('http://127.0.0.1:8000/register/', {
//         username,
//         password,
//       });
//       setMessage('User registered successfully!');
//     } catch (err) {
//       setMessage('Error registering user');
//     }
//   };

//   const login = async () => {
//     try {
//       const res = await axios.post('http://127.0.0.1:8000/login/', {
//         username,
//         password,
//       });
//       localStorage.setItem('token', res.data.access_token);
//       setMessage('User logged in successfully!');
//     } catch (err) {
//       setMessage('Error logging in');
//     }
//   };

//   const getProtected = async () => {
//     try {
//       const token = localStorage.getItem('token');
//       const res = await axios.get('http://127.0.0.1:8000/protected/', {
//         headers: { Authorization: `Bearer ${token}` },
//       });
//       setMessage(res.data.message);
//     } catch (err) {
//       setMessage('Error accessing protected route');
//     }
//   };

//   return (
//     <div>
//       <input
//         type="text"
//         placeholder="Username"
//         onChange={(e) => setUsername(e.target.value)}
//       />
//       <input
//         type="password"
//         placeholder="Password"
//         onChange={(e) => setPassword(e.target.value)}
//       />
//       <button onClick={register}>Register</button>
//       <button onClick={login}>Login</button>
//       <button onClick={getProtected}>Access Protected Route</button>
//       <p>{message}</p>
//     </div>
//   );
// };

// export default App;

