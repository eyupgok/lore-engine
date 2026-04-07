package com.qyzenth.ai_gateaway.repository;

import com.qyzenth.ai_gateaway.entity.ChatHistory;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface ChatHistoryRepository extends JpaRepository<ChatHistory, Long> {

    // Spring Boot'un en büyük sihri burası!
    // Metodun adını İngilizce kurallara göre yazıyoruz, arka plandaki tüm karmaşık
    // SQL kodunu (SELECT * FROM chat_history ORDER BY id DESC LIMIT 5) Spring kendisi yazıyor.
    List<ChatHistory> findTop5ByOrderByIdDesc();

}