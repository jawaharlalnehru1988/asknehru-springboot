package com.asknehru.asknehrubackend.yoga;

import jakarta.persistence.*;
import java.util.ArrayList;
import java.util.List;

@Entity
@Table(name = "yoga_poses")
public class YogaPose {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @Column(unique = true, nullable = false)
    private String poseId; // pose001, pose002, etc.
    
    @Column(nullable = false)
    private String name;
    
    private String englishName;
    private String sanskritName;
    
    @Enumerated(EnumType.STRING)
    private Difficulty difficulty;
    
    @Column(length = 1000)
    private String imageUrl;
    
    private String imageContext;
    
    @Column(length = 2000)
    private String description;
    
    private String quickBenefit;
    
    @OneToMany(mappedBy = "yogaPose", cascade = CascadeType.ALL, orphanRemoval = true)
    private List<Benefit> benefits = new ArrayList<>();
    
    @OneToMany(mappedBy = "yogaPose", cascade = CascadeType.ALL, orphanRemoval = true)
    private List<DetailedStep> detailedSteps = new ArrayList<>();
    
    @ElementCollection
    @CollectionTable(name = "pose_contraindications", joinColumns = @JoinColumn(name = "pose_id"))
    @Column(name = "contraindication")
    private List<String> contraindications = new ArrayList<>();
    
    @ElementCollection
    @CollectionTable(name = "pose_mistakes", joinColumns = @JoinColumn(name = "pose_id"))
    @Column(name = "mistake")
    private List<String> mistakes = new ArrayList<>();
    
    private String duration;
    
    @ElementCollection
    @CollectionTable(name = "pose_tags", joinColumns = @JoinColumn(name = "pose_id"))
    @Column(name = "tag")
    private List<String> tags = new ArrayList<>();
    
    private String category;
    
    @Embedded
    private SpiritualQuote spiritualQuote;
    
    private Integer popularity;
    
    public enum Difficulty {
        BEGINNER, INTERMEDIATE, ADVANCED
    }
    
    // Getters and Setters
    public Long getId() {
        return id;
    }
    
    public void setId(Long id) {
        this.id = id;
    }
    
    public String getPoseId() {
        return poseId;
    }
    
    public void setPoseId(String poseId) {
        this.poseId = poseId;
    }
    
    public String getName() {
        return name;
    }
    
    public void setName(String name) {
        this.name = name;
    }
    
    public String getEnglishName() {
        return englishName;
    }
    
    public void setEnglishName(String englishName) {
        this.englishName = englishName;
    }
    
    public String getSanskritName() {
        return sanskritName;
    }
    
    public void setSanskritName(String sanskritName) {
        this.sanskritName = sanskritName;
    }
    
    public Difficulty getDifficulty() {
        return difficulty;
    }
    
    public void setDifficulty(Difficulty difficulty) {
        this.difficulty = difficulty;
    }
    
    public String getImageUrl() {
        return imageUrl;
    }
    
    public void setImageUrl(String imageUrl) {
        this.imageUrl = imageUrl;
    }
    
    public String getImageContext() {
        return imageContext;
    }
    
    public void setImageContext(String imageContext) {
        this.imageContext = imageContext;
    }
    
    public String getDescription() {
        return description;
    }
    
    public void setDescription(String description) {
        this.description = description;
    }
    
    public String getQuickBenefit() {
        return quickBenefit;
    }
    
    public void setQuickBenefit(String quickBenefit) {
        this.quickBenefit = quickBenefit;
    }
    
    public List<Benefit> getBenefits() {
        return benefits;
    }
    
    public void setBenefits(List<Benefit> benefits) {
        this.benefits = benefits;
    }
    
    public List<DetailedStep> getDetailedSteps() {
        return detailedSteps;
    }
    
    public void setDetailedSteps(List<DetailedStep> detailedSteps) {
        this.detailedSteps = detailedSteps;
    }
    
    public List<String> getContraindications() {
        return contraindications;
    }
    
    public void setContraindications(List<String> contraindications) {
        this.contraindications = contraindications;
    }
    
    public List<String> getMistakes() {
        return mistakes;
    }
    
    public void setMistakes(List<String> mistakes) {
        this.mistakes = mistakes;
    }
    
    public String getDuration() {
        return duration;
    }
    
    public void setDuration(String duration) {
        this.duration = duration;
    }
    
    public List<String> getTags() {
        return tags;
    }
    
    public void setTags(List<String> tags) {
        this.tags = tags;
    }
    
    public String getCategory() {
        return category;
    }
    
    public void setCategory(String category) {
        this.category = category;
    }
    
    public SpiritualQuote getSpiritualQuote() {
        return spiritualQuote;
    }
    
    public void setSpiritualQuote(SpiritualQuote spiritualQuote) {
        this.spiritualQuote = spiritualQuote;
    }
    
    public Integer getPopularity() {
        return popularity;
    }
    
    public void setPopularity(Integer popularity) {
        this.popularity = popularity;
    }
}
