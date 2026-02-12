package com.asknehru.asknehrubackend.medicine;

import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDate;
import java.util.List;
import java.util.Optional;

@Service
public class MedicineService {
    private final MedicineRepository medicineRepository;

    public MedicineService(MedicineRepository medicineRepository) {
        this.medicineRepository = medicineRepository;
    }

    @Transactional
    public Medicine create(MedicineCreateRequest request) {
        Medicine medicine = new Medicine();
        medicine.setName(request.getName().trim());
        medicine.setBrand(request.getBrand() != null ? request.getBrand().trim() : null);
        medicine.setCategory(request.getCategory());
        medicine.setQuantity(request.getQuantity());
        medicine.setUnit(request.getUnit() != null ? request.getUnit().trim() : "Tablets");
        medicine.setExpiryDate(request.getExpiryDate());
        medicine.setManufactureDate(request.getManufactureDate());
        medicine.setDescription(request.getDescription());
        medicine.setDosageInstructions(request.getDosageInstructions());
        medicine.setIngredients(request.getIngredients());
        medicine.setSideEffects(request.getSideEffects());
        medicine.setBenefits(request.getBenefits());
        medicine.setLocation(request.getLocation());
        
        return medicineRepository.save(medicine);
    }

    @Transactional(readOnly = true)
    public List<Medicine> list() {
        return medicineRepository.findAll();
    }

    @Transactional(readOnly = true)
    public Optional<Medicine> get(Long id) {
        return medicineRepository.findById(id);
    }

    @Transactional(readOnly = true)
    public List<Medicine> findByCategory(MedicineCategory category) {
        return medicineRepository.findByCategory(category);
    }

    @Transactional(readOnly = true)
    public List<Medicine> searchByName(String name) {
        return medicineRepository.findByNameContainingIgnoreCase(name);
    }

    @Transactional(readOnly = true)
    public List<Medicine> findExpiringSoon(int days) {
        LocalDate now = LocalDate.now();
        LocalDate futureDate = now.plusDays(days);
        return medicineRepository.findExpiringBetween(now, futureDate);
    }

    @Transactional(readOnly = true)
    public List<Medicine> findExpired() {
        return medicineRepository.findExpiredBefore(LocalDate.now());
    }

    @Transactional(readOnly = true)
    public List<Medicine> findLowStock(int threshold) {
        return medicineRepository.findLowStock(threshold);
    }

    @Transactional
    public Medicine update(Long id, MedicineUpdateRequest request) {
        Medicine medicine = medicineRepository.findById(id)
            .orElseThrow(() -> new MedicineNotFoundException("Medicine not found with id: " + id));

        if (request.getName() != null && !request.getName().isBlank()) {
            medicine.setName(request.getName().trim());
        }
        if (request.getBrand() != null) {
            medicine.setBrand(request.getBrand().trim());
        }
        if (request.getCategory() != null) {
            medicine.setCategory(request.getCategory());
        }
        if (request.getQuantity() != null) {
            medicine.setQuantity(request.getQuantity());
        }
        if (request.getUnit() != null) {
            medicine.setUnit(request.getUnit().trim());
        }
        if (request.getExpiryDate() != null) {
            medicine.setExpiryDate(request.getExpiryDate());
        }
        if (request.getManufactureDate() != null) {
            medicine.setManufactureDate(request.getManufactureDate());
        }
        if (request.getDescription() != null) {
            medicine.setDescription(request.getDescription());
        }
        if (request.getDosageInstructions() != null) {
            medicine.setDosageInstructions(request.getDosageInstructions());
        }
        if (request.getIngredients() != null) {
            medicine.setIngredients(request.getIngredients());
        }
        if (request.getSideEffects() != null) {
            medicine.setSideEffects(request.getSideEffects());
        }
        if (request.getBenefits() != null) {
            medicine.setBenefits(request.getBenefits());
        }
        if (request.getLocation() != null) {
            medicine.setLocation(request.getLocation());
        }

        return medicineRepository.save(medicine);
    }

    @Transactional
    public void delete(Long id) {
        if (!medicineRepository.existsById(id)) {
            throw new MedicineNotFoundException("Medicine not found with id: " + id);
        }
        medicineRepository.deleteById(id);
    }
}
