package com.qyzenth.ai_gateaway.service;

import com.qyzenth.ai_gateaway.dto.AIRequest;
import com.qyzenth.ai_gateaway.dto.AIResponse;
import com.qyzenth.ai_gateaway.entity.ChatHistory;
import com.qyzenth.ai_gateaway.repository.ChatHistoryRepository;
import org.springframework.stereotype.Service;
import org.springframework.web.reactive.function.client.WebClient;

import java.util.Collections;
import java.util.List;

@Service
public class AIGatewayService {

    private final WebClient webClient;
    private final ChatHistoryRepository chatHistoryRepository; // 1. Kütüphaneciyi işe aldık

    // Constructor Injection (Spring Boot kütüphaneciyi ve motoru otomatik getirir)
    public AIGatewayService(WebClient customWebClient, ChatHistoryRepository chatHistoryRepository) {
        this.webClient = customWebClient;
        this.chatHistoryRepository = chatHistoryRepository;
    }

    public AIResponse askPythonAI(AIRequest request) {

        // --- 1. AŞAMA: HAFIZAYI ÇAĞIRMA ---
        // Kütüphaneciden son 5 sohbeti istiyoruz. (Metot "Desc" olduğu için en yeniden eskiye doğru gelir)
        List<ChatHistory> pastChats = chatHistoryRepository.findTop5ByOrderByIdDesc();

        // Doğru bir sohbet akışı (eskiden yeniye) için listeyi ters çeviriyoruz
        Collections.reverse(pastChats);

        // --- 2. AŞAMA: PROMPT MÜHENDİSLİĞİ (Geçmişi Yeni Soruya Ekleme) ---
        String finalPrompt = request.prompt(); // Eğer geçmiş yoksa, sadece ham soruyu yollayacağız.

        if (!pastChats.isEmpty()) {
            StringBuilder memoryBuilder = new StringBuilder("İşte seninle yapılan önceki sohbetlerin geçmişi:\n");

            for (ChatHistory chat : pastChats) {
                memoryBuilder.append("Kullanıcı: ").append(chat.getPrompt()).append("\n");
                memoryBuilder.append("Sen: ").append(chat.getAnswer()).append("\n\n");
            }

            memoryBuilder.append("Şimdi, yukarıdaki geçmişi de göz önünde bulundurarak şu YENİ SORUYU cevapla: ")
                    .append(request.prompt());

            finalPrompt = memoryBuilder.toString();
        }

        // Java'da "record" yapıları değiştirilemez (immutable) olduğu için,
        // hafızayla şişirilmiş yepyeni bir AIRequest kutusu oluşturuyoruz.
        AIRequest enrichedRequest = new AIRequest(finalPrompt, request.maxTokens(), request.temperature());

        // --- 3. AŞAMA: PYTHON'A GÖNDERME ---
        AIResponse response = webClient.post()
                .uri("/api/ask")
                .bodyValue(enrichedRequest)
                .retrieve()
                .bodyToMono(AIResponse.class)
                .block();

        // --- 4. AŞAMA: KASAYA KAYDETME ---
        // Python'dan cevap başarıyla geldikten sonra, kullanıcının o ilk baştaki ham sorusunu
        // ve Python'un cevabını veritabanına kaydediyoruz.
        ChatHistory newRecord = new ChatHistory(request.prompt(), response.answer());
        chatHistoryRepository.save(newRecord); // Kütüphaneci bunu hemen PostgreSQL'e yazar

        return response;
    }
}