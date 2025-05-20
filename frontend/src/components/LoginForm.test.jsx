Here is a set of comprehensive unit tests for the LoginForm component using Jest and React Testing Library.

```jsx
import React from 'react';
import { render, fireEvent, screen } from '@testing-library/react';
import '@testing-library/jest-dom/extend-expect';
import LoginForm from './LoginForm';

describe('LoginForm', () => {
  const mockSubmit = jest.fn();

  beforeEach(() => {
    render(<LoginForm onSubmit={mockSubmit} />);
  });

  it('renders without crashing', () => {
    expect(screen.getByRole('form')).toBeInTheDocument();
    expect(screen.getByPlaceholderText('Username')).toBeInTheDocument();
    expect(screen.getByPlaceholderText('Password')).toBeInTheDocument();
    expect(screen.getByRole('button')).toBeInTheDocument();
  });

  it('does not submit the form if fields are empty', () => {
    fireEvent.click(screen.getByRole('button'));
    expect(screen.getByText('Please fill in all fields')).toBeInTheDocument();
    expect(mockSubmit).not.toHaveBeenCalled();
  });

  it('submits the form if fields are filled', () => {
    const usernameInput = screen.getByPlaceholderText('Username');
    const passwordInput = screen.getByPlaceholderText('Password');

    fireEvent.change(usernameInput, { target: { value: 'testuser' } });
    fireEvent.change(passwordInput, { target: { value: 'testpassword' } });
    
    fireEvent.click(screen.getByRole('button'));
    expect(mockSubmit).toHaveBeenCalledWith({ username: 'testuser', password: 'testpassword' });
    expect(mockSubmit).toHaveBeenCalledTimes(1);
  });

  it('clears error message on input change', () => {
    fireEvent.click(screen.getByRole('button'));
    expect(screen.getByText('Please fill in all fields')).toBeInTheDocument();

    const usernameInput = screen.getByPlaceholderText('Username');
    fireEvent.change(usernameInput, { target: { value: 'testuser' } });

    expect(screen.queryByText('Please fill in all fields')).toBeNull();
  });
});
```

These tests ensure:
- `LoginForm` renders without crashing, displaying all expected elements.
- The form does not submit when fields are empty and an error message is displayed.
- The form submits correctly when fields are filled and the `onSubmit` prop is called with the correct arguments.
- The error message is cleared when user starts typing in the input fields after an error.

The test setup imports necessary libraries and mocks the `onSubmit` prop. The `beforeEach` block renders the component before each test to ensure a fresh instance for each test case.