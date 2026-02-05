package com.asknehru.asknehrubackend.users;

import org.springframework.http.HttpStatus;
import org.springframework.web.server.ResponseStatusException;

public class UserConflictException extends ResponseStatusException {
    public UserConflictException(String reason) {
        super(HttpStatus.CONFLICT, reason);
    }
}
