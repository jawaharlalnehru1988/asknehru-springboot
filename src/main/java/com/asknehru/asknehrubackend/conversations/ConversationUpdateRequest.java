package com.asknehru.asknehrubackend.conversations;

import jakarta.validation.constraints.Size;

public class ConversationUpdateRequest {
    @Size(max = 120)
    private String topicCategory;

    private String question;

    private String answer;

    private String criticalConversation;

    public String getTopicCategory() {
        return topicCategory;
    }

    public void setTopicCategory(String topicCategory) {
        this.topicCategory = topicCategory;
    }

    public String getQuestion() {
        return question;
    }

    public void setQuestion(String question) {
        this.question = question;
    }

    public String getAnswer() {
        return answer;
    }

    public void setAnswer(String answer) {
        this.answer = answer;
    }

    public String getCriticalConversation() {
        return criticalConversation;
    }

    public void setCriticalConversation(String criticalConversation) {
        this.criticalConversation = criticalConversation;
    }
}
