import { render } from '@testing-library/react';

import Snowflakes from './snowflakes';

describe('Snowflakes', () => {
  it('should render successfully', () => {
    const { baseElement } = render(<Snowflakes />);
    expect(baseElement).toBeTruthy();
  });
});
