package com.asknehru.asknehrubackend.conversations;

public class MainTopicResponse {
    private String value;
    private String label;

    public MainTopicResponse(String value, String label) {
        this.value = value;
        this.label = label;
    }

    public String getValue() {
        return value;
    }

    public String getLabel() {
        return label;
    }
}
