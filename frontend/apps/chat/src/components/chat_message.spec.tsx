import { render } from '@testing-library/react';

import ChatMessage from './chat_message';

describe('ChatMessage', () => {
  it('should render successfully', () => {
    const { baseElement } = render(<ChatMessage />);
    expect(baseElement).toBeTruthy();
  });
});
