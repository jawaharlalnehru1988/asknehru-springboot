package com.asknehru.asknehrubackend.roadmap;

import com.asknehru.asknehrubackend.conversations.FileStorageService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.core.io.Resource;
import org.springframework.core.io.UrlResource;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.List;

@RestController
@RequestMapping("/api/roadmaps")
@RequiredArgsConstructor
@CrossOrigin(origins = "*")
public class RoadmapController {
    private final RoadmapService roadmapService;
    private final FileStorageService fileStorageService;

    @GetMapping
    public ResponseEntity<List<RoadmapResponse>> getAllRoadmaps() {
        return ResponseEntity.ok(roadmapService.getAllRoadmaps());
    }

    @GetMapping("/{id}")
    public ResponseEntity<RoadmapResponse> getRoadmapById(@PathVariable Long id) {
        return ResponseEntity.ok(roadmapService.getRoadmapById(id));
    }

    @PostMapping(consumes = MediaType.MULTIPART_FORM_DATA_VALUE)
    public ResponseEntity<RoadmapResponse> createRoadmap(
            @Valid @RequestPart("data") RoadmapCreateRequest request,
            @RequestPart(value = "image", required = false) MultipartFile imageFile) {
        RoadmapResponse response = roadmapService.createRoadmap(request, imageFile);
        return ResponseEntity.status(HttpStatus.CREATED).body(response);
    }

    @PutMapping(value = "/{id}", consumes = MediaType.MULTIPART_FORM_DATA_VALUE)
    public ResponseEntity<RoadmapResponse> updateRoadmap(
            @PathVariable Long id,
            @Valid @RequestPart("data") RoadmapUpdateRequest request,
            @RequestPart(value = "image", required = false) MultipartFile imageFile) {
        RoadmapResponse response = roadmapService.updateRoadmap(id, request, imageFile);
        return ResponseEntity.ok(response);
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deleteRoadmap(@PathVariable Long id) {
        roadmapService.deleteRoadmap(id);
        return ResponseEntity.noContent().build();
    }

    @GetMapping("/images/{filename}")
    public ResponseEntity<Resource> getImage(@PathVariable String filename) {
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
}
