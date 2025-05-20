Here is a basic example of a User Registration form in React:

```jsx
// necessary imports
import React, { useState } from 'react';
import PropTypes from 'prop-types';
import './UserRegistration.css'; // Importing CSS module

// component function
const UserRegistration = ({ onSubmit }) => {
    // form state
    const [formData, setFormData] = useState({
        username: '',
        email: '',
        password: '',
    });

    // error state
    const [error, setError] = useState('');

    // handling form field changes
    const handleInputChange = (e) => {
        setFormData({
            ...formData,
            [e.target.name]: e.target.value,
        });
    };

    // handling form submission
    const handleFormSubmit = (e) => {
        e.preventDefault();

        // basic validation
        for (let key in formData) {
            if (!formData[key]) {
                setError(`Please input ${key}`);
                return;
            }
        }

        // submit form
        onSubmit(formData);
    };

    return (
        <form className="user-registration" onSubmit={handleFormSubmit}>
            <input
                type="text"
                name="username"
                value={formData.username}
                onChange={handleInputChange}
                placeholder="Username"
            />
            <input
                type="email"
                name="email"
                value={formData.email}
                onChange={handleInputChange}
                placeholder="Email"
            />
            <input
                type="password"
                name="password"
                value={formData.password}
                onChange={handleInputChange}
                placeholder="Password"
            />
            <button type="submit">Register</button>
            {error && <p className="error">{error}</p>}
        </form>
    );
};

// prop types validation
UserRegistration.propTypes = {
    onSubmit: PropTypes.func.isRequired,
};

export default UserRegistration;
```

The CSS module `UserRegistration.css`:

```css
.user-registration {
    width: 300px;
    margin: 0 auto;
}

.user-registration input {
    display: block;
    width: 100%;
    margin-bottom: 10px;
    padding: 10px;
}

.user-registration button {
    display: block;
    width: 100%;
    padding: 10px;
    background-color: #007bff;
    color: white;
    border: none;
    cursor: pointer;
}

.user-registration .error {
    color: red;
    margin-top: 10px;
}
```

In the above code, the `UserRegistration` component is a form that takes user input for username, email, and password. User input is stored in the `formData` state. A simple validation is done before form submission to check if all fields are filled. If not, an error message is shown. The `onSubmit` function is passed as a prop to the component and is called when the form is successfully submitted.