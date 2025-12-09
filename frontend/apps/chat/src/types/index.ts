// Shared type definitions for the ElfAgent chat application

/**
 * Gift/Product information from marketplace search
 */
export interface Gift {
  id: string;
  name: string;
  marketplace: string;
  original_price?: number;
  current_price?: number;
  rating: number;
  image_url: string;
  order_url: string;
  availability: boolean;
}

/**
 * Message type for chat interface
 */
export interface Message {
  id: string;
  type: 'user' | 'buddy';
  text: string;
  products?: Gift[];
}

/**
 * API response from backend /api/query endpoint
 */
export interface ApiResponse {
  session_id: string;
  user_id: string;
  response: string;
  status: string;
}

/**
 * Props for ChatMessage component
 */
export interface ChatMessageProps {
  message: Message;
}

/**
 * Props for GiftCard component
 */
export interface GiftCardProps {
  product: Gift;
}
