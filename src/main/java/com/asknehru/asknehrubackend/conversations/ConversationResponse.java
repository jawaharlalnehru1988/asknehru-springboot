package com.asknehru.asknehrubackend.conversations;

import java.time.Instant;

public class ConversationResponse {
    private Long id;
    private MainTopic mainTopic;
    private String subTopic;
    private String article;
    private String positiveConversation;
    private String negativeConversation;
    private String articleAudio;
    private String conversationAudio;
    private Instant createdAt;
    private Instant updatedAt;

    public ConversationResponse(Long id,
                                MainTopic mainTopic,
                                String subTopic,
                                String article,
                                String positiveConversation,
                                String negativeConversation,
                                String articleAudio,
                                String conversationAudio,
                                Instant createdAt,
                                Instant updatedAt) {
        this.id = id;
        this.mainTopic = mainTopic;
        this.subTopic = subTopic;
        this.article = article;
        this.positiveConversation = positiveConversation;
        this.negativeConversation = negativeConversation;
        this.articleAudio = articleAudio;
        this.conversationAudio = conversationAudio;
        this.createdAt = createdAt;
        this.updatedAt = updatedAt;
    }

    public Long getId() {
        return id;
    }

    public MainTopic getMainTopic() {
        return mainTopic;
    }

    public String getSubTopic() {
        return subTopic;
    }

    public String getArticle() {
        return article;
    }

    public String getPositiveConversation() {
        return positiveConversation;
    }

    public String getNegativeConversation() {
        return negativeConversation;
    }

    public String getArticleAudio() {
        return articleAudio;
    }

    public String getConversationAudio() {
        return conversationAudio;
    }

    public Instant getCreatedAt() {
        return createdAt;
    }

    public Instant getUpdatedAt() {
        return updatedAt;
    }
}
