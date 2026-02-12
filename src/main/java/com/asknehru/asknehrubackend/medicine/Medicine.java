package com.asknehru.asknehrubackend.medicine;

import jakarta.persistence.*;
import java.time.Instant;
import java.time.LocalDate;
import java.util.ArrayList;
import java.util.List;

@Entity
@Table(name = "medicines")
public class Medicine {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, length = 200)
    private String name;

    @Column(length = 200)
    private String brand;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false, length = 50)
    private MedicineCategory category;

    @Column(nullable = false)
    private Integer quantity;

    @Column(length = 50)
    private String unit;

    @Column(nullable = false)
    private LocalDate expiryDate;

    @Column
    private LocalDate manufactureDate;

    @Column(columnDefinition = "TEXT")
    private String description;

    @Column(columnDefinition = "TEXT")
    private String dosageInstructions;

    @ElementCollection
    @CollectionTable(name = "medicine_ingredients", joinColumns = @JoinColumn(name = "medicine_id"))
    @Column(name = "ingredient")
    private List<String> ingredients = new ArrayList<>();

    @ElementCollection
    @CollectionTable(name = "medicine_side_effects", joinColumns = @JoinColumn(name = "medicine_id"))
    @Column(name = "side_effect")
    private List<String> sideEffects = new ArrayList<>();

    @ElementCollection
    @CollectionTable(name = "medicine_benefits", joinColumns = @JoinColumn(name = "medicine_id"))
    @Column(name = "benefit")
    private List<String> benefits = new ArrayList<>();

    @Column(length = 200)
    private String location;

    @Column(nullable = false, updatable = false)
    private Instant createdAt;

    @Column(nullable = false)
    private Instant lastUpdated;

    @PrePersist
    void onCreate() {
        Instant now = Instant.now();
        createdAt = now;
        lastUpdated = now;
    }

    @PreUpdate
    void onUpdate() {
        lastUpdated = Instant.now();
    }

    // Getters and Setters

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getBrand() {
        return brand;
    }

    public void setBrand(String brand) {
        this.brand = brand;
    }

    public MedicineCategory getCategory() {
        return category;
    }

    public void setCategory(MedicineCategory category) {
        this.category = category;
    }

    public Integer getQuantity() {
        return quantity;
    }

    public void setQuantity(Integer quantity) {
        this.quantity = quantity;
    }

    public String getUnit() {
        return unit;
    }

    public void setUnit(String unit) {
        this.unit = unit;
    }

    public LocalDate getExpiryDate() {
        return expiryDate;
    }

    public void setExpiryDate(LocalDate expiryDate) {
        this.expiryDate = expiryDate;
    }

    public LocalDate getManufactureDate() {
        return manufactureDate;
    }

    public void setManufactureDate(LocalDate manufactureDate) {
        this.manufactureDate = manufactureDate;
    }

    public String getDescription() {
        return description;
    }

    public void setDescription(String description) {
        this.description = description;
    }

    public String getDosageInstructions() {
        return dosageInstructions;
    }

    public void setDosageInstructions(String dosageInstructions) {
        this.dosageInstructions = dosageInstructions;
    }

    public List<String> getIngredients() {
        return ingredients;
    }

    public void setIngredients(List<String> ingredients) {
        this.ingredients = ingredients;
    }

    public List<String> getSideEffects() {
        return sideEffects;
    }

    public void setSideEffects(List<String> sideEffects) {
        this.sideEffects = sideEffects;
    }

    public List<String> getBenefits() {
        return benefits;
    }

    public void setBenefits(List<String> benefits) {
        this.benefits = benefits;
    }

    public String getLocation() {
        return location;
    }

    public void setLocation(String location) {
        this.location = location;
    }

    public Instant getCreatedAt() {
        return createdAt;
    }

    public void setCreatedAt(Instant createdAt) {
        this.createdAt = createdAt;
    }

    public Instant getLastUpdated() {
        return lastUpdated;
    }

    public void setLastUpdated(Instant lastUpdated) {
        this.lastUpdated = lastUpdated;
    }
}
