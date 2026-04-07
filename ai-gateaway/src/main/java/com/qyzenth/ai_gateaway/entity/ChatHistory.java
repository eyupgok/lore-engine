package com.qyzenth.ai_gateaway.entity;

import jakarta.persistence.*;

@Entity // Spring'e "Bu sınıfı al, PostgreSQL'de bir tabloya çevir" diyen sihirli şapka.
public class ChatHistory {

    @Id // Bu verinin kimlik numarası (Primary Key) olduğunu belirtir.
    @GeneratedValue(strategy = GenerationType.IDENTITY) // Kimlik numarasını 1, 2, 3 diye otomatik artırır.
    private Long id;

    @Column(columnDefinition = "TEXT") // Uzun paragraflar sığabilsin diye TEXT tipinde açıyoruz.
    private String prompt;

    @Column(columnDefinition = "TEXT")
    private String answer;

    // JPA'nın arka planda çalışabilmesi için zorunlu olan boş yapıcı metot
    public ChatHistory() {
    }

    // Kendi kullanacağımız yapıcı metot
    public ChatHistory(String prompt, String answer) {
        this.prompt = prompt;
        this.answer = answer;
    }

    // Verileri okuyabilmek için Get metotları
    public Long getId() {
        return id;
    }

    public String getPrompt() {
        return prompt;
    }

    public String getAnswer() {
        return answer;
    }
}