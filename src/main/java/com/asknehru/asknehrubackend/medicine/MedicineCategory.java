package com.asknehru.asknehrubackend.medicine;

public enum MedicineCategory {
    AYURVEDIC("Ayurvedic"),
    ALLOPATHIC("Allopathic"),
    HOMEOPATHIC("Homeopathic"),
    OTHER("Other");

    private final String displayName;

    MedicineCategory(String displayName) {
        this.displayName = displayName;
    }

    public String getDisplayName() {
        return displayName;
    }
}
