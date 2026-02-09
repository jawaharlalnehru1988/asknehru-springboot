package com.asknehru.asknehrubackend.yoga;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import java.util.List;
import java.util.Optional;

@Repository
public interface YogaPoseRepository extends JpaRepository<YogaPose, Long> {
    Optional<YogaPose> findByPoseId(String poseId);
    List<YogaPose> findByDifficulty(YogaPose.Difficulty difficulty);
    List<YogaPose> findByCategory(String category);
    List<YogaPose> findByTagsContaining(String tag);
    List<YogaPose> findByNameContainingIgnoreCase(String name);
    List<YogaPose> findAllByOrderByPopularityDesc();
}
