package com.asknehru.asknehrubackend.medicine;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.time.LocalDate;
import java.util.List;

@Repository
public interface MedicineRepository extends JpaRepository<Medicine, Long> {
    
    List<Medicine> findByCategory(MedicineCategory category);
    
    List<Medicine> findByNameContainingIgnoreCase(String name);
    
    @Query("SELECT m FROM Medicine m WHERE m.expiryDate BETWEEN :startDate AND :endDate")
    List<Medicine> findExpiringBetween(@Param("startDate") LocalDate startDate, @Param("endDate") LocalDate endDate);
    
    @Query("SELECT m FROM Medicine m WHERE m.expiryDate < :date")
    List<Medicine> findExpiredBefore(@Param("date") LocalDate date);
    
    @Query("SELECT m FROM Medicine m WHERE m.quantity <= :threshold")
    List<Medicine> findLowStock(@Param("threshold") Integer threshold);
}
