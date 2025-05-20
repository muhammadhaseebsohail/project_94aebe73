Creating a React component for writing unit tests for frontend components is not really possible, as unit testing is not done within React components. However, I can guide you through creating a unit test for a simple React component using Jest and Enzyme. 

For instance, let's consider a simple Button component:

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

Now, we would write a unit test for this Button component:

```jsx
// Button.test.js
import React from 'react';
import { shallow } from 'enzyme';
import Button from './Button';

describe('<Button />', () => {
  it('renders without crashing', () => {
    shallow(<Button onClick={() => {}}>Click me!</Button>);
  });

  it('calls onClick prop when clicked', () => {
    const onClickMock = jest.fn();
    const wrapper = shallow(<Button onClick={onClickMock}>Click me!</Button>);

    wrapper.simulate('click');

    expect(onClickMock).toHaveBeenCalled();
  });
  
  it('matches snapshot', () => {
    const wrapper = shallow(<Button onClick={() => {}}>Click me!</Button>);

    expect(wrapper).toMatchSnapshot();
  });
});
```

In this test file, we're using Jest as our test runner and assertion library, and Enzyme to render our React components and simulate user interactions.

The first test ensures that the component renders without throwing an error. The second test ensures that when the button is clicked, it calls the onClick function passed in as a prop. The third test ensures that the rendered component matches a stored snapshot. If the component's output changes in the future, this test will fail, alerting us to the change.

Please note that this is a simplified example and real-world components and tests will likely be more complex.