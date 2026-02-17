package com.asknehru.asknehrubackend.yoga;

import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import java.util.List;

@Service
public class YogaPoseService {
    
    private final YogaPoseRepository yogaPoseRepository;
    
    public YogaPoseService(YogaPoseRepository yogaPoseRepository) {
        this.yogaPoseRepository = yogaPoseRepository;
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
        if (!yogaPoseRepository.existsById(id)) {
            throw new YogaPoseNotFoundException("Yoga pose not found with id: " + id);
        }
        yogaPoseRepository.deleteById(id);
    }
}
