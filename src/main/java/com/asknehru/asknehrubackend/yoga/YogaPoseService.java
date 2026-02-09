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
    
    public YogaPose getPoseByPoseId(String poseId) {
        return yogaPoseRepository.findByPoseId(poseId)
                .orElseThrow(() -> new YogaPoseNotFoundException("Yoga pose not found with poseId: " + poseId));
    }
    
    public List<YogaPose> getPosesByDifficulty(String difficulty) {
        YogaPose.Difficulty difficultyEnum = YogaPose.Difficulty.valueOf(difficulty.toUpperCase());
        return yogaPoseRepository.findByDifficulty(difficultyEnum);
    }
    
    public List<YogaPose> getPosesByCategory(String category) {
        return yogaPoseRepository.findByCategory(category);
    }
    
    public List<YogaPose> getPosesByTag(String tag) {
        return yogaPoseRepository.findByTagsContaining(tag);
    }
    
    public List<YogaPose> searchPosesByName(String name) {
        return yogaPoseRepository.findByNameContainingIgnoreCase(name);
    }
    
    public List<YogaPose> getPopularPoses() {
        return yogaPoseRepository.findAllByOrderByPopularityDesc();
    }
    
    @Transactional
    public YogaPose createPose(YogaPose yogaPose) {
        // Set bidirectional relationships
        if (yogaPose.getBenefits() != null) {
            yogaPose.getBenefits().forEach(benefit -> benefit.setYogaPose(yogaPose));
        }
        if (yogaPose.getDetailedSteps() != null) {
            for (int i = 0; i < yogaPose.getDetailedSteps().size(); i++) {
                DetailedStep step = yogaPose.getDetailedSteps().get(i);
                step.setYogaPose(yogaPose);
                step.setOrder(i + 1);
            }
        }
        return yogaPoseRepository.save(yogaPose);
    }
    
    @Transactional
    public YogaPose updatePose(Long id, YogaPose updatedPose) {
        YogaPose existingPose = getPoseById(id);
        
        existingPose.setPoseId(updatedPose.getPoseId());
        existingPose.setName(updatedPose.getName());
        existingPose.setEnglishName(updatedPose.getEnglishName());
        existingPose.setSanskritName(updatedPose.getSanskritName());
        existingPose.setDifficulty(updatedPose.getDifficulty());
        existingPose.setImageUrl(updatedPose.getImageUrl());
        existingPose.setImageContext(updatedPose.getImageContext());
        existingPose.setDescription(updatedPose.getDescription());
        existingPose.setQuickBenefit(updatedPose.getQuickBenefit());
        existingPose.setDuration(updatedPose.getDuration());
        existingPose.setCategory(updatedPose.getCategory());
        existingPose.setSpiritualQuote(updatedPose.getSpiritualQuote());
        existingPose.setPopularity(updatedPose.getPopularity());
        
        // Update collections
        existingPose.getContraindications().clear();
        existingPose.getContraindications().addAll(updatedPose.getContraindications());
        
        existingPose.getMistakes().clear();
        existingPose.getMistakes().addAll(updatedPose.getMistakes());
        
        existingPose.getTags().clear();
        existingPose.getTags().addAll(updatedPose.getTags());
        
        // Update benefits
        existingPose.getBenefits().clear();
        if (updatedPose.getBenefits() != null) {
            updatedPose.getBenefits().forEach(benefit -> {
                benefit.setYogaPose(existingPose);
                existingPose.getBenefits().add(benefit);
            });
        }
        
        // Update steps
        existingPose.getDetailedSteps().clear();
        if (updatedPose.getDetailedSteps() != null) {
            for (int i = 0; i < updatedPose.getDetailedSteps().size(); i++) {
                DetailedStep step = updatedPose.getDetailedSteps().get(i);
                step.setYogaPose(existingPose);
                step.setOrder(i + 1);
                existingPose.getDetailedSteps().add(step);
            }
        }
        
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
