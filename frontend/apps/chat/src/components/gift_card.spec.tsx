import { render } from '@testing-library/react';

import ProductCard from './gift_card';

describe('ProductCard', () => {
  it('should render successfully', () => {
    const { baseElement } = render(<ProductCard />);
    expect(baseElement).toBeTruthy();
  });
});
