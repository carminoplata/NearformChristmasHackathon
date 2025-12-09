'use client'
import { useState, useRef, useEffect } from 'react';
import { Send } from 'lucide-react';
import { ChatMessage } from './chat_message';
import { GiftCard } from './gift_card';
import { config } from '../lib/config';
import type { Message, ApiResponse, Gift } from '../types';

const initialMessage: Message = {
  id: '1',
  type: 'buddy',
  text: "SANTA CLAUS! SANTA CLAUS! OH MY GOSH! It's really you! I'm Buddy the Elf, and I'm here to help you find the BEST Christmas presents in the whole wide world! Just tell me what gift you're looking for, and I'll search through ALL the marketplaces faster than you can say 'MERRY CHRISTMAS!!!' 🎅✨",
};

export function ChatInterface() {
  const [messages, setMessages] = useState<Message[]>([initialMessage]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [userId, setUserId] = useState<string | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const parseGiftsFromResponse = (json: any): Gift[] => {
    try {
      if('gifts' in json){
        return json.gifts.map((gift: any, index: number) => ({
          id: gift.id || `gift-${Date.now()}-${index}`,
          name: gift.name || 'Unknown Product',
          marketplace: gift.marketplace || 'Unknown',
          current_price: parseFloat(gift.current_price),
          original_price: gift.original_price ? parseFloat(gift.original_price) : undefined,
          rating: parseFloat(gift.rating || gift.product_star_rating || 0),
          image_url: gift.image_url || gift.product_image || gift.product_photo || '',
          order_url: gift.order_url || gift.product_url || '#',
          availability: true,
        }));
      }else{
        return [];
      }
    } catch (error) {
      console.error('Error parsing gifts from response:', error);
      return [];
    }
  };

  const searchGifts = async (query: string): Promise<{ text: string; gifts: Gift[] }> => {
    try {
      const response = await fetch(`${config.apiUrl}/api/query`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          query,
          user_id: userId,
          session_id: sessionId,
        }),
      });

      if (!response.ok) {
        return {
          text: "OH NO! Something went wrong with the North Pole's computer system! 😱 Can you try asking me again? I promise I'll do better!",
          gifts: []
        }
      }

      const data: ApiResponse = await response.json();
    
      // Store session info for future requests
      setSessionId(data.session_id);
      setUserId(data.user_id)
      // Parse gifts from the response
      const json = JSON.parse(data.response);
      console.log(json);
      const gifts = parseGiftsFromResponse(JSON.parse(data.response));
      console.log(`FOUND ${gifts.length} gifts`)
      if(gifts.length == 0){
        return {
          text: "OH NO! Something went wrong with the North Pole's computer system! 😱 Can you try asking me again? I promise I'll do better!",
          gifts: [],
        };
      }
      
      return {
        text: getBuddyResponse(query, gifts),
        gifts: gifts,
      };
    } catch (error) {
      console.error('Error calling API:', error);
      return {
        text: "OH NO! Something went wrong with the North Pole's computer system! 😱 Can you try asking me again? I promise I'll do better!",
        gifts: [],
      };
    }
  };

  const getBuddyResponse = (userMessage: string, products: Gift[]): string => {
    const responses = [
      `OH BOY! I found ${products.length} AMAZING deals for "${userMessage}"! These are the BEST prices I could find, Santa! The elves would be SO proud! 🎁`,
      `SANTA! SANTA! I searched through ALL the North Pole's favorite stores and found ${products.length} PERFECT options for "${userMessage}"! Look at these SPECTACULAR deals! ⭐`,
      `WOW! This is so exciting! I checked EVERYWHERE and found ${products.length} incredible deals on "${userMessage}"! I sorted them by price because I know you have to budget for MILLIONS of presents! 🎄`,
      `BUDDY THE ELF, WHAT'S YOUR FAVORITE DEAL? ALL OF THESE! I found ${products.length} options for "${userMessage}" and they're all SPECTACULAR! The cheapest one is at the top! 🌟`,
      `This is the BEST DAY EVER! I found ${products.length} amazing deals for "${userMessage}"! I'm so good at helping Santa! Does someone need a hug? 🤗`,
    ];
    
    return responses[Math.floor(Math.random() * responses.length)];
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      type: 'user',
      text: input,
    };

    setMessages(prev => [...prev, userMessage]);
    const queryText = input;
    setInput('');
    setIsLoading(true);

    try {
      const result = await searchGifts(queryText);
      const buddyMessage: Message = {
        id: (Date.now() + 1).toString(),
        type: 'buddy',
        text: result.text,
        products: result.gifts.length > 0 ? result.gifts : undefined,
      };

      setMessages(prev => [...prev, buddyMessage]);
    } catch (error) {
      console.error('Error processing query:', error);
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        type: 'buddy',
        text: "OH NO! Something went wrong! 😱 The elves are working on fixing it!",
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-2xl overflow-hidden border-4 border-yellow-400">
      <div className="h-[600px] overflow-y-auto p-6 space-y-4 bg-gradient-to-b from-red-50 to-green-50">
        {messages.map(message => (
          <div key={message.id}>
            <ChatMessage message={message} />
            {message.products && message.products.length > 0 && (
              <div className="mt-4 space-y-3">
                {message.products.map(product => (
                  <GiftCard key={product.id} product={product} />
                ))}
              </div>
            )}
          </div>
        ))}
        {isLoading && (
          <div className="flex items-start gap-3">
            <div className="w-10 h-10 rounded-full bg-green-600 flex items-center justify-center overflow-hidden flex-shrink-0 border-2 border-green-700">
              <img src="/elf_avatar.png" alt="Buddy" className="w-full h-full object-cover" /> 
            </div>
            <div className="bg-white rounded-2xl rounded-tl-none px-4 py-3 shadow-md border-2 border-green-300">
              <div className="flex gap-1">
                <span className="w-2 h-2 bg-green-600 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></span>
                <span className="w-2 h-2 bg-green-600 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></span>
                <span className="w-2 h-2 bg-green-600 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></span>
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <form onSubmit={handleSubmit} className="border-t-4 border-yellow-400 bg-green-800 p-4">
        <div className="flex gap-2">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="What gift are you looking for, Santa Claus?"
            className="flex-1 rounded-full px-6 py-3 border-2 border-yellow-400 focus:outline-none focus:ring-2 focus:ring-yellow-500"
            disabled={isLoading}
          />
          <button
            type="submit"
            disabled={isLoading || !input.trim()}
            className="bg-red-600 text-white rounded-full px-6 py-3 hover:bg-red-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors shadow-lg flex items-center gap-2"
          >
            <Send className="w-5 h-5" />
            <span>Send</span>
          </button>
        </div>
      </form>
    </div>
  );
}