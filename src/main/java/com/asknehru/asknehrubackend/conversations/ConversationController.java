package com.asknehru.asknehrubackend.conversations;

import jakarta.validation.Valid;
import java.util.List;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/conversations")
public class ConversationController {
    private final ConversationService conversationService;

    public ConversationController(ConversationService conversationService) {
        this.conversationService = conversationService;
    }

    @PostMapping
    public ResponseEntity<ConversationResponse> create(@Valid @RequestBody ConversationCreateRequest request) {
        Conversation conversation = conversationService.create(request);
        return ResponseEntity.status(HttpStatus.CREATED).body(toResponse(conversation));
    }

    @GetMapping
    public List<ConversationResponse> list() {
        return conversationService.list().stream().map(this::toResponse).toList();
    }

    @GetMapping("/{id}")
    public ConversationResponse get(@PathVariable Long id) {
        return toResponse(conversationService.get(id));
    }

    @PutMapping("/{id}")
    public ConversationResponse update(@PathVariable Long id,
                                       @Valid @RequestBody ConversationUpdateRequest request) {
        return toResponse(conversationService.update(id, request));
    }

    @DeleteMapping("/{id}")
    @org.springframework.web.bind.annotation.ResponseStatus(HttpStatus.NO_CONTENT)
    public void delete(@PathVariable Long id) {
        conversationService.delete(id);
    }

    private ConversationResponse toResponse(Conversation conversation) {
        return new ConversationResponse(
            conversation.getId(),
            conversation.getTopicCategory(),
            conversation.getQuestion(),
            conversation.getAnswer(),
            conversation.getCriticalConversation(),
            conversation.getCreatedAt(),
            conversation.getUpdatedAt()
        );
    }
}
