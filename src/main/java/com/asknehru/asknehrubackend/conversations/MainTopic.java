package com.asknehru.asknehrubackend.conversations;

public enum MainTopic {
    JAVA("Java"),
    ANGULAR("Angular"),
    REACT("React"),
    AGENTIC_AI("Agentic AI"),
    SOFT_SKILL("Soft Skill"),
    NODE("Node"),
    TESTING("Testing"),
    DEVOPS("DevOps");

    private final String displayName;

    MainTopic(String displayName) {
        this.displayName = displayName;
    }

    public String getDisplayName() {
        return displayName;
    }
}
