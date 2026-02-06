package com.asknehru.asknehrubackend.conversations;

import java.time.Instant;

public class ConversationResponse {
    private Long id;
    private String topicCategory;
    private String question;
    private String answer;
    private String criticalConversation;
    private Instant createdAt;
    private Instant updatedAt;

    public ConversationResponse(Long id,
                                String topicCategory,
                                String question,
                                String answer,
                                String criticalConversation,
                                Instant createdAt,
                                Instant updatedAt) {
        this.id = id;
        this.topicCategory = topicCategory;
        this.question = question;
        this.answer = answer;
        this.criticalConversation = criticalConversation;
        this.createdAt = createdAt;
        this.updatedAt = updatedAt;
    }

    public Long getId() {
        return id;
    }

    public String getTopicCategory() {
        return topicCategory;
    }

    public String getQuestion() {
        return question;
    }

    public String getAnswer() {
        return answer;
    }

    public String getCriticalConversation() {
        return criticalConversation;
    }

    public Instant getCreatedAt() {
        return createdAt;
    }

    public Instant getUpdatedAt() {
        return updatedAt;
    }
}
