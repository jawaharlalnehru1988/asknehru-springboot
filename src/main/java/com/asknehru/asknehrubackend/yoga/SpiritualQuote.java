package com.asknehru.asknehrubackend.yoga;

import jakarta.persistence.Column;
import jakarta.persistence.Embeddable;

@Embeddable
public class SpiritualQuote {
    
    @Column(length = 1000)
    private String text;
    
    private String author;
    
    // Getters and Setters
    public String getText() {
        return text;
    }
    
    public void setText(String text) {
        this.text = text;
    }
    
    public String getAuthor() {
        return author;
    }
    
    public void setAuthor(String author) {
        this.author = author;
    }
}
