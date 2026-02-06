package com.asknehru.asknehrubackend.conversations;

import org.springframework.http.HttpStatus;
import org.springframework.web.server.ResponseStatusException;

public class ConversationNotFoundException extends ResponseStatusException {
    public ConversationNotFoundException(String reason) {
        super(HttpStatus.NOT_FOUND, reason);
    }
}
