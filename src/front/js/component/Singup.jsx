import React, { useState } from 'react';
import { Link } from 'react-router-dom';

const Signup = () => {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleSignup = () => {
    // Aquí puedes implementar la lógica para enviar los datos de registro al servidor
    // Por ejemplo, puedes hacer una solicitud HTTP utilizando fetch() o axios
    // y manejar la respuesta del servidor

    // Ejemplo básico de solicitud utilizando fetch():
    fetch('/api/signup', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ name, email, password }),
    })
      .then(response => response.json())
      .then(data => {
        // Aquí puedes manejar la respuesta del servidor
        // Por ejemplo, redireccionar al usuario a otra página o mostrar un mensaje de éxito/error
      })
      .catch(error => {
        // Aquí puedes manejar cualquier error de la solicitud
        console.error('Error:', error);
      });
  };

  return (
    <div className='container'>
      <h1>Signup</h1>
      <form>
        <div>
          <label>Name:</label>
          <input type="text" value={name} onChange={e => setName(e.target.value)} />
        </div>
        <div>
          <label>Email:</label>
          <input type="email" value={email} onChange={e => setEmail(e.target.value)} />
        </div>
        <div>
          <label>Password:</label>
          <input type="password" value={password} onChange={e => setPassword(e.target.value)} />
        </div>
        <button type="button" onClick={handleSignup}>Signup</button>
      </form>
      <p>Ya tienes una cuenta? <Link to="/">Inicia sesión aquí</Link></p>
    </div>
  );
};

export default Signup;