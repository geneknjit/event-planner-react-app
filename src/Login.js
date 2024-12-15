import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './Auth.css';

const Login = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [errorMessage, setErrorMessage] = useState('');
  const navigate = useNavigate();

  const handleLogin = (e) => {
    e.preventDefault();
    fetch(`${process.env.REACT_APP_API_BASE_URL}/api/login`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        email: email,
        password: password,
      }),
    })
    .then(response => response.json())
    .then(data => {
      if (data.redirect) {
        window.location.href = data.redirect;
      } else {
        setErrorMessage(data.message || 'Invalid email or password');
      }
    })
    .catch(error => {
      console.error('Error:', error);
      setErrorMessage('Failed to login');
    });
  };

  return (
    <div className="page-container">
      <div className="page-image"></div>
      <div className="auth-container">
        <form onSubmit={handleLogin} className="auth-form">
          <h2>Login</h2>
          <div className="input-group">
            <label>Email</label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>
          <div className="input-group">
            <label>Password</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>
          {errorMessage && <p className="error-message">{errorMessage}</p>}
          <button type="submit" className="btn">Login</button>
          <button type="button" className="btn secondary" onClick={() => navigate('/register')}>Register</button>
        </form>
      </div>
    </div>
  );
};

export default Login;