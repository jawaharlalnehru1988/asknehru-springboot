package com.asknehru.asknehrubackend.medicine;

public class MedicineNotFoundException extends RuntimeException {
    public MedicineNotFoundException(String message) {
        super(message);
    }
}
