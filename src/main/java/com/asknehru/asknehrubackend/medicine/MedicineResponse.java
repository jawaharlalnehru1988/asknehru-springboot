package com.asknehru.asknehrubackend.medicine;

import java.time.Instant;
import java.time.LocalDate;
import java.util.List;

public class MedicineResponse {
    
    private Long id;
    private String name;
    private String brand;
    private MedicineCategory category;
    private Integer quantity;
    private String unit;
    private LocalDate expiryDate;
    private LocalDate manufactureDate;
    private String description;
    private String dosageInstructions;
    private List<String> ingredients;
    private List<String> sideEffects;
    private List<String> benefits;
    private String location;
    private Instant createdAt;
    private Instant lastUpdated;

    public MedicineResponse(Long id, String name, String brand, MedicineCategory category, 
                          Integer quantity, String unit, LocalDate expiryDate, 
                          LocalDate manufactureDate, String description, String dosageInstructions,
                          List<String> ingredients, List<String> sideEffects, List<String> benefits,
                          String location, Instant createdAt, Instant lastUpdated) {
        this.id = id;
        this.name = name;
        this.brand = brand;
        this.category = category;
        this.quantity = quantity;
        this.unit = unit;
        this.expiryDate = expiryDate;
        this.manufactureDate = manufactureDate;
        this.description = description;
        this.dosageInstructions = dosageInstructions;
        this.ingredients = ingredients;
        this.sideEffects = sideEffects;
        this.benefits = benefits;
        this.location = location;
        this.createdAt = createdAt;
        this.lastUpdated = lastUpdated;
    }

    // Getters

    public Long getId() {
        return id;
    }

    public String getName() {
        return name;
    }

    public String getBrand() {
        return brand;
    }

    public MedicineCategory getCategory() {
        return category;
    }

    public Integer getQuantity() {
        return quantity;
    }

    public String getUnit() {
        return unit;
    }

    public LocalDate getExpiryDate() {
        return expiryDate;
    }

    public LocalDate getManufactureDate() {
        return manufactureDate;
    }

    public String getDescription() {
        return description;
    }

    public String getDosageInstructions() {
        return dosageInstructions;
    }

    public List<String> getIngredients() {
        return ingredients;
    }

    public List<String> getSideEffects() {
        return sideEffects;
    }

    public List<String> getBenefits() {
        return benefits;
    }

    public String getLocation() {
        return location;
    }

    public Instant getCreatedAt() {
        return createdAt;
    }

    public Instant getLastUpdated() {
        return lastUpdated;
    }
}
