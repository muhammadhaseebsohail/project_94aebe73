Here is how you can create unit tests for the UserRegistration component using Jest and React Testing Library:

```jsx
// necessary imports
import React from 'react';
import { render, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom/extend-expect';
import UserRegistration from './UserRegistration'; // assuming we are in the same directory

// test suite for UserRegistration component
describe('UserRegistration', () => {
  // test for rendering the component
  it('renders correctly', () => {
    const { getByPlaceholderText } = render(<UserRegistration onSubmit={() => {}} />);
    expect(getByPlaceholderText('Username')).toBeInTheDocument();
    expect(getByPlaceholderText('Email')).toBeInTheDocument();
    expect(getByPlaceholderText('Password')).toBeInTheDocument();
  });

  // test for user interactions
  it('updates on input change and submits form data', () => {
    const onSubmitMock = jest.fn();

    const { getByPlaceholderText, getByText } = render(<UserRegistration onSubmit={onSubmitMock} />);

    fireEvent.change(getByPlaceholderText('Username'), { target: { value: 'testuser' } });
    fireEvent.change(getByPlaceholderText('Email'), { target: { value: 'test@test.com' } });
    fireEvent.change(getByPlaceholderText('Password'), { target: { value: 'testpass' } });

    fireEvent.click(getByText('Register'));

    expect(onSubmitMock).toBeCalledWith({
      username: 'testuser',
      email: 'test@test.com',
      password: 'testpass',
    });
  });

  // test for props validation - onSubmit is required
  it('throws an error when onSubmit prop is missing', () => {
    console.error = jest.fn();

    expect(() => {
      render(<UserRegistration />);
    }).toThrowError();

    expect(console.error).toHaveBeenCalled();
  });

  // test for edge cases - form validation error
  it('shows an error message when form validation fails', async () => {
    const onSubmitMock = jest.fn();
    const { getByPlaceholderText, getByText, findByText } = render(<UserRegistration onSubmit={onSubmitMock} />);

    fireEvent.change(getByPlaceholderText('Username'), { target: { value: 'testuser' } });
    fireEvent.change(getByPlaceholderText('Email'), { target: { value: 'test@test.com' } });
    // password field is left empty

    fireEvent.click(getByText('Register'));

    const errorMessage = await findByText(/please input password/i);

    expect(errorMessage).toBeInTheDocument();
    expect(onSubmitMock).not.toHaveBeenCalled();
  });
});
```

In the above tests:

- The first test checks if the form renders correctly by checking the presence of the input fields.
- The second test simulates user interactions by filling the form fields and clicking the submit button. It checks if the onSubmit mock function has been called with the correct form data.
- The third test checks if the component throws an error when the required onSubmit prop is missing.
- The last test checks the edge case where the form fails validation. It simulates partially filling the form and clicking the submit button, and checks if the error message is shown and onSubmit function is not called.