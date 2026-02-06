package com.asknehru.asknehrubackend.conversations;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.EnumType;
import jakarta.persistence.Enumerated;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.PrePersist;
import jakarta.persistence.PreUpdate;
import jakarta.persistence.Table;
import java.time.Instant;

@Entity
@Table(name = "knowledge_base")
public class Conversation {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false, length = 50)
    private MainTopic mainTopic;

    @Column(nullable = false, length = 200)
    private String subTopic;

    @Column(nullable = false, columnDefinition = "text")
    private String article;

    @Column(columnDefinition = "text")
    private String positiveConversation;

    @Column(columnDefinition = "text")
    private String negativeConversation;

    @Column(length = 500)
    private String articleAudio;

    @Column(length = 500)
    private String conversationAudio;

    @Column(nullable = false, updatable = false)
    private Instant createdAt;

    @Column(nullable = false)
    private Instant updatedAt;

    @PrePersist
    void onCreate() {
        Instant now = Instant.now();
        createdAt = now;
        updatedAt = now;
    }

    @PreUpdate
    void onUpdate() {
        updatedAt = Instant.now();
    }

    public Long getId() {
        return id;
    }

    public MainTopic getMainTopic() {
        return mainTopic;
    }

    public void setMainTopic(MainTopic mainTopic) {
        this.mainTopic = mainTopic;
    }

    public String getSubTopic() {
        return subTopic;
    }

    public void setSubTopic(String subTopic) {
        this.subTopic = subTopic;
    }

    public String getArticle() {
        return article;
    }

    public void setArticle(String article) {
        this.article = article;
    }

    public String getPositiveConversation() {
        return positiveConversation;
    }

    public void setPositiveConversation(String positiveConversation) {
        this.positiveConversation = positiveConversation;
    }

    public String getNegativeConversation() {
        return negativeConversation;
    }

    public void setNegativeConversation(String negativeConversation) {
        this.negativeConversation = negativeConversation;
    }

    public String getArticleAudio() {
        return articleAudio;
    }

    public void setArticleAudio(String articleAudio) {
        this.articleAudio = articleAudio;
    }

    public String getConversationAudio() {
        return conversationAudio;
    }

    public void setConversationAudio(String conversationAudio) {
        this.conversationAudio = conversationAudio;
    }

    public Instant getCreatedAt() {
        return createdAt;
    }

    public Instant getUpdatedAt() {
        return updatedAt;
    }
}
