package com.asknehru.asknehrubackend.conversations;

import jakarta.validation.Valid;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Arrays;
import java.util.List;
import java.util.stream.Collectors;
import org.springframework.core.io.Resource;
import org.springframework.core.io.UrlResource;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestPart;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.multipart.MultipartFile;

@RestController
@RequestMapping("/api/conversations")
public class ConversationController {
    private final ConversationService conversationService;
    private final FileStorageService fileStorageService;

    public ConversationController(ConversationService conversationService,
                                 FileStorageService fileStorageService) {
        this.conversationService = conversationService;
        this.fileStorageService = fileStorageService;
    }

    @GetMapping("/main-topics")
    public List<MainTopicResponse> getMainTopics() {
        return Arrays.stream(MainTopic.values())
            .map(topic -> new MainTopicResponse(topic.name(), topic.getDisplayName()))
            .collect(Collectors.toList());
    }

    @PostMapping(consumes = MediaType.MULTIPART_FORM_DATA_VALUE)
    public ResponseEntity<ConversationResponse> create(
            @Valid @RequestPart("data") ConversationCreateRequest request,
            @RequestPart(value = "articleAudio", required = false) MultipartFile articleAudioFile,
            @RequestPart(value = "conversationAudio", required = false) MultipartFile conversationAudioFile) {
        Conversation conversation = conversationService.create(request, articleAudioFile, conversationAudioFile);
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

    @PutMapping(value = "/{id}", consumes = MediaType.MULTIPART_FORM_DATA_VALUE)
    public ConversationResponse update(
            @PathVariable Long id,
            @Valid @RequestPart("data") ConversationUpdateRequest request,
            @RequestPart(value = "articleAudio", required = false) MultipartFile articleAudioFile,
            @RequestPart(value = "conversationAudio", required = false) MultipartFile conversationAudioFile) {
        return toResponse(conversationService.update(id, request, articleAudioFile, conversationAudioFile));
    }

    @DeleteMapping("/{id}")
    @org.springframework.web.bind.annotation.ResponseStatus(HttpStatus.NO_CONTENT)
    public void delete(@PathVariable Long id) {
        conversationService.delete(id);
    }

    @GetMapping("/audio/{filename}")
    public ResponseEntity<Resource> getAudio(@PathVariable String filename) {
        try {
            Path filePath = fileStorageService.getFilePath(filename);
            Resource resource = new UrlResource(filePath.toUri());

            if (resource.exists() && resource.isReadable()) {
                String contentType = Files.probeContentType(filePath);
                if (contentType == null) {
                    contentType = "application/octet-stream";
                }

                return ResponseEntity.ok()
                    .contentType(MediaType.parseMediaType(contentType))
                    .header(HttpHeaders.CONTENT_DISPOSITION, "inline; filename=\"" + filename + "\"")
                    .body(resource);
            } else {
                return ResponseEntity.notFound().build();
            }
        } catch (IOException e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).build();
        }
    }

    private ConversationResponse toResponse(Conversation conversation) {
        String articleAudioUrl = conversation.getArticleAudio() != null 
            ? "/api/conversations/audio/" + conversation.getArticleAudio()
            : null;
        
        String conversationAudioUrl = conversation.getConversationAudio() != null 
            ? "/api/conversations/audio/" + conversation.getConversationAudio()
            : null;
            
        return new ConversationResponse(
            conversation.getId(),
            conversation.getMainTopic(),
            conversation.getSubTopic(),
            conversation.getArticle(),
            conversation.getPositiveConversation(),
            conversation.getNegativeConversation(),
            articleAudioUrl,
            conversationAudioUrl,
            conversation.getCreatedAt(),
            conversation.getUpdatedAt()
        );
    }
}
