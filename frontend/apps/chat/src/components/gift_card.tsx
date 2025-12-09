import { Star, ShoppingCart } from 'lucide-react';
import type { GiftCardProps } from '../types';

export function GiftCard({ product }: GiftCardProps) {
  let discount = 0;
  if(product.original_price && product.current_price)
    discount = Math.round(((product.original_price - product.current_price) / product.original_price) * 100);


  return (
    <div className="bg-white rounded-lg border-2 border-yellow-400 p-4 hover:shadow-lg transition-shadow">
      <div className="flex gap-4">
        <div className="w-24 h-24 bg-gray-100 rounded-lg overflow-hidden flex-shrink-0">
          <img 
            src={product.image_url ? product.image_url : "https://images.unsplash.com/photo-1513885535751-8b9238bd345a?w=400&h=400&fit=crop"} 
            alt={product.name}
            className="w-full h-full object-cover"
          />
        </div>
        
        <div className="flex-1 min-w-0">
          <h3 className="text-gray-900 line-clamp-2 mb-1">
            {product.name}
          </h3>
          
          <div className="flex items-center gap-2 mb-2">
            <span className="inline-block px-2 py-1 bg-blue-100 text-blue-800 rounded text-sm">
              {product.marketplace}
            </span>
            <span className="inline-block px-2 py-1 rounded text-sm 'bg-green-100 text-green-800">
              In Stock
            </span>
          </div>
          
          <div className="flex items-center gap-1 mb-2">
            <Star className="w-4 h-4 fill-yellow-400 text-yellow-400" />
            <span className="text-gray-700">{product.rating}</span>
          </div>
          
          <div className="flex items-center gap-3">
            <div>
              <span className="text-green-700 mr-2">${product.current_price?.toFixed(2)}</span>
              {product.original_price && (
                <>
                  <span className="text-gray-500 line-through text-sm">
                    ${product.original_price.toFixed(2)}
                  </span>
                  <span className="ml-2 inline-block px-2 py-1 bg-red-100 text-red-800 rounded text-sm">
                    {discount}% OFF
                  </span>
                </>
              )}
            </div>
          </div>
        </div>
        
        <a 
          href={product.order_url} 
          target="_blank" 
          rel="noopener noreferrer"
          className="bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 transition-colors self-start flex items-center gap-2"
        >
          <ShoppingCart className="w-4 h-4" />
          <span>Order</span>
        </a>
      </div>
    </div>
  );
}
