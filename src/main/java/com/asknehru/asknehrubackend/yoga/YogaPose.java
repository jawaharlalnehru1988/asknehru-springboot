package com.asknehru.asknehrubackend.yoga;

import jakarta.persistence.*;

@Entity
@Table(name = "yoga_poses")
public class YogaPose {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @Column(nullable = false)
    private String yogaName;
    
    @Column(length = 10000)
    private String blogContent;
    
    @Column(length = 1000)
    private String audioURL;
    
    @Column(length = 1000)
    private String videoURL;
    
    @Column(length = 1000)
    private String imageURL;

    private String category;
    
    // Getters and Setters
    public Long getId() {
        return id;
    }
    
    public void setId(Long id) {
        this.id = id;
    }
    
    public String getYogaName() {
        return yogaName;
    }
    
    public void setYogaName(String yogaName) {
        this.yogaName = yogaName;
    }
    
    public String getBlogContent() {
        return blogContent;
    }
    
    public void setBlogContent(String blogContent) {
        this.blogContent = blogContent;
    }
    
    public String getAudioURL() {
        return audioURL;
    }
    
    public void setAudioURL(String audioURL) {
        this.audioURL = audioURL;
    }
    
    public String getVideoURL() {
        return videoURL;
    }
    
    public void setVideoURL(String videoURL) {
        this.videoURL = videoURL;
    }
    
    public String getImageURL() {
        return imageURL;
    }

    public void setImageURL(String imageURL) {
        this.imageURL = imageURL;
    }

    public String getCategory() {
        return category;
    }

    public void setCategory(String category) {
        this.category = category;
    }
}
