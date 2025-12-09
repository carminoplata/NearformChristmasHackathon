import type { ChatMessageProps } from '../types';

export function ChatMessage({ message }: ChatMessageProps) {
  if (message.type === 'buddy') {
    return (
      <div className="flex items-start gap-3">
        <div className="w-10 h-10 rounded-full bg-green-600 flex items-center justify-center overflow-hidden flex-shrink-0 border-2 border-green-700">
          <img src="/elf_avatar.png" alt="Buddy" className="w-full h-full object-cover" />
        </div>
        <div className="bg-white rounded-2xl rounded-tl-none px-4 py-3 max-w-[80%] shadow-md border-2 border-green-300">
          <p className="text-gray-800">{message.text}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="flex items-start gap-3 justify-end">
      <div className="bg-red-600 text-white rounded-2xl rounded-tr-none px-4 py-3 max-w-[80%] shadow-md">
        <p>{message.text}</p>
      </div>
      <div className="w-10 h-10 rounded-full bg-red-600 flex items-center justify-center text-xl flex-shrink-0">
        🎅
      </div>
    </div>
  );
}