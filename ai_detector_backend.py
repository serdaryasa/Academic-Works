# Yapay Zeka ve Doğal Dil İşleme Dersi Kapsamlı Projesi
import math
import re
from typing import Dict, Any

class TextMetricsCalculator:
    """Metnin yapısal ve dilbilimsel özelliklerini analiz eden sınıf."""
    
    @staticmethod
    def calculate_burstiness(text: str) -> float:
        """Cümle uzunluklarının varyansını hesaplayarak insansı yazım ritmini (Burstiness) ölçer."""
        sentences = re.split(r'[.!?]+', text)
        lengths = [len(s.split()) for s in sentences if len(s.split()) > 0]
        
        if len(lengths) < 2:
            return 0.0
            
        mean = sum(lengths) / len(lengths)
        variance = sum((x - mean) ** 2 for x in lengths) / len(lengths)
        return math.sqrt(variance)

    @staticmethod
    def calculate_perplexity(text: str) -> float:
        """Kelime çeşitliliği ve tekrarlarına bakarak metnin tahmin edilebilirliğini (Perplexity) simüle eder."""
        words = re.findall(r'\b\w+\b', text.lower())
        if not words:
            return 0.0
            
        word_counts = {}
        for word in words:
            word_counts[word] = word_counts.get(word, 0) + 1
            
        entropy = 0.0
        total_words = len(words)
        for count in word_counts.values():
            p = count / total_words
            entropy -= p * math.log2(p)
            
        return entropy * 10 

class DetectorModelFactory:
    """Farklı analiz modellerini dinamik olarak üreten Factory Design Pattern yapısı."""
    
    def get_detector(self, model_type: str):
        if model_type.upper() == "STATISTICAL":
            return StatisticalAIDetector()
        elif model_type.upper() == "HYBRID":
            return HybridAIDetector()
        else:
            raise ValueError(f"Bilinmeyen model tipi: {model_type}")

class AIDetectorBase:
    def analyze(self, text: str) -> Dict[str, Any]:
        raise NotImplementedError("Bu metot alt sınıflar tarafından ezilmelidir.")

class StatisticalAIDetector(AIDetectorBase):
    """İstatistiksel analiz yöntemleriyle AI tespiti yapan model."""
    
    def analyze(self, text: str) -> Dict[str, Any]:
        perplexity = TextMetricsCalculator.calculate_perplexity(text)
        burstiness = TextMetricsCalculator.calculate_burstiness(text)

        ai_probability = 100.0
        if perplexity > 30 and burstiness > 5:
            ai_probability -= (perplexity * 1.2) + (burstiness * 2.0)
            
        ai_probability = max(0.0, min(99.9, ai_probability))
        
        return {
            "model_used": "Statistical-NLP-v1",
            "ai_probability": round(ai_probability, 2),
            "metrics": {
                "perplexity_score": round(perplexity, 4),
                "burstiness_score": round(burstiness, 4)
            },
            "verdict": "AI Generated" if ai_probability > 50 else "Human Written"
        }

class HybridAIDetector(AIDetectorBase):
    """Hem istatistiksel hem de anlamsal heuristikleri birleştiren gelişmiş model."""
    
    def analyze(self, text: str) -> Dict[str, Any]:
        base_detector = StatisticalAIDetector()
        result = base_detector.analyze(text)
        
        ai_markers = ["furthermore", "in conclusion", "it is important to note", "testament to"]
        marker_count = sum(1 for marker in ai_markers if marker in text.lower())
        
        adjusted_prob = result["ai_probability"] + (marker_count * 5.0)
        adjusted_prob = max(0.0, min(99.9, adjusted_prob))
        
        result["ai_probability"] = round(adjusted_prob, 2)
        result["model_used"] = "Hybrid-Heuristic-v2"
        result["verdict"] = "AI Generated" if adjusted_prob > 50 else "Human Written"
        
        return result

if __name__ == "__main__":
    factory = DetectorModelFactory()
    detector = factory.get_detector("hybrid")
    
    human_text = "Dün gece arabayı çalıştırırken marş basmadı, sinir oldum. Bütün elektronik ışıklar yanıyor ama motor bir türlü ateşlemiyordu. Sanırım sanayinin yolu gözüktü."
    ai_text = "Furthermore, it is important to note that the internal combustion engine requires a precise mixture of fuel and air. In conclusion, a faulty starter motor can result in immediate ignition failure."
    
    print("="*60)
    print("🤖 Gelişmiş Yapay Zeka İçerik Tespit Motoru Analiz Testi")
    print("="*60)
    
    for i, test_text in enumerate([human_text, ai_text], 1):
        print(f"\n[Test #{i}] Analiz Edilen Metin: '{test_text[:60]}...'")
        analysis_result = detector.analyze(test_text)
        print(f"-> Kullanılan Model : {analysis_result['model_used']}")
        print(f"-> Yapay Zeka Olasılığı: %{analysis_result['ai_probability']}")
        print(f"-> Metrik Raporu    : {analysis_result['metrics']}")
        print(f"-> Nihai Karar      :  {analysis_result['verdict']}")
        print("-" * 60)
