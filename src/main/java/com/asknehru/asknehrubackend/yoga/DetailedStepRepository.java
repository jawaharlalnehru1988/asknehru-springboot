package com.asknehru.asknehrubackend.yoga;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface DetailedStepRepository extends JpaRepository<DetailedStep, Long> {
}
