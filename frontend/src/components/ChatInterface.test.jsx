To test the ChatInterface component, we will use Jest and @testing-library/react. We will also mock the 'socket.io-client' library with jest-mock. Our tests will cover component rendering, user interactions, props validation and edge cases.

Here is how you can do it:

```jsx
import React from 'react';
import { render, fireEvent, waitFor, screen } from '@testing-library/react';
import { act } from 'react-dom/test-utils';
import io from 'socket.io-client';
import ChatInterface from './ChatInterface'; // the path to your component

jest.mock('socket.io-client');

describe('ChatInterface', () => {
  let socket;

  beforeEach(() => {
    socket = {
      on: jest.fn(),
      emit: jest.fn(),
      disconnect: jest.fn(),
    };
    io.connect.mockReturnValue(socket);
  });

  test('renders without crashing', () => {
    render(<ChatInterface socketUrl="http://localhost:3000" />);
    expect(screen.getByRole('textbox')).toBeInTheDocument();
    expect(screen.getByRole('button')).toBeInTheDocument();
  });

  test('connects and disconnects the socket when mounting and unmounting', () => {
    const { unmount } = render(<ChatInterface socketUrl="http://localhost:3000" />);
    expect(io.connect).toHaveBeenCalledWith('http://localhost:3000');
    unmount();
    expect(socket.disconnect).toHaveBeenCalled();
  });

  test('sends a message when the form is submitted', () => {
    render(<ChatInterface socketUrl="http://localhost:3000" />);
    const input = screen.getByRole('textbox');
    const button = screen.getByRole('button');
    fireEvent.change(input, { target: { value: 'test message' } });
    fireEvent.click(button);
    expect(socket.emit).toHaveBeenCalledWith('message', { content: 'test message' });
  });

  test('does not send an empty message', () => {
    render(<ChatInterface socketUrl="http://localhost:3000" />);
    const button = screen.getByRole('button');
    fireEvent.click(button);
    expect(socket.emit).not.toHaveBeenCalled();
  });

  test('adds a received message to the list', async () => {
    render(<ChatInterface socketUrl="http://localhost:3000" />);
    act(() => {
      const messageHandler = socket.on.mock.calls[0][1];
      messageHandler({ content: 'test message' });
    });
    await waitFor(() => expect(screen.getByText('test message')).toBeInTheDocument());
  });

  test('throws an error if no socketUrl prop is provided', () => {
    console.error = jest.fn();
    expect(() => render(<ChatInterface />)).toThrowError();
    expect(console.error).toHaveBeenCalled();
  });
});
```

In these tests, we're first mocking the Socket.IO client so we can control its behavior. Then, we're testing whether the component renders correctly, connects and disconnects the socket when mounting and unmounting, sends messages when the form is submitted, doesn't send empty messages, adds received messages to the list, and throws an error if no `socketUrl` prop is provided. The `waitFor` function from `@testing-library/react` is used to wait for the message to be added to the list because this is done asynchronously.