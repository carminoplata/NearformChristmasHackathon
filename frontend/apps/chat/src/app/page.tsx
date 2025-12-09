import { ChatInterface } from '../components/chat_interface';
import { Snowflakes } from '../components/snowflakes';
export default function Index() {
  /*
   * Replace the elements below with your own.
   *
   * Note: The corresponding styles are in the ./index.tailwind file.
   */
  return (
    <div className="min-h-screen bg-gradient-to-b from-red-700 via-green-700 to-red-800 relative overflow-hidden">
      <Snowflakes /> 
      <div className="relative z-10">
        <header className="bg-green-800 border-b-4 border-yellow-400 shadow-lg">
          <div className="max-w-4xl mx-auto px-4 py-6">
            <div className="flex items-center justify-center gap-6">
              <img src="/elf_icon.png" alt="Buddy the Elf" className="w-24 h-24 rounded-full border-4 border-yellow-400" />
              <div>
                <h1 className="text-center text-white">
                  🎄 Buddy The Christmas Assistant 🎄
                </h1>
                <p className="text-center text-yellow-300 mt-2">
                  "The best way to spread Christmas cheer is finding deals for all to hear!"
                </p>
              </div>
            </div>
          </div>
        </header>
        
        <main className="max-w-4xl mx-auto px-4 py-8">
          <ChatInterface />
        </main>
      </div>
    </div>
  );
}
