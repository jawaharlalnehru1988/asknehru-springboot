package com.asknehru.asknehrubackend.conversations;

import jakarta.validation.constraints.Size;

public class ConversationUpdateRequest {
    @Size(max = 100)
    private String mainTopic;

    @Size(max = 200)
    private String subTopic;

    private String article;

    private String positiveConversation;
    
    private String negativeConversation;

    public String getMainTopic() {
        return mainTopic;
    }

    public void setMainTopic(String mainTopic) {
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
