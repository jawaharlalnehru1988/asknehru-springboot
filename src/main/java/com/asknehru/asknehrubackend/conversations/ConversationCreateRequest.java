package com.asknehru.asknehrubackend.conversations;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Size;

public class ConversationCreateRequest {
    @NotNull
    private MainTopic mainTopic;

    @NotBlank
    @Size(max = 200)
    private String subTopic;

    @NotBlank
    private String article;

    private String positiveConversation;
    
    private String negativeConversation;

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
}
