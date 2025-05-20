First, let's define a TypeScript interface for the User to ensure type safety:

```jsx
interface User {
  id: number;
  name: string;
  isActive: boolean;
}
```

Then let's create the `ActiveUserList` component:

```jsx
// Import necessary libraries
import React, { useState, useEffect } from 'react';

/**
 * ActiveUserList function component
 * @param {Object} props - React props
 * @returns {JSX.Element} Rendered component tree
 */
const ActiveUserList: React.FC = () => {
  // Define state variables
  const [users, setUsers] = useState<User[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Fetch users data from an API
  useEffect(() => {
    const fetchUsers = async () => {
      setLoading(true);
      try {
        const response = await fetch('https://api.example.com/users');
        const data = await response.json();
        setUsers(data.filter((user: User) => user.isActive));
      } catch (e) {
        setError(e);
      } finally {
        setLoading(false);
      }
    };

    fetchUsers();
  }, []);

  return (
    <div>
      {loading ? (
        <p>Loading...</p>
      ) : error ? (
        <p>Error: {error.message}</p>
      ) : (
        <ul>
          {users.map((user: User) => (
            <li key={user.id}>{user.name}</li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default ActiveUserList;
```

This component fetches a list of users from a given API, filters out the inactive ones, and displays them in a list. It also handles loading and error states.

For CSS styling, you can use CSS-in-JS or CSS modules. Here's a simple CSS-in-JS example using styled-components:

```jsx
import styled from 'styled-components';

const UserList = styled.ul`
  list-style-type: none;
  padding: 0;
`;

const UserListItem = styled.li`
  padding: 10px;
  border-bottom: 1px solid #ddd;
`;

// Then replace the <ul> and <li> in the render method with UserList and UserListItem
```

Note: Remember to install `styled-components` if you choose to use it:

```bash
npm install --save styled-components
```