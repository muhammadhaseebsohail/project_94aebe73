Here's a simple example of a chat interface using React, Socket.IO client, and styled-components for styling. This component will render a chat interface that allows the user to input a message and see all messages displayed in real-time.

```jsx
import React, { useState, useEffect, useRef } from 'react';
import io from 'socket.io-client';
import PropTypes from 'prop-types';
import styled from 'styled-components';

const Container = styled.div`
  display: flex;
  flex-direction: column;
  height: 100vh;
`;

const MessageList = styled.ul`
  flex-grow: 1;
  overflow-y: scroll;
`;

const MessageListItem = styled.li`
  margin-bottom: 1em;
`;

const Input = styled.input`
  flex-grow: 0;
  height: 3em;
  padding: 0.5em;
`;

const Button = styled.button`
  flex-grow: 0;
  height: 3em;
  padding: 0.5em;
`;

const ChatInterface = ({ socketUrl }) => {
  const [message, setMessage] = useState('');
  const [messages, setMessages] = useState([]);
  const socketRef = useRef();

  useEffect(() => {
    socketRef.current = io.connect(socketUrl);
    socketRef.current.on('message', ({ content }) => {
      setMessages(prevMessages => [...prevMessages, content]);
    });
    return () => {
      socketRef.current.disconnect();
    };
  }, [socketUrl]);

  const handleSendMessage = (event) => {
    event.preventDefault();
    if (message !== '') {
      socketRef.current.emit('message', { content: message });
      setMessage('');
    }
  };

  return (
    <Container>
      <MessageList>
        {messages.map((message, index) => (
          <MessageListItem key={index}>{message}</MessageListItem>
        ))}
      </MessageList>
      <form onSubmit={handleSendMessage}>
        <Input
          type="text"
          value={message}
          onChange={e => setMessage(e.target.value)}
          placeholder="Type a message"
        />
        <Button type="submit">Send</Button>
      </form>
    </Container>
  );
};

ChatInterface.propTypes = {
  socketUrl: PropTypes.string.isRequired,
};

export default ChatInterface;
```

This component requires the `socketUrl` prop, which is the URL of the Socket.IO server. The messages are stored in a state array `messages` and the current input message is stored in the `message` state. When the component mounts, it opens a connection to the Socket.IO server and starts listening for 'message' events, adding any received messages to the `messages` array. When the component unmounts, it disconnects from the server. The `handleSendMessage` function is used to send a 'message' event to the server with the current input message when the form is submitted.