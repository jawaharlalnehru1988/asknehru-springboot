package com.asknehru.asknehrubackend.conversations;

import java.util.List;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.web.multipart.MultipartFile;

@Service
public class ConversationService {
    private final ConversationRepository conversationRepository;
    private final FileStorageService fileStorageService;

    public ConversationService(ConversationRepository conversationRepository,
                               FileStorageService fileStorageService) {
        this.conversationRepository = conversationRepository;
        this.fileStorageService = fileStorageService;
    }

    @Transactional
    public Conversation create(ConversationCreateRequest request, MultipartFile audioFile) {
        Conversation conversation = new Conversation();
        conversation.setTopicCategory(request.getTopicCategory().trim());
        conversation.setQuestion(request.getQuestion().trim());
        conversation.setAnswer(request.getAnswer().trim());
        conversation.setCriticalConversation(request.getCriticalConversation());
        
        if (audioFile != null && !audioFile.isEmpty()) {
            String filename = fileStorageService.storeFile(audioFile);
            conversation.setAudio(filename);
        }
        
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
    public Conversation update(Long id, ConversationUpdateRequest request, MultipartFile audioFile) {
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
        
        if (audioFile != null && !audioFile.isEmpty()) {
            // Delete old audio file if exists
            if (conversation.getAudio() != null) {
                fileStorageService.deleteFile(conversation.getAudio());
            }
            String filename = fileStorageService.storeFile(audioFile);
            conversation.setAudio(filename);
        }

        return conversationRepository.save(conversation);
    }

    @Transactional
    public void delete(Long id) {
        Conversation conversation = get(id);
        
        // Delete audio file if exists
        if (conversation.getAudio() != null) {
            fileStorageService.deleteFile(conversation.getAudio());
        }
        
        conversationRepository.deleteById(id);
    }
}
