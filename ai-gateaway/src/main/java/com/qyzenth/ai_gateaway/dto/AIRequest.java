package com.qyzenth.ai_gateaway.dto;

import com.fasterxml.jackson.annotation.JsonProperty;

public record AIRequest(
        String prompt,

        // Python tarafı yılan_isimlendirmesi (snake_case) bekliyor,
        // ama Java'da deve_hörgücü (camelCase) kullanılır.
        // JsonProperty ile dışarı çıkarken adını max_tokens yapıyoruz.
        @JsonProperty("max_tokens") int maxTokens,

        double temperature
) {
}