package com.asknehru.asknehrubackend.medicine;

import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/medicines")
@CrossOrigin(origins = "*")
public class MedicineController {
    private final MedicineService medicineService;

    public MedicineController(MedicineService medicineService) {
        this.medicineService = medicineService;
    }

    @PostMapping
    public ResponseEntity<MedicineResponse> create(@Valid @RequestBody MedicineCreateRequest request) {
        Medicine medicine = medicineService.create(request);
        return ResponseEntity.status(HttpStatus.CREATED).body(toResponse(medicine));
    }

    @GetMapping
    public List<MedicineResponse> list() {
        return medicineService.list().stream().map(this::toResponse).toList();
    }

    @GetMapping("/{id}")
    public MedicineResponse get(@PathVariable Long id) {
        Medicine medicine = medicineService.get(id)
            .orElseThrow(() -> new MedicineNotFoundException("Medicine not found with id: " + id));
        return toResponse(medicine);
    }

    @GetMapping("/category/{category}")
    public List<MedicineResponse> getByCategory(@PathVariable MedicineCategory category) {
        return medicineService.findByCategory(category).stream()
            .map(this::toResponse)
            .toList();
    }

    @GetMapping("/search")
    public List<MedicineResponse> search(@RequestParam String name) {
        return medicineService.searchByName(name).stream()
            .map(this::toResponse)
            .toList();
    }

    @GetMapping("/expiring-soon")
    public List<MedicineResponse> getExpiringSoon(@RequestParam(defaultValue = "30") int days) {
        return medicineService.findExpiringSoon(days).stream()
            .map(this::toResponse)
            .toList();
    }

    @GetMapping("/expired")
    public List<MedicineResponse> getExpired() {
        return medicineService.findExpired().stream()
            .map(this::toResponse)
            .toList();
    }

    @GetMapping("/low-stock")
    public List<MedicineResponse> getLowStock(@RequestParam(defaultValue = "10") int threshold) {
        return medicineService.findLowStock(threshold).stream()
            .map(this::toResponse)
            .toList();
    }

    @PutMapping("/{id}")
    public MedicineResponse update(@PathVariable Long id, @Valid @RequestBody MedicineUpdateRequest request) {
        Medicine medicine = medicineService.update(id, request);
        return toResponse(medicine);
    }

    @DeleteMapping("/{id}")
    @ResponseStatus(HttpStatus.NO_CONTENT)
    public void delete(@PathVariable Long id) {
        medicineService.delete(id);
    }

    private MedicineResponse toResponse(Medicine medicine) {
        return new MedicineResponse(
            medicine.getId(),
            medicine.getName(),
            medicine.getBrand(),
            medicine.getCategory(),
            medicine.getQuantity(),
            medicine.getUnit(),
            medicine.getExpiryDate(),
            medicine.getManufactureDate(),
            medicine.getDescription(),
            medicine.getDosageInstructions(),
            medicine.getIngredients(),
            medicine.getSideEffects(),
            medicine.getBenefits(),
            medicine.getLocation(),
            medicine.getCreatedAt(),
            medicine.getLastUpdated()
        );
    }

    @ExceptionHandler(MedicineNotFoundException.class)
    public ResponseEntity<String> handleNotFound(MedicineNotFoundException ex) {
        return ResponseEntity.status(HttpStatus.NOT_FOUND).body(ex.getMessage());
    }
}
