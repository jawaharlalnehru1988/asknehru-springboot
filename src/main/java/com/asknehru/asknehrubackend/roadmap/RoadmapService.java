package com.asknehru.asknehrubackend.roadmap;

import com.asknehru.asknehrubackend.conversations.FileStorageService;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.web.multipart.MultipartFile;

import java.util.List;
import java.util.stream.Collectors;

@Service
@RequiredArgsConstructor
public class RoadmapService {
    private final RoadmapRepository roadmapRepository;
    private final FileStorageService fileStorageService;

    public List<String> getAllMainTopics() {
        return roadmapRepository.findAllMainTopics();
    }

    public List<RoadmapResponse> getAllRoadmaps() {
        return roadmapRepository.findAllByOrderByCreatedAtDesc().stream()
                .map(this::toResponse)
                .collect(Collectors.toList());
    }

    public RoadmapResponse getRoadmapById(Long id) {
        Roadmap roadmap = roadmapRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Roadmap not found with id: " + id));
        return toResponse(roadmap);
    }

    @Transactional
    public RoadmapResponse createRoadmap(RoadmapCreateRequest request, MultipartFile imageFile) {
        Roadmap roadmap = new Roadmap();
        roadmap.setMainTopic(request.getMainTopic());
        roadmap.setSyllabus(request.getSyllabus());
        roadmap.setRouterLink(request.getRouterLink());
        roadmap.setIntro(request.getIntro());

        // Handle image file upload
        if (imageFile != null && !imageFile.isEmpty()) {
            String filename = fileStorageService.storeFile(imageFile);
            roadmap.setImageUrl(filename);
        }

        Roadmap saved = roadmapRepository.save(roadmap);
        return toResponse(saved);
    }

    @Transactional
    public RoadmapResponse updateRoadmap(Long id, RoadmapUpdateRequest request, MultipartFile imageFile) {
        Roadmap roadmap = roadmapRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Roadmap not found with id: " + id));

        if (request.getMainTopic() != null) {
            roadmap.setMainTopic(request.getMainTopic());
        }
        if (request.getSyllabus() != null) {
            roadmap.setSyllabus(request.getSyllabus());
        }
        if (request.getRouterLink() != null) {
            roadmap.setRouterLink(request.getRouterLink());
        }
        if (request.getIntro() != null) {
            roadmap.setIntro(request.getIntro());
        }

        // Handle image file upload
        if (imageFile != null && !imageFile.isEmpty()) {
            // Delete old image if exists
            if (roadmap.getImageUrl() != null) {
                fileStorageService.deleteFile(roadmap.getImageUrl());
            }
            String filename = fileStorageService.storeFile(imageFile);
            roadmap.setImageUrl(filename);
        }

        Roadmap updated = roadmapRepository.save(roadmap);
        return toResponse(updated);
    }

    @Transactional
    public void deleteRoadmap(Long id) {
        Roadmap roadmap = roadmapRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Roadmap not found with id: " + id));
        
        // Delete image file if exists
        if (roadmap.getImageUrl() != null) {
            fileStorageService.deleteFile(roadmap.getImageUrl());
        }
        
        roadmapRepository.deleteById(id);
    }

    private RoadmapResponse toResponse(Roadmap roadmap) {
        String imageUrl = roadmap.getImageUrl() != null 
            ? "/api/roadmaps/images/" + roadmap.getImageUrl()
            : null;
            
        return new RoadmapResponse(
                roadmap.getId(),
                roadmap.getMainTopic(),
                roadmap.getSyllabus(),
                imageUrl,
                roadmap.getRouterLink(),
                roadmap.getIntro(),
                roadmap.getCreatedAt(),
                roadmap.getUpdatedAt()
        );
    }
}
