For testing, we will use Jest and React Testing Library. Here's the test suite for the `ActiveUserList` component:

```jsx
import React from 'react';
import { render, waitFor, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import ActiveUserList from './ActiveUserList';

// Mock fetch API
global.fetch = jest.fn(() =>
  Promise.resolve({
    json: () => Promise.resolve([
      { id: 1, name: 'User1', isActive: true },
      { id: 2, name: 'User2', isActive: false },
      { id: 3, name: 'User3', isActive: true },
    ]),
  })
);

beforeEach(() => {
  fetch.mockClear();
});

describe('<ActiveUserList />', () => {
  test('renders without crashing', () => {
    render(<ActiveUserList />);
    expect(screen.getByText('Loading...')).toBeInTheDocument();
  });

  test('renders active users', async () => {
    render(<ActiveUserList />);
    await waitFor(() => expect(fetch).toHaveBeenCalledTimes(1));
    expect(screen.getByText('User1')).toBeInTheDocument();
    expect(screen.getByText('User3')).toBeInTheDocument();
    expect(screen.queryByText('User2')).toBeNull();
  });

  test('handles errors', async () => {
    const errorMessage = 'Something went wrong';
    global.fetch = jest.fn(() => Promise.reject(new Error(errorMessage)));
    render(<ActiveUserList />);
    await waitFor(() => expect(fetch).toHaveBeenCalledTimes(1));
    expect(screen.getByText(`Error: ${errorMessage}`)).toBeInTheDocument();
  });
});
```

This test suite ensures that:
- The component renders without crashing
- Active users are rendered correctly, and inactive users are not rendered
- Errors are handled and displayed correctly

For this test suite to work, ensure that you have installed the necessary packages:

```bash
npm install --save @testing-library/react @testing-library/user-event jest
```

Remember to add Jest to your project if it's not already included:

```bash
npm install --save-dev jest
```