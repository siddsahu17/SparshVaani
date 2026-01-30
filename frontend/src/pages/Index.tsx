import { useState } from "react";
import Hero from "@/components/Hero";
import InputModes from "@/components/InputModes";
import OutputDisplay from "@/components/OutputDisplay";
import AccessibilityControls from "@/components/AccessibilityControls";
import LanguageSwitcher from "@/components/LanguageSwitcher";
import Footer from "@/components/Footer";
import { LanguageProvider } from "@/contexts/LanguageContext";

const Index = () => {
  const [activeMode, setActiveMode] = useState<'voice' | 'upload' | 'youtube' | null>(null);
  const [result, setResult] = useState<{ text: string; braille: string } | null>(null);

  const handleModeSelect = (mode: 'voice' | 'upload' | 'youtube') => {
    setActiveMode(mode);
    setResult(null); // Clear previous results
    // Smooth scroll to input section
    setTimeout(() => {
      window.scrollTo({ top: window.innerHeight * 0.6, behavior: 'smooth' });
    }, 100);
  };

  const handleProcess = (processedResult: { text: string; braille: string }) => {
    setResult(processedResult);
    // Smooth scroll to results
    setTimeout(() => {
      window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' });
    }, 100);
  };

  return (
    <LanguageProvider>
      <div className="min-h-screen flex flex-col">
        <div className="fixed top-4 right-20 z-50">
          <LanguageSwitcher />
        </div>
        <AccessibilityControls />
        
        <main className="flex-grow">
          <Hero onModeSelect={handleModeSelect} />
          <InputModes activeMode={activeMode} onProcess={handleProcess} />
          <OutputDisplay result={result} />
        </main>

        <Footer />
      </div>
    </LanguageProvider>
  );
};

export default Index;
