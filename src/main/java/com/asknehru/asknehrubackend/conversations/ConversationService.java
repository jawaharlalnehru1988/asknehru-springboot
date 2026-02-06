package com.asknehru.asknehrubackend.conversations;

import java.util.List;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
public class ConversationService {
    private final ConversationRepository conversationRepository;

    public ConversationService(ConversationRepository conversationRepository) {
        this.conversationRepository = conversationRepository;
    }

    @Transactional
    public Conversation create(ConversationCreateRequest request) {
        Conversation conversation = new Conversation();
        conversation.setTopicCategory(request.getTopicCategory().trim());
        conversation.setQuestion(request.getQuestion().trim());
        conversation.setAnswer(request.getAnswer().trim());
        conversation.setCriticalConversation(request.getCriticalConversation());
        return conversationRepository.save(conversation);
    }

    @Transactional(readOnly = true)
    public List<Conversation> list() {
        return conversationRepository.findAll();
    }

    @Transactional(readOnly = true)
    public Conversation get(Long id) {
        return conversationRepository.findById(id)
            .orElseThrow(() -> new ConversationNotFoundException("Conversation not found."));
    }

    @Transactional
    public Conversation update(Long id, ConversationUpdateRequest request) {
        Conversation conversation = get(id);

        if (request.getTopicCategory() != null && !request.getTopicCategory().isBlank()) {
            conversation.setTopicCategory(request.getTopicCategory().trim());
        }
        if (request.getQuestion() != null && !request.getQuestion().isBlank()) {
            conversation.setQuestion(request.getQuestion().trim());
        }
        if (request.getAnswer() != null && !request.getAnswer().isBlank()) {
            conversation.setAnswer(request.getAnswer().trim());
        }
        if (request.getCriticalConversation() != null) {
            conversation.setCriticalConversation(request.getCriticalConversation().trim());
        }

        return conversationRepository.save(conversation);
    }

    @Transactional
    public void delete(Long id) {
        if (!conversationRepository.existsById(id)) {
            throw new ConversationNotFoundException("Conversation not found.");
        }
        conversationRepository.deleteById(id);
    }
}
