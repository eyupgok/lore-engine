package com.qyzenth.ai_gateaway.controller;

import com.qyzenth.ai_gateaway.dto.AIRequest;
import com.qyzenth.ai_gateaway.dto.AIResponse;
import com.qyzenth.ai_gateaway.service.AIGatewayService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/v1/ai")
public class AIGatewayController {

    private final AIGatewayService aiService;

    // Garsonu işe alıyoruz (Dependency Injection)
    public AIGatewayController(AIGatewayService aiService) {
        this.aiService = aiService;
    }

    @PostMapping("/ask")
    public ResponseEntity<AIResponse> askQuestion(@RequestBody AIRequest request) {

        // 1. Müşteriden gelen siparişi (request) al ve mutfak kuryesine (aiService) ver.
        AIResponse response = aiService.askPythonAI(request);

        // 2. Mutfaktan gelen tabağı (response) al, "200 OK (Başarılı)" etiketiyle müşteriye sun.
        return ResponseEntity.ok(response);
    }
}