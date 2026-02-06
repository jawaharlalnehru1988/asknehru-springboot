package com.asknehru.asknehrubackend.conversations;

import jakarta.validation.constraints.Size;

public class ConversationUpdateRequest {
    private MainTopic mainTopic;

    @Size(max = 200)
    private String subTopic;

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
