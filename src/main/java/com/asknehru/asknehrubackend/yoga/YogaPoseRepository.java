package com.asknehru.asknehrubackend.yoga;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import java.util.List;

@Repository
public interface YogaPoseRepository extends JpaRepository<YogaPose, Long> {
    List<YogaPose> findByYogaNameContainingIgnoreCase(String yogaName);
}
