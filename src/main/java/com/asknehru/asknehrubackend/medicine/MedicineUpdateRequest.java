package com.asknehru.asknehrubackend.medicine;

import java.time.LocalDate;
import java.util.List;

public class MedicineUpdateRequest {
    
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

    // Getters and Setters

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
}
