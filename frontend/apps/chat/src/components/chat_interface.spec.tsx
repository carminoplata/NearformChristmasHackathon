import { render } from '@testing-library/react';

import ChatInterface from './chat_interface';

describe('ChatInterface', () => {
  it('should render successfully', () => {
    const { baseElement } = render(<ChatInterface />);
    expect(baseElement).toBeTruthy();
  });
});
