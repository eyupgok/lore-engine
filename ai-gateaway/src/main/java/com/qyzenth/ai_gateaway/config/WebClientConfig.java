package com.qyzenth.ai_gateaway.config;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.reactive.function.client.WebClient;

@Configuration
public class WebClientConfig {

    @Bean
    public WebClient customWebClient() {
        // Python FastAPI sunucumuzun ana adresini (Base URL) buraya sabitliyoruz.
        return WebClient.builder()
                .baseUrl("http://127.0.0.1:8000")
                .build();
    }
}