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
    public Conversation create(ConversationCreateRequest request, 
                              MultipartFile articleAudioFile,
                              MultipartFile conversationAudioFile) {
        Conversation conversation = new Conversation();
        conversation.setMainTopic(request.getMainTopic());
        conversation.setSubTopic(request.getSubTopic().trim());
        conversation.setArticle(request.getArticle().trim());
        conversation.setPositiveConversation(request.getPositiveConversation());
        conversation.setNegativeConversation(request.getNegativeConversation());
        
        if (articleAudioFile != null && !articleAudioFile.isEmpty()) {
            String filename = fileStorageService.storeFile(articleAudioFile);
            conversation.setArticleAudio(filename);
        }
        
        if (conversationAudioFile != null && !conversationAudioFile.isEmpty()) {
            String filename = fileStorageService.storeFile(conversationAudioFile);
            conversation.setConversationAudio(filename);
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
    public Conversation update(Long id, ConversationUpdateRequest request, 
                              MultipartFile articleAudioFile,
                              MultipartFile conversationAudioFile) {
        Conversation conversation = get(id);

        if (request.getMainTopic() != null) {
            conversation.setMainTopic(request.getMainTopic());
        }
        if (request.getSubTopic() != null && !request.getSubTopic().isBlank()) {
            conversation.setSubTopic(request.getSubTopic().trim());
        }
        if (request.getArticle() != null && !request.getArticle().isBlank()) {
            conversation.setArticle(request.getArticle().trim());
        }
        if (request.getPositiveConversation() != null) {
            conversation.setPositiveConversation(request.getPositiveConversation().trim());
        }
        if (request.getNegativeConversation() != null) {
            conversation.setNegativeConversation(request.getNegativeConversation().trim());
        }
        
        if (articleAudioFile != null && !articleAudioFile.isEmpty()) {
            // Delete old audio file if exists
            if (conversation.getArticleAudio() != null) {
                fileStorageService.deleteFile(conversation.getArticleAudio());
            }
            String filename = fileStorageService.storeFile(articleAudioFile);
            conversation.setArticleAudio(filename);
        }
        
        if (conversationAudioFile != null && !conversationAudioFile.isEmpty()) {
            // Delete old audio file if exists
            if (conversation.getConversationAudio() != null) {
                fileStorageService.deleteFile(conversation.getConversationAudio());
            }
            String filename = fileStorageService.storeFile(conversationAudioFile);
            conversation.setConversationAudio(filename);
        }

        return conversationRepository.save(conversation);
    }

    @Transactional
    public void delete(Long id) {
        Conversation conversation = get(id);
        
        // Delete audio files if they exist
        if (conversation.getArticleAudio() != null) {
            fileStorageService.deleteFile(conversation.getArticleAudio());
        }
        if (conversation.getConversationAudio() != null) {
            fileStorageService.deleteFile(conversation.getConversationAudio());
        }
        
        conversationRepository.deleteById(id);
    }
}
