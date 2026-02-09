package com.asknehru.asknehrubackend.yoga;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import java.util.List;

@RestController
@RequestMapping("/api/yoga/poses")
@CrossOrigin(origins = "*")
public class YogaPoseController {
    
    private final YogaPoseService yogaPoseService;
    
    public YogaPoseController(YogaPoseService yogaPoseService) {
        this.yogaPoseService = yogaPoseService;
    }
    
    @GetMapping
    public ResponseEntity<List<YogaPose>> getAllPoses() {
        return ResponseEntity.ok(yogaPoseService.getAllPoses());
    }
    
    @GetMapping("/{id}")
    public ResponseEntity<YogaPose> getPoseById(@PathVariable Long id) {
        return ResponseEntity.ok(yogaPoseService.getPoseById(id));
    }
    
    @GetMapping("/pose-id/{poseId}")
    public ResponseEntity<YogaPose> getPoseByPoseId(@PathVariable String poseId) {
        return ResponseEntity.ok(yogaPoseService.getPoseByPoseId(poseId));
    }
    
    @GetMapping("/difficulty/{difficulty}")
    public ResponseEntity<List<YogaPose>> getPosesByDifficulty(@PathVariable String difficulty) {
        return ResponseEntity.ok(yogaPoseService.getPosesByDifficulty(difficulty));
    }
    
    @GetMapping("/category/{category}")
    public ResponseEntity<List<YogaPose>> getPosesByCategory(@PathVariable String category) {
        return ResponseEntity.ok(yogaPoseService.getPosesByCategory(category));
    }
    
    @GetMapping("/tag/{tag}")
    public ResponseEntity<List<YogaPose>> getPosesByTag(@PathVariable String tag) {
        return ResponseEntity.ok(yogaPoseService.getPosesByTag(tag));
    }
    
    @GetMapping("/search")
    public ResponseEntity<List<YogaPose>> searchPoses(@RequestParam String name) {
        return ResponseEntity.ok(yogaPoseService.searchPosesByName(name));
    }
    
    @GetMapping("/popular")
    public ResponseEntity<List<YogaPose>> getPopularPoses() {
        return ResponseEntity.ok(yogaPoseService.getPopularPoses());
    }
    
    @PostMapping
    public ResponseEntity<YogaPose> createPose(@RequestBody YogaPose yogaPose) {
        YogaPose created = yogaPoseService.createPose(yogaPose);
        return ResponseEntity.status(HttpStatus.CREATED).body(created);
    }
    
    @PutMapping("/{id}")
    public ResponseEntity<YogaPose> updatePose(@PathVariable Long id, @RequestBody YogaPose yogaPose) {
        return ResponseEntity.ok(yogaPoseService.updatePose(id, yogaPose));
    }
    
    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deletePose(@PathVariable Long id) {
        yogaPoseService.deletePose(id);
        return ResponseEntity.noContent().build();
    }
    
    @ExceptionHandler(YogaPoseNotFoundException.class)
    public ResponseEntity<String> handleNotFound(YogaPoseNotFoundException ex) {
        return ResponseEntity.status(HttpStatus.NOT_FOUND).body(ex.getMessage());
    }
}
