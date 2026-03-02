package com.asknehru.asknehrubackend.yoga;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.io.IOException;
import java.net.URI;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.List;

@Service
public class YogaPoseService {
    
    private final YogaPoseRepository yogaPoseRepository;
    private final Path imageUploadPath;
    private final Path audioUploadPath;
    private final Path videoUploadPath;
    
    public YogaPoseService(
            YogaPoseRepository yogaPoseRepository,
            @Value("${file.upload-dir:/var/www/spring-apps/asknehrubackend/media/yoga-poses}") String imageUploadDir,
            @Value("${file.audio-upload-dir:/var/www/spring-apps/asknehrubackend/media/yoga-audio}") String audioUploadDir,
            @Value("${file.video-upload-dir:/var/www/spring-apps/asknehrubackend/media/yoga-video}") String videoUploadDir
    ) {
        this.yogaPoseRepository = yogaPoseRepository;
        this.imageUploadPath = Paths.get(imageUploadDir).toAbsolutePath().normalize();
        this.audioUploadPath = Paths.get(audioUploadDir).toAbsolutePath().normalize();
        this.videoUploadPath = Paths.get(videoUploadDir).toAbsolutePath().normalize();
    }
    
    public List<YogaPose> getAllPoses() {
        return yogaPoseRepository.findAll();
    }
    
    public YogaPose getPoseById(Long id) {
        return yogaPoseRepository.findById(id)
                .orElseThrow(() -> new YogaPoseNotFoundException("Yoga pose not found with id: " + id));
    }

    public List<YogaPose> searchPosesByYogaName(String yogaName) {
        return yogaPoseRepository.findByYogaNameContainingIgnoreCase(yogaName);
    }
    
    @Transactional
    public YogaPose createPose(YogaPose yogaPose) {
        return yogaPoseRepository.save(yogaPose);
    }
    
    @Transactional
    public YogaPose updatePose(Long id, YogaPose updatedPose) {
        YogaPose existingPose = getPoseById(id);

        deleteReplacedMedia(existingPose.getAudioURL(), updatedPose.getAudioURL(), audioUploadPath, "/media/yoga-audio/", "audio");
        deleteReplacedMedia(existingPose.getImageURL(), updatedPose.getImageURL(), imageUploadPath, "/media/yoga-poses/", "image");
        deleteReplacedMedia(existingPose.getVideoURL(), updatedPose.getVideoURL(), videoUploadPath, "/media/yoga-video/", "video");

        existingPose.setYogaName(updatedPose.getYogaName());
        existingPose.setBlogContent(updatedPose.getBlogContent());
        existingPose.setAudioURL(updatedPose.getAudioURL());
        existingPose.setVideoURL(updatedPose.getVideoURL());
        existingPose.setImageURL(updatedPose.getImageURL());
        existingPose.setCategory(updatedPose.getCategory());
        
        return yogaPoseRepository.save(existingPose);
    }
    
    @Transactional
    public void deletePose(Long id) {
        YogaPose yogaPose = getPoseById(id);
        deleteMediaFileIfPresent(yogaPose.getAudioURL(), audioUploadPath, "/media/yoga-audio/", "audio");
        deleteMediaFileIfPresent(yogaPose.getImageURL(), imageUploadPath, "/media/yoga-poses/", "image");
        deleteMediaFileIfPresent(yogaPose.getVideoURL(), videoUploadPath, "/media/yoga-video/", "video");
        yogaPoseRepository.deleteById(id);
    }

    private void deleteReplacedMedia(
            String existingMediaRef,
            String updatedMediaRef,
            Path uploadDirectory,
            String publicPathPrefix,
            String mediaLabel
    ) {
        if (existingMediaRef == null || existingMediaRef.isBlank()) {
            return;
        }

        String existingTrimmed = existingMediaRef.trim();
        String updatedTrimmed = updatedMediaRef == null ? "" : updatedMediaRef.trim();
        if (existingTrimmed.equals(updatedTrimmed)) {
            return;
        }

        deleteMediaFileIfPresent(existingTrimmed, uploadDirectory, publicPathPrefix, mediaLabel);
    }

    private void deleteMediaFileIfPresent(
            String mediaRef,
            Path uploadDirectory,
            String publicPathPrefix,
            String mediaLabel
    ) {
        if (mediaRef == null || mediaRef.isBlank()) {
            return;
        }

        String pathPart = mediaRef.trim();
        try {
            URI uri = URI.create(pathPart);
            if (uri.getPath() != null && !uri.getPath().isBlank()) {
                pathPart = uri.getPath();
            }
        } catch (IllegalArgumentException ignored) {
        }

        if (!isManagedMediaReference(pathPart, publicPathPrefix)) {
            return;
        }

        Path fileNamePath = Paths.get(pathPart).getFileName();
        if (fileNamePath == null) {
            return;
        }

        Path resolvedPath = uploadDirectory.resolve(fileNamePath.toString()).normalize();
        if (!resolvedPath.startsWith(uploadDirectory)) {
            throw new RuntimeException("Refusing to delete " + mediaLabel + " outside configured upload directory");
        }

        try {
            Files.deleteIfExists(resolvedPath);
        } catch (IOException ex) {
            throw new RuntimeException("Could not delete " + mediaLabel + " file: " + resolvedPath.getFileName(), ex);
        }
    }

    private boolean isManagedMediaReference(String pathPart, String publicPathPrefix) {
        if (pathPart == null || pathPart.isBlank()) {
            return false;
        }

        if (!pathPart.contains("/")) {
            return true;
        }

        String normalizedPath = pathPart.trim();
        String normalizedPrefix = publicPathPrefix.startsWith("/") ? publicPathPrefix : "/" + publicPathPrefix;
        String noSlashPrefix = normalizedPrefix.substring(1);

        return normalizedPath.startsWith(normalizedPrefix) || normalizedPath.startsWith(noSlashPrefix);
    }
}
