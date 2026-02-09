package com.asknehru.asknehrubackend.yoga;

import jakarta.persistence.*;
import com.fasterxml.jackson.annotation.JsonIgnore;

@Entity
@Table(name = "pose_steps")
public class DetailedStep {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "pose_id", nullable = false)
    @JsonIgnore
    private YogaPose yogaPose;
    
    @Column(name = "step_order")
    private Integer order;
    
    @Column(nullable = false)
    private String title;
    
    private String stage;
    
    @Column(length = 2000)
    private String description;
    
    private String breath;
    
    // Getters and Setters
    public Long getId() {
        return id;
    }
    
    public void setId(Long id) {
        this.id = id;
    }
    
    public YogaPose getYogaPose() {
        return yogaPose;
    }
    
    public void setYogaPose(YogaPose yogaPose) {
        this.yogaPose = yogaPose;
    }
    
    public Integer getOrder() {
        return order;
    }
    
    public void setOrder(Integer order) {
        this.order = order;
    }
    
    public String getTitle() {
        return title;
    }
    
    public void setTitle(String title) {
        this.title = title;
    }
    
    public String getStage() {
        return stage;
    }
    
    public void setStage(String stage) {
        this.stage = stage;
    }
    
    public String getDescription() {
        return description;
    }
    
    public void setDescription(String description) {
        this.description = description;
    }
    
    public String getBreath() {
        return breath;
    }
    
    public void setBreath(String breath) {
        this.breath = breath;
    }
}
