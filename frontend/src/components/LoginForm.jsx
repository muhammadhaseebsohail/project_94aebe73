Here's the code for a simple functional Login Form component using React and hooks:

```jsx
import React, { useState } from 'react';
import PropTypes from 'prop-types';
import './LoginForm.css';

/**
 * LoginForm Functional Component
 * @param {Object} props 
 * @returns JSX.Element
 */
const LoginForm = ({ onSubmit }) => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState(null);

  const validateForm = () => {
    if (!username || !password) {
      setError('Please fill in all fields');
      return false;
    }
    return true;
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (validateForm()) {
      onSubmit({ username, password });
    }
  };

  return (
    <form className="login-form" onSubmit={handleSubmit}>
      <h2>Login</h2>
      {error && <div className="error">{error}</div>}
      <input 
        type="text" 
        placeholder="Username" 
        value={username} 
        onChange={e => setUsername(e.target.value)} 
      />
      <input 
        type="password" 
        placeholder="Password" 
        value={password} 
        onChange={e => setPassword(e.target.value)} 
      />
      <button type="submit">Submit</button>
    </form>
  );
};

LoginForm.propTypes = {
  onSubmit: PropTypes.func.isRequired,
};

export default LoginForm;
```

CSS styling for the component:

```css
/* LoginForm.css */
.login-form {
  display: flex;
  flex-direction: column;
  width: 300px;
  margin: 0 auto;
}

.login-form input {
  margin-bottom: 10px;
  padding: 10px;
}

.login-form button {
  padding: 10px;
}

.error {
  color: red;
  margin-bottom: 10px;
}
```

In this component, we are using local state to manage the form input values and error messages. The `validateForm` function checks if the username and password fields are filled in. If not, it sets an error message.

The `handleSubmit` function is called when the form is submitted. It prevents the default form submission event, validates the form, and if validation passes, calls the `onSubmit` prop with the username and password.