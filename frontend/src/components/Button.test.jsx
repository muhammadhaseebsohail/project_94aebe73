Sure, here is how you could test a button component using Jest and React Testing Library.

First, let's consider a simple button component:

```jsx
// Button.js
import React from 'react';
import PropTypes from 'prop-types';

const Button = ({ onClick, children }) => (
  <button type="button" onClick={onClick}>
    {children}
  </button>
);

Button.propTypes = {
  onClick: PropTypes.func.isRequired,
  children: PropTypes.node.isRequired,
};

export default Button;
```

Now, we can write a test for this Button component:

```jsx
// Button.test.js
import React from 'react';
import { render, fireEvent } from '@testing-library/react';
import Button from './Button';

describe('Button component', () => {
  it('renders button text', () => {
    const { getByText } = render(<Button onClick={() => {}}>Click me!</Button>);
    expect(getByText('Click me!')).toBeDefined();
  });

  it('handles click when button is clicked', () => {
    const handleClick = jest.fn();
    const { getByText } = render(<Button onClick={handleClick}>Click me!</Button>);
    fireEvent.click(getByText('Click me!'));
    expect(handleClick).toHaveBeenCalled();
  });

  it('does not crash when an invalid prop is provided', () => {
    // Suppress console error for this one test
    const consoleError = console.error;
    console.error = jest.fn();

    expect(() => {
      render(<Button onClick="not a function">Click me!</Button>);
    }).not.toThrow();

    // Restore console.error
    console.error = consoleError;
  });
});
```

In this test file, we're using Jest as our test runner and assertion library, and React Testing Library to render our React components and simulate user interactions.

The first test checks that the component renders the correct button text. The second test checks that when the button is clicked, it calls the onClick function passed in as a prop. The third test checks that the component does not crash even when an invalid prop is provided.

These tests cover the basic functionality of the Button component. Depending on the complexity of your components, you may need to write more tests to cover additional functionality and edge cases.